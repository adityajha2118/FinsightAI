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

def classify_complaint(narrative: str) -> str:
    """Classify complaint into: Billing, Fraud, Card Declined, Rewards, Customer Service, Service Delay, Credit Reporting, Collections."""
    categories = "Billing, Fraud, Card Declined, Rewards, Customer Service, Service Delay, Credit Reporting, Collections"
    prompt = (f"Classify this financial complaint into exactly ONE category. "
              f"Categories: {categories}. "
              f"Return ONLY the category name with no other text. "
              f"Complaint: {narrative[:800]}")
    for attempt in range(2):
        try:
            llm = _get_llm()
            return llm.invoke(prompt).content.strip()
        except Exception as e:
            if attempt == 0:
                time.sleep(2)
                continue
            return "Unknown"
    return "Unknown"
