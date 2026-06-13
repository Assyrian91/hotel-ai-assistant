import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, LLM_MODEL, DOCS_PATH, FAISS_PATH

_rag_chain = None

def get_llm():
    return ChatGroq(api_key=GROQ_API_KEY, model_name=LLM_MODEL, temperature=0.3)

def build_vector_store():
    loader = DirectoryLoader(DOCS_PATH, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(FAISS_PATH)
    return vectorstore

def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

def get_rag_chain():
    global _rag_chain
    if _rag_chain:
        return _rag_chain
    if os.path.exists(FAISS_PATH):
        vectorstore = load_vector_store()
    else:
        vectorstore = build_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    _rag_chain = RetrievalQA.from_chain_type(
        llm=get_llm(),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False
    )
    return _rag_chain

def query_rag(question: str) -> str:
    chain = get_rag_chain()
    result = chain.invoke({"query": question})
    return result["result"]
