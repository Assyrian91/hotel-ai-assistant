from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from app.config import GROQ_API_KEY, LLM_MODEL
from app.agents.sql_agent import query_sql
from app.agents.rag_agent import query_rag

llm = ChatGroq(api_key=GROQ_API_KEY, model_name=LLM_MODEL, temperature=0)

ROUTER_PROMPT = PromptTemplate.from_template("""
You are a routing assistant for a hotel management system.
Classify the user question into ONE of these categories:

- SQL: questions about data, numbers, bookings, revenue, guests, occupancy, statistics, pricing history
- RAG: questions about hotel policy, procedures, check-in/out, cancellation, amenities, operations guide
- GENERAL: greetings, general hotel questions, or anything else

User question: {question}

Reply with ONLY one word: SQL, RAG, or GENERAL
""")

def classify_intent(question: str) -> str:
    chain = ROUTER_PROMPT | llm
    result = chain.invoke({"question": question})
    intent = result.content.strip().upper()
    if intent not in ["SQL", "RAG", "GENERAL"]:
        intent = "GENERAL"
    return intent

def handle_general(question: str) -> str:
    system = """You are an AI hotel operations assistant for Grand Palace Hotel.
    You help hotel managers with insights, analytics, and operations.
    Be concise, professional, and helpful."""
    from langchain_core.messages import SystemMessage, HumanMessage
    result = llm.invoke([SystemMessage(content=system), HumanMessage(content=question)])
    return result.content

def route_query(question: str) -> dict:
    intent = classify_intent(question)
    if intent == "SQL":
        answer = query_sql(question)
    elif intent == "RAG":
        answer = query_rag(question)
    else:
        answer = handle_general(question)
    return {"intent": intent, "answer": answer}
