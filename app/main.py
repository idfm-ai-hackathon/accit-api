from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket
from app.core.config import settings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
# from app.api.routes import chat, transport
# from app.core.config import settings
# from app.db.elasticsearch import init_elasticsearch
# from app.db.duckdb import init_duckdb
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Accessibility Assistant for Paris Transportation",
)

loader = UnstructuredFileLoader("ai_adoption_google.pdf")
docs = loader.load()

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=2000,
    chunk_overlap=200
)
texts = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings()

db = FAISS.from_documents(texts, embeddings)

# llm = Ollama(model="llama3")
llm = Ollama(model="qwen2.5-coder")

chain = RetrievalQA.from_chain_type(
    llm,
    retriever=db.as_retriever()
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"}, status_code=200)

@app.get("/config")
async def get_config():
    return settings.dict()

@app.get("/chat")
async def chat():
    question = "What is the document about?"
    return chain.invoke({"query": question})
