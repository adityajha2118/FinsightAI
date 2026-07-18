from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import os, time
from dotenv import load_dotenv; load_dotenv()

from src.complaints.summarizer import summarize_complaint
from src.complaints.classifier import classify_complaint
from src.complaints.emotion_detector import detect_emotion
from src.complaints.escalation_model import load_escalation_model, predict_escalation, encode_for_escalation

class ComplaintState(TypedDict):
    narrative: str
    summary: str
    category: str
    emotion: str
    escalation_probability: float
    priority_level: str
    assigned_team: str
    recommended_action: str
    suggested_response: str

def summarize_node(state: ComplaintState) -> ComplaintState:
    """Call summarizer and update state with complaint summary."""
    state['summary'] = summarize_complaint(state['narrative'])
    return state

def classify_node(state: ComplaintState) -> ComplaintState:
    """Call classifier and update state with complaint category."""
    state['category'] = classify_complaint(state['narrative'])
    return state

def detect_emotion_node(state: ComplaintState) -> ComplaintState:
    """Call emotion detector and update state with detected emotion."""
    state['emotion'] = detect_emotion(state['narrative'])
    return state

def score_escalation_node(state: ComplaintState) -> ComplaintState:
    """Score escalation probability from current state features."""
    features = encode_for_escalation(state['category'], state['emotion'], len(state['narrative'].split()))
    result = predict_escalation(features)
    state['escalation_probability'] = result['escalation_probability']
    return state

def route_node(state: ComplaintState) -> ComplaintState:
    """Apply business rules to assign priority, team, and action."""
    prob = state['escalation_probability']
    emotion = state['emotion']
    if prob > 0.90:
        state['priority_level'] = "CRITICAL"
        state['assigned_team'] = "Supervisor"
        state['recommended_action'] = "Notify supervisor immediately"
    elif prob > 0.80:
        state['priority_level'] = "HIGH"
        state['assigned_team'] = "Priority Support"
        state['recommended_action'] = "Escalate to senior agent"
    elif emotion in ["Legal Threat", "Distress"]:
        state['priority_level'] = "CRITICAL"
        state['assigned_team'] = "Legal Compliance"
        state['recommended_action'] = "Escalate to compliance immediately"
    elif emotion == "Anger" and prob > 0.60:
        state['priority_level'] = "HIGH"
        state['assigned_team'] = "Priority Support"
        state['recommended_action'] = "Immediate callback required"
    else:
        state['priority_level'] = "STANDARD"
        state['assigned_team'] = "General Support"
        state['recommended_action'] = "Standard resolution process"
    return state

def generate_response_node(state: ComplaintState) -> ComplaintState:
    """Generate a professional customer response using LLM."""
    prompt = (
        f"Write a professional, empathetic 2-3 sentence response to a bank customer "
        f"whose complaint is about {state['category']}, "
        f"emotional state is {state['emotion']}, "
        f"and priority level is {state['priority_level']}. "
        f"Be concise, solution-focused, and avoid making specific promises about timelines."
    )
    provider = os.getenv("LLM_PROVIDER", "gemini")
    try:
        if provider == "groq":
            from langchain_groq import ChatGroq
            llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.3)
        elif provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
        else:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        state['suggested_response'] = llm.invoke(prompt).content.strip()
    except Exception as e:
        state['suggested_response'] = (
            "Thank you for bringing this to our attention. We take your concern seriously "
            "and a member of our team will contact you shortly to resolve this matter."
        )
    return state

def build_complaint_graph():
    """Build and compile the LangGraph complaint processing pipeline."""
    graph = StateGraph(ComplaintState)
    graph.add_node("summarize", summarize_node)
    graph.add_node("classify", classify_node)
    graph.add_node("detect_emotion", detect_emotion_node)
    graph.add_node("score_escalation", score_escalation_node)
    graph.add_node("route", route_node)
    graph.add_node("generate_response", generate_response_node)
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", "classify")
    graph.add_edge("classify", "detect_emotion")
    graph.add_edge("detect_emotion", "score_escalation")
    graph.add_edge("score_escalation", "route")
    graph.add_edge("route", "generate_response")
    graph.add_edge("generate_response", END)
    return graph.compile()

_agent = None

def run_complaint_agent(narrative: str) -> dict:
    """Run full complaint pipeline and return complete ComplaintState as dict."""
    global _agent
    if _agent is None:
        _agent = build_complaint_graph()
    initial_state = ComplaintState(
        narrative=narrative,
        summary="", category="", emotion="",
        escalation_probability=0.0,
        priority_level="", assigned_team="",
        recommended_action="", suggested_response=""
    )
    result = _agent.invoke(initial_state)
    return dict(result)
