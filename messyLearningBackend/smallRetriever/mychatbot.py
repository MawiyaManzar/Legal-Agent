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
from systemmessage import system_message
# from langchain_community.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec

load_dotenv()

def embed_pdf(pdf_path):

    # 1. Load PDF pages
    pages = PyPDFLoader(pdf_path).load()

    # 2. Chunk into smaller pieces
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    pages_split = text_splitter.split_documents(pages)

    # 3. Convert Document objects → plain text
    texts = [d.page_content for d in pages_split]

    # 4. Init Jina embeddings (LangChain wrapper)
    jina = JinaEmbeddings(
        api_key=os.getenv("JINA_API_KEY"),
        model_name="jina-embeddings-v3"
    )

    # 5. Embed using LangChain interface
    embeddings = jina.embed_documents(texts)

    pc= PineconeVectorStore(os.getenv('PINECONE_API_KEY'))

    INDEX_NAME = "my-jina-index"

    if INDEX_NAME not in [i["name"] for i in pc.list_indexes()]:
        pc.create_index(
            name=INDEX_NAME,
            dimension=1024,   # ❗ model "jina-embeddings-v3" is 1024-dimensional
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    index = pc.Index(INDEX_NAME)

    vectors_to_upsert = []

    for i, vector in enumerate(embeddings):
        chunk_id = f"chunk-{i}"

        metadata = {
            "text": texts[i],
            "page": pages_split[i].metadata.get("page", None),
        }

        vectors_to_upsert.append((chunk_id, vector, metadata))
    
    index.upsert(vectors=vectors_to_upsert)



    return embeddings, texts, pages_split



import os, time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import JinaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# --- Step 1: Load and chunk PDF ---
def load_pdf(pdf_path):
    pages = PyPDFLoader(pdf_path).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(pages)


# --- Step 2: Setup Pinecone ---
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
INDEX_NAME = "my-jina-index"

if INDEX_NAME not in [i["name"] for i in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=1024,       # because Jina v3 uses 1024 dims
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    while not pc.describe_index(INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pc.Index(INDEX_NAME)


# --- Step 3: Initialize vector store ---
embedding = JinaEmbeddings(
    api_key=os.getenv("JINA_API_KEY"),
    model_name="jina-embeddings-v3"
)

vector_store = PineconeVectorStore(index=index, embedding=embedding)


# --- Step 4: Upload PDF ---
chunks = load_pdf("/home/mawiya/Desktop/Backup/useful/legal_Agent/backend/smallRetriever/ResumeMawiya (2).pdf")
ids = [f"chunk-{i}" for i in range(len(chunks))]
print(ids)
# vector_store.add_documents(documents=chunks, ids=ids)
results=vector_store.similarity_search("what is Mawiya Manzar skills ?",k=1 )
for doc in results:
    print("-----")
    print(doc.page_content)
    print(doc.metadata)

print("Uploaded", len(chunks), "chunks into Pinecone!")

    



# embed_pdf("/home/mawiya/Desktop/Backup/useful/legal_Agent/backend/smallRetriever/uploads/Techathon 6 Statements.pdf")