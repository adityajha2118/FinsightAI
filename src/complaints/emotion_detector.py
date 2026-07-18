import os, time
from dotenv import load_dotenv
load_dotenv()

def _get_llm():
    """Initialize LLM client based on LLM_PROVIDER env variable."""
    provider = os.getenv("LLM_PROVIDER", "gemini")
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(model="llama-3.1-70b-versatile", temperature=0.0)
    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

def detect_emotion(narrative: str) -> str:
    """Detect emotion: Anger, Frustration, Neutral, Legal Threat, Distress."""
    prompt = (f"Detect the dominant emotion in this financial complaint. "
              f"Return ONLY one word from: Anger, Frustration, Neutral, Legal Threat, Distress. "
              f"No other text. Complaint: {narrative[:800]}")
    for attempt in range(2):
        try:
            llm = _get_llm()
            return llm.invoke(prompt).content.strip()
        except Exception as e:
            if attempt == 0:
                time.sleep(2)
                continue
            return "Neutral"
    return "Neutral"
