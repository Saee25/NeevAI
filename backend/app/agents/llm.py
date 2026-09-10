import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    from langchain_groq import ChatGroq
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    if os.getenv("GROQ_API_KEY"):
        return ChatGroq(model="openai/gpt-oss-120b", temperature=0)
    elif os.getenv("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    else:
        raise ValueError("No LLM API key found. Please set GROQ_API_KEY or GOOGLE_API_KEY.")
