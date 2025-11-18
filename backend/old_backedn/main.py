from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv
from typing import Optional,List,TypedDict


load_dotenv()
# ---- 1. Define the State ----
# State is a dict-like object that flows between nodes
class AgentState(TypedDict):
    research_mode: bool
    query: str
    documents: Optional[List]
    summary: Optional[str]
    report: Optional[str]
    answer: Optional[str]

# ---- 2. Define Nodes ----

# Direct Answer Node
def direct_answer(state: AgentState, config: RunnableConfig):
    """Direct answer with token streaming"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        streaming=True  # Enable token streaming
    )
    prompt = f"""
    As a professional legal advisor, provide a well-structured answer to: {state['query']}
    
    Format your response with:
    - Clear headings using ## for main sections
    - **Bold text** for important legal concepts
    - Bullet points for key information
    - Proper citations where applicable
    """
    
    # Stream the response
    response = llm.stream(prompt, config=config)
    full_response = ""
    
    for chunk in response:
        if hasattr(chunk, 'content'):
            full_response += chunk.content
    
    state["answer"] = full_response
    state["research_mode"] = False
    return state

# Retriever Node (mock)
def retriever(state: AgentState):
    # Imagine this calls a case law API
    import requests

    def fetch_kanoon_data(user_input, api_token, pagenum=0):
        url = "https://api.indiankanoon.org/search/"
        headers = {"Authorization": f"Token {api_token}", "Accept": "application/json"}
        params = {"formInput": user_input, "pagenum": pagenum}
        try:
            response = requests.post(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant fields and generate case links
            results = []
            for doc in data.get('docs', []):
                case_info = {
                    'tid': doc.get('tid'),
                    'title': doc.get('title'),
                    'docsource': doc.get('docsource'),
                    'publishdate': doc.get('publishdate'),
                    'author': doc.get('author'),
                    # 'bench': doc.get('bench'),
                    # 'catids': doc.get('catids'),
                    'citation': doc.get('citation'),
                    'numcites': doc.get('numcites'),
                    'numcitedby': doc.get('numcitedby'),
                    'link': f"https://indiankanoon.org/doc/{doc.get('tid')}/"
                }
                results.append(case_info)
            
            return {
                'cases': results,
                'found': data.get('found'),
                'encodedformInput': data.get('encodedformInput')
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
        
    api_token = "14643c2a5b137ab178234409a2e8b8e219629d60"
    result = fetch_kanoon_data(state['query'], api_token)

    # docs = [f"Case law related to: {state['query']}"]
    state["documents"] = result
    return state

# Summarizer Node
def summarizer(state: AgentState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    notes = llm.invoke(
        f"Summarize the following legal documents :\n{state['documents']}"
    )
    state["summary"] = notes.content
    return state

# Formatter Node
def formatter(state: AgentState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    schema = """
    Please provide a detailed legal analysis covering:
- A clear title for the case
- Proper citation format
- Comprehensive summary of the legal matter
- Relevant Indian laws and statutes applicable
- Pertinent case precedents from Indian courts
- Strong arguments that could lead to a favorable outcome
- Potential counter-arguments and weaknesses
- Legal conclusion based on the analysis
- Specific recommendations for legal strategy

Ensure all legal terminology is accurate and appropriate for Indian legal context.
   """
    report = llm.invoke(f"{schema}\n\nSummary:\n{state['summary']}")
    state["report"] = report.content
    state["research_mode"] = False  # reset
    return state

def build_graph():
    # ---- 1. Build the Graph ----
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("direct_answer", direct_answer)
    workflow.add_node("retriever", retriever)
    workflow.add_node("summarizer", summarizer)
    workflow.add_node("formatter", formatter)

    # ---- 2. Conditional branch function ----
    def decide_branch(state: AgentState):
        if state.get("research_mode"):
            print("--- RESEARCH MODE DETECTED, ROUTING TO RETRIEVER ---")
            return "retriever"
        else:
            print("--- DIRECT ANSWER MODE DETECTED, ROUTING TO DIRECT ANSWER ---")
            return "direct_answer"

    workflow.set_conditional_entry_point(
        decide_branch,
        {
            "retriever": "retriever",
            "direct_answer": "direct_answer",
        }
    )

    # ---- 3. Define graph edges ----
    workflow.add_edge("retriever", "summarizer")
    workflow.add_edge("summarizer", "formatter")
    workflow.add_edge("formatter", END)
    workflow.add_edge("direct_answer", END)

    # ---- 4. Compile Graph ----
    app = workflow.compile()
    
    return app

