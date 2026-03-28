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

load_dotenv()

class BasicChatbot(TypedDict):
    messages:Annotated[list,add_messages]

search_tool = TavilySearchResults(max_results= 2,TAVILY_API_KEY=os.getenv('TAVILY_API_KEY'))
tools = [search_tool]

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash',api_key=os.getenv("GOOGLE_API_KEY"))
llm_with_tool=llm.bind_tools(tools=tools)

def chatbot(state: BasicChatbot):
    return{
        'messages': [llm_with_tool.invoke(state['messages'])]
    }

def tools_router(state: BasicChatbot):
    last_message = state['messages'][-1]
    
    if(hasattr(last_message,'tools_calls') and len(last_message.tool_calls)>0):
        return 'tool_node'
    else:
        return END 

tool_node = ToolNode(tools=tools)



graph=StateGraph(BasicChatbot)
graph.add_node('chatbot',chatbot)
graph.add_node('tool_node',tool_node)

graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot",tools_router)
graph.add_edge("tool_node","chatbot")
app=graph.compile()
while True:
    userinput=input('user: ')
    if userinput=='exit':
        break
    else:
        res=app.invoke({'messages':[HumanMessage(content=userinput)]})
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

load_dotenv()

class BasicChatbot(TypedDict):
    messages:Annotated[list,add_messages]

search_tool = TavilySearchResults(max_results= 2,TAVILY_API_KEY=os.getenv('TAVILY_API_KEY'))
tools = [search_tool]

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash',api_key=os.getenv("GOOGLE_API_KEY"))
llm_with_tool=llm.bind_tools(tools=tools)

def chatbot(state: BasicChatbot):
    return{
        'messages': [llm_with_tool.invoke(state['messages'])]
    }

def tools_router(state: BasicChatbot):
    last_message = state['messages'][-1]
    
    if(hasattr(last_message,'tools_calls') and len(last_message.tool_calls)>0):
        return 'tool_node'
    else:
        return END 

tool_node = ToolNode(tools=tools)



graph=StateGraph(BasicChatbot)
graph.add_node('chatbot',chatbot)
graph.add_node('tool_node',tool_node)

graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot",tools_router)
graph.add_edge("tool_node","chatbot")
app=graph.compile()
while True:
    userinput=input('user: ')
    if userinput=='exit':
        break
    else:
        res=app.invoke({'messages':[HumanMessage(content=userinput)]})
>>>>>>> master
        print(res['messages'][1].content)