import os
import hashlib
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
USE_MOCK_EMBEDDINGS = os.getenv("USE_MOCK_EMBEDDINGS", "true").lower() == "true"


def generate_mock_embedding(text: str, dim: int = 1536) -> List[float]:
    """
    Generate a consistent mock embedding based on text hash.
    This allows the app to run without OpenAI API quota.
    """
    hash_obj = hashlib.sha256(text.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    
    # Generate deterministic embeddings from hash
    embeddings = []
    for i in range(dim):
        seed = hash_int + i
        # Use a simple deterministic random-like function
        value = ((seed * 1103515245 + 12345) % (2**31)) / (2**31)
        value = (value - 0.5) * 2  # Scale to [-1, 1]
        embeddings.append(value)
    
    return embeddings


async def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Async embedding wrapper using OpenAI or mock embeddings.
    Falls back to mock embeddings if OPENAI_API_KEY is invalid or USE_MOCK_EMBEDDINGS is true.
    """
    if not texts:
        return []

    if USE_MOCK_EMBEDDINGS:
        # Use mock embeddings for testing/development
        return [generate_mock_embedding(text) for text in texts]

    try:
        from openai import AsyncOpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not set, using mock embeddings")
            return [generate_mock_embedding(text) for text in texts]
            
        client = AsyncOpenAI(api_key=api_key)
        resp = await client.embeddings.create(
            model=EMBED_MODEL,
            input=texts,
        )
        return [d.embedding for d in resp.data]
    except Exception as e:
        print(f"Warning: OpenAI API call failed ({e}), falling back to mock embeddings")
        return [generate_mock_embedding(text) for text in texts]
