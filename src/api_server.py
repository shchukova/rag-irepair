"""
FastAPI REST API Server
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import uvicorn
import os
from datetime import datetime

app = FastAPI(title="iFixit RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = None
chatbot_initialized = False
sessions = {}


class InitializeRequest(BaseModel):
    device_name: str
    max_guides: int = 5
    model_name: str = "llama2"


class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    timestamp: str


@app.get("/")
async def root():
    return {"message": "iFixit RAG Chatbot API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "initialized": chatbot_initialized,
        "model": "llama2" if chatbot else "none"
    }


@app.post("/initialize")
async def initialize_chatbot(request: InitializeRequest):
    global chatbot, chatbot_initialized
    
    try:
        from ifixit_chatbot import IFixitRAGChatbot
        
        api_key = os.getenv('IFIXIT_API_KEY')
        chatbot = IFixitRAGChatbot(api_key=api_key, model_name=request.model_name)
        chatbot.build_knowledge_base(request.device_name, max_guides=request.max_guides)
        
        chatbot_initialized = True
        
        return {
            "status": "success",
            "message": f"Initialized for {request.device_name}",
            "device": request.device_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_chatbot(request: QueryRequest):
    global chatbot
    
    if not chatbot_initialized or not chatbot:
        raise HTTPException(status_code=400, detail="Not initialized")
    
    try:
        answer = chatbot.query(request.question)
        return QueryResponse(answer=answer, timestamp=datetime.now().isoformat())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset_chatbot():
    global chatbot, chatbot_initialized
    chatbot = None
    chatbot_initialized = False
    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083)
