from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from operator import add as add_messages
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import requests
from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()
#file input
#while loop logic

def bro(query):

    pdf_path ='pdf/Fundamentals of Building Autonomous LLM.pdf'
    pages = PyPDFLoader(pdf_path).load()

    text_splitter= RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,
            separators=[
            "\n\n",
            "\n",
            " ",
            ""
            ])

    pages_split=text_splitter.split_documents(pages)
    persist_directory = r"C:\Users\mawiy\OneDrive\Desktop\Legal-Agent\learning Langraph\pdf"
    collection_name = "cases"

    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)

    from langchain_community.embeddings import JinaEmbeddings
    jina = JinaEmbeddings(
                    api_key=os.getenv('JINA_API_KEY'),
                    model_name="jina-embeddings-v3",
                )

    vectorstore = Chroma.from_documents(
        documents = pages_split,
        persist_directory= persist_directory,
        collection_name=collection_name,
        embedding=jina
    )

    def retriever(str) :
        ret= vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        return ret.invoke(str)



    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_classic.retrievers import EnsembleRetriever
    from langchain_classic.retrievers import BM25Retriever

    llm= ChatGoogleGenerativeAI(model='gemini-2.0-flash')
    bm25_retriver = BM25Retriever.from_documents(pages_split)
    ret= vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
    ensemble_ret=EnsembleRetriever(retrievers=[ret,bm25_retriver],
                                weights=[0.5,0.5]
                                )

    query=query
    results = ensemble_ret.invoke(query)    
    answer=llm.invoke(f'this is the relevent context {results} based on this and your understanding give me appropriate answer best to your knowledge ')
    return answer.content



