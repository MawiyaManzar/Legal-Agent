import requests
import os
from dotenv import load_dotenv

load_dotenv()

def embed_legal_documents(documents):
    """Store legal documents in your database"""
    url = 'https://api.jina.ai/v1/embeddings'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"
    }
    data = {
        "model": "jina-embeddings-v3",  # Correct model name
        "input": documents,
        # Remove unsupported parameters for this API
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error response: {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def search_legal_documents(query):
    """Search through your legal database"""
    url = 'https://api.jina.ai/v1/embeddings'
    headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"
    }
    data = {
        "model": "jina-embeddings-v3",
        "input": [query],  # Keep as list for single query
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error response: {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

# Test function
def test_embeddings():
    # Check if API key is set
    api_key = os.getenv('JINA_API_KEY')
    if not api_key:
        print("❌ JINA_API_KEY environment variable not set!")
        print("Please set it using: export JINA_API_KEY='your_key_here'")
        return
    
    print(f"✅ API Key found (first 10 chars): {api_key[:10]}...")
    
    # Test with smaller, simpler documents first
    legal_docs = [
        "Intellectual property clause governing patent rights",
        "Contract termination conditions and notice periods",
        "Confidentiality agreement for proprietary information"
    ]
    
    print("📄 Testing document embedding...")
    doc_embeddings = embed_legal_documents(legal_docs)
    
    if doc_embeddings:
        print("✅ Document embedding successful!")
        print(f"Number of documents embedded: {len(doc_embeddings.get('data', []))}")
        
        # Show embedding details
        if doc_embeddings.get('data'):
            first_embedding = doc_embeddings['data'][0]
            embedding_vector = first_embedding.get('embedding', [])
            print(f"Embedding dimensions: {len(embedding_vector)}")
            print(f"First 5 values: {embedding_vector[:5]}")
    
    print("\n🔍 Testing search query...")
    query_embedding = search_legal_documents("What are the patent rights terms?")
    
    if query_embedding:
        print("✅ Query embedding successful!")
        if query_embedding.get('data'):
            query_vec = query_embedding['data'][0].get('embedding', [])
            print(f"Query embedding dimensions: {len(query_vec)}")
            print(f"First 5 values: {query_vec[:5]}")

# Alternative: Using the correct Jina model names
def embed_legal_documents_v2(documents):
    """Alternative version with correct parameters"""
    url = 'https://api.jina.ai/v1/embeddings'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"
    }
    data = {
        "model": "jina-embeddings-v3",  # or try "jina-embeddings-v2-base-en"
        "input": documents,
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Run the test
if __name__ == "__main__":
    test_embeddings()