<<<<<<< HEAD
from typing import TypedDict,Annotated
from langgraph.graph import add_messages,StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage,HumanMessage
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
import os
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver


load_dotenv()

sq_conn=sqlite3.connect("checkpoint.sqlite",check_same_thread=False)
memory= SqliteSaver(sq_conn)

llm=ChatGoogleGenerativeAI(model='gemini-2.5-flash')

class basicChatState(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state:basicChatState):
    return{
        "messages":[llm.invoke(state['messages'])]
    }

graph= StateGraph(basicChatState)
graph.add_node("chatbot",chatbot)
graph.add_edge('chatbot',END)
graph.set_entry_point("chatbot")
app= graph.compile(checkpointer=memory)

config = {
    "configurable":{
        "thread_id":1
    }
}    

while True:
    user_input = input("User :")
    if(user_input =="exit"):
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        },config=config)
        
        print("AI :" + result["messages"][-1].content)
=======
from typing import TypedDict,Annotated
from langgraph.graph import add_messages,StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage,HumanMessage
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
import os
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver


load_dotenv()

sq_conn=sqlite3.connect("checkpoint.sqlite",check_same_thread=False)
memory= SqliteSaver(sq_conn)

llm=ChatGoogleGenerativeAI(model='gemini-2.5-flash')

class basicChatState(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state:basicChatState):
    return{
        "messages":[llm.invoke(state['messages'])]
    }

graph= StateGraph(basicChatState)
graph.add_node("chatbot",chatbot)
graph.add_edge('chatbot',END)
graph.set_entry_point("chatbot")
app= graph.compile(checkpointer=memory)

config = {
    "configurable":{
        "thread_id":1
    }
}    

while True:
    user_input = input("User :")
    if(user_input =="exit"):
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        },config=config)
        
        print("AI :" + result["messages"][-1].content)
>>>>>>> master
        