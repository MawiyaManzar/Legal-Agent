<<<<<<< HEAD
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
from langchain_community.embeddings import JinaEmbeddings
import pickle
from langchain_classic.retrievers import BM25Retriever
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.retrievers import EnsembleRetriever


load_dotenv()

def initialise_retirevers(pdf_path):
    '''run this once'''
    #load
    pages= PyPDFLoader(pdf_path).load()
    text_splitter= RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    pages_split= text_splitter.split_documents(pages)
    
    persist_directory = "vectorstore/"
    collection_name = "cases"
    bm25_cache = "vectorstore/bm25_retriever.pkl"
    
    jina = JinaEmbeddings(
                    api_key=os.getenv('JINA_API_KEY'),
                    model_name="jina-embeddings-v3",
                )

    vectorstore = Chroma(
        persist_directory=persist_directory,
        collection_name=collection_name,
        embedding_function=jina
    )
    
    if vectorstore._collection.count() == 0:
        vectorstore.add_documents(pages_split)
        print("indexed document in chroma")
    
    #setup bm25
    if os.path.exists(bm25_cache):
        with open(bm25_cache,'rb') as f:
            bm25_retriever = pickle.load(f)

    else:
        bm25_retriever = BM25Retriever.from_documents(pages_split)
        with open(bm25_cache,'wb') as f:
            pickle.dump(bm25_retriever,f)
        print('created bm25 cache')
    
    return vectorstore,bm25_retriever

def bro(query):
    
    '''fast query function- no reindexing'''
    jina = JinaEmbeddings(
        api_key=os.getenv('JINA_API_KEY'),
        model_name="jina-embeddings-v3"
    )
    
    vectorstore = Chroma(
        persist_directory="vectorstore/",
        collection_name="cases",
        embedding_function=jina
    )
    
    with open('vectorstore/bm25_retriever.pkl','rb') as f:
        bm25_retriever= pickle.load(f)
    
    
    ret=vectorstore.as_retriever(search_kwargs={"k":5})
    ensemble_ret = EnsembleRetriever(
        retrievers=[ret,bm25_retriever],
        weights=[0.5,0.5]
    )
    
    # query
    
    results=ensemble_ret.invoke(query)
    print(results)    
    llm= ChatGoogleGenerativeAI(
        model='gemini-2.0-flash'
    )        
    
    answer =llm.invoke(
        f'Context: {results}\n\nQuestion: {query}\n\nProvide an accurate answer.'
    )
    print(answer)
    
    return answer.content
        
        
=======
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
from langchain_community.embeddings import JinaEmbeddings
import pickle
from langchain_classic.retrievers import BM25Retriever
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.retrievers import EnsembleRetriever


load_dotenv()

def initialise_retirevers(pdf_path):
    '''run this once'''
    #load
    pages= PyPDFLoader(pdf_path).load()
    text_splitter= RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    pages_split= text_splitter.split_documents(pages)
    
    persist_directory = "vectorstore/"
    collection_name = "cases"
    bm25_cache = "vectorstore/bm25_retriever.pkl"
    
    jina = JinaEmbeddings(
                    api_key=os.getenv('JINA_API_KEY'),
                    model_name="jina-embeddings-v3",
                )

    vectorstore = Chroma(
        persist_directory=persist_directory,
        collection_name=collection_name,
        embedding_function=jina
    )
    
    if vectorstore._collection.count() == 0:
        vectorstore.add_documents(pages_split)
        print("indexed document in chroma")
    
    #setup bm25
    if os.path.exists(bm25_cache):
        with open(bm25_cache,'rb') as f:
            bm25_retriever = pickle.load(f)

    else:
        bm25_retriever = BM25Retriever.from_documents(pages_split)
        with open(bm25_cache,'wb') as f:
            pickle.dump(bm25_retriever,f)
        print('created bm25 cache')
    
    return vectorstore,bm25_retriever

def bro(query):
    
    '''fast query function- no reindexing'''
    jina = JinaEmbeddings(
        api_key=os.getenv('JINA_API_KEY'),
        model_name="jina-embeddings-v3"
    )
    
    vectorstore = Chroma(
        persist_directory="vectorstore/",
        collection_name="cases",
        embedding_function=jina
    )
    
    with open('vectorstore/bm25_retriever.pkl','rb') as f:
        bm25_retriever= pickle.load(f)
    
    
    ret=vectorstore.as_retriever(search_kwargs={"k":5})
    ensemble_ret = EnsembleRetriever(
        retrievers=[ret,bm25_retriever],
        weights=[0.5,0.5]
    )
    
    # query
    
    results=ensemble_ret.invoke(query)
    print(results)    
    llm= ChatGoogleGenerativeAI(
        model='gemini-2.0-flash'
    )        
    
    answer =llm.invoke(
        f'Context: {results}\n\nQuestion: {query}\n\nProvide an accurate answer.'
    )
    print(answer)
    
    return answer.content
        
        
>>>>>>> master
            