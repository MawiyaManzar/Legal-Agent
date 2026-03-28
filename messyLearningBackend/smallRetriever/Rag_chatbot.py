from dotenv import load_dotenv
import os
import time

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import JinaEmbeddings
from langchain_classic.retrievers import BM25Retriever, EnsembleRetriever
from langchain_google_genai import ChatGoogleGenerativeAI
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import pickle


from langchain_classic.chains.conversation.base import ConversationChain,LLMChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_mongodb import MongoDBChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_classic.prompts import PromptTemplate

PERSIST_DIRECTORY = "vectorstore/"
COLLECTION_NAME = "cases"
BM25_CACHE_PATH = os.path.join(PERSIST_DIRECTORY, "bm25_retriever.pkl")
PINECONE_INDEX_NAME = "my-jina-index"
EMBEDDING_MODEL_NAME = "jina-embeddings-v3"

load_dotenv()

def _load_and_split_pdf(pdf_path: str):
    """Load a PDF and split it into chunks."""
    pages = PyPDFLoader(pdf_path).load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    return text_splitter.split_documents(pages)


def _ensure_pinecone_index() -> "Pinecone.Index":
    """Ensure the Pinecone index exists and is ready, then return the index handle."""
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

    if PINECONE_INDEX_NAME not in [i["name"] for i in pc.list_indexes()]:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1024,       # because Jina v3 uses 1024 dims
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
            time.sleep(1)

    return pc.Index(PINECONE_INDEX_NAME)


def _build_vector_store(index, pages_split):
    """Create the vector store in Pinecone and add all document chunks."""
    embedding = JinaEmbeddings(
        api_key=os.getenv("JINA_API_KEY"),
        model_name=EMBEDDING_MODEL_NAME
    )

    vector_store = PineconeVectorStore(index=index, embedding=embedding)
    ids = [f"chunk-{i}" for i in range(len(pages_split))]
    vector_store.add_documents(documents=pages_split, ids=ids)


def _build_and_cache_bm25(pages_split):
    """Build a BM25 retriever from the chunks and cache it to disk."""
    bm25_retriever = BM25Retriever.from_documents(pages_split)
    with open(BM25_CACHE_PATH, 'wb') as f:
        pickle.dump(bm25_retriever, f)
    print('created bm25 cache')
    return bm25_retriever


def _get_vector_store_for_query():
    """Return a vector store connected to the existing Pinecone index (no re-upload)."""
    index = _ensure_pinecone_index()
    embedding = JinaEmbeddings(
        api_key=os.getenv("JINA_API_KEY"),
        model_name=EMBEDDING_MODEL_NAME
    )
    return PineconeVectorStore(index=index, embedding=embedding)


def _load_bm25_from_cache():
    """Load a cached BM25 retriever from disk."""
    if not os.path.exists(BM25_CACHE_PATH):
        raise FileNotFoundError(
            f"BM25 cache not found at {BM25_CACHE_PATH}. "
            "Run initialise_retrievers(pdf_path) at least once before querying."
        )
    with open(BM25_CACHE_PATH, 'rb') as f:
        return pickle.load(f)


def initialise_retrievers(pdf_path):
    """Run the full indexing pipeline once for a given PDF."""
    pages_split = _load_and_split_pdf(pdf_path)
    index = _ensure_pinecone_index()
    vector_store = _build_vector_store(index, pages_split)
    bm25_retriever = _build_and_cache_bm25(pages_split)

    return vector_store, bm25_retriever

from systemmessage import system_message
def bro(query):
    
    
    '''fast query function- no reindexing'''
    system_message_value = system_message() if callable(system_message) else system_message


    # Build hybrid retriever (vector + BM25) from existing index/cache
    vector_store = _get_vector_store_for_query()
    vector_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    bm25_retriever = _load_bm25_from_cache()

    ensemble_ret = EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        weights=[0.5, 0.5],
    )

    # Retrieve relevant chunks
    results = ensemble_ret.invoke(query)

    # Build context string for the LLM
    context_snippets = []
    for doc in results:
        context_snippets.append(doc.page_content)
    context_text = "\n\n---\n\n".join(context_snippets)

    #history stored in mongodb
    history=MongoDBChatMessageHistory(
        connection_string='mongodb+srv://mawiyamanzar:8750688779@cluster1.lqstsqr.mongodb.net/',
        database_name="Cluster1",
        collection_name="legalagentmemory",
        session_id="gemini1")
    #memory connector 
    memory=ConversationBufferMemory(
        chat_memory=history,
        return_messages=True,
        memory_key="history"
     )
   
    # FIX: Real PromptTemplate instead of raw string
    prompt = PromptTemplate(
        input_variables=["history", "context_text", "query"],
        template="""

Conversation so far:
{history}

Context:
{context_text}

Question:
{query}
"""
    )

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    chain = prompt | llm | StrOutputParser()

    # FIX: RunnableWithMessageHistory instead of deprecated ConversationChain
    runnable = RunnableWithMessageHistory(
        chain,
        lambda session_id: history,
        input_messages_key="query",
        history_messages_key="history"
    )

    response = runnable.invoke(
        {"query": query, "context_text": context_text,"system_message": system_message_value},
        config={"configurable": {"session_id": "gemini1"},"memory":memory},
    )

    print(response)
    return response
  







  
    # # Compose final prompt for the LLM
    # user_prompt = (
    #     # f"{system_message}"
    #     f"Use the following retrieved legal context to answer the question.\n\n"
    #     f"Context:\n{context_text}\n\n"
    #     f"Question: {query}"
    # )

    # llm= ChatGoogleGenerativeAI(
    #     model='gemini-2.0-flash'
    # )        
    # chain= ConversationChain(llm=llm,memory=memory,prompt=user_prompt)


    # answer = chain.invoke({
    #     "context": context_text,
    #     "question": query
    # })

    # print(answer)
    
    # return answer["response"]
        


    
    