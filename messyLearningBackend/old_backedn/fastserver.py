from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from main import build_graph
from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StructuredOutputParser

app= FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3100"],  # React dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()

@app.get("/")
async def root():
    return {"message":"hello"}

class QueryRequest (BaseModel):
    query:str
    research_mode:bool=False

@app.post("/ask")
async def askQuestions(request: QueryRequest):
    try:
        state = {
            "query": request.query,
            "research_mode": request.research_mode
        }
        result = graph.invoke(state)
        
        if request.research_mode:
            return {
                "success": True,
                "report": result.get("report"),
                "query": request.query,
                "mode": "research"
            }
        else:
            return {
                "success": True,
                "answer": result.get('answer'),
                "query": request.query,
                "mode": "direct"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": request.query,
            "mode": "research" if request.research_mode else "direct"
        }