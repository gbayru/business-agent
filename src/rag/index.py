from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


@dataclass
class RAGIndex:
    """
    Abstract handle to a vector index.
    Implementation can be Chroma/FAISS/pgvector/etc.
    """
    index_id: str
    meta: Dict[str, Any]


class VectorStore:
    """
    ChromaDB-based vector store implementation.
    """
    def __init__(self, base_dir: str = "data/indexes", embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=base_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        try:
            self.embedder = SentenceTransformer(embedding_model)
        except Exception as e:
            print(f"Warning: Could not load embedding model {embedding_model}: {e}")
            print("Falling back to stub mode. Install sentence-transformers for full functionality.")
            self.embedder = None

    def create_index(self, index_id: str) -> RAGIndex:
        """Create or get a ChromaDB collection"""
        collection_name = f"rag_index_{index_id}"
        
        # Get or create collection
        try:
            collection = self.client.get_collection(collection_name)
        except:
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"index_id": index_id}
            )
        
        return RAGIndex(index_id=index_id, meta={"collection_name": collection_name, "store": "chromadb"})

    def add_texts(
        self,
        index: RAGIndex,
        texts: List[str],
        metadatas: Optional[List[dict]] = None,
    ) -> None:
        """Add texts to the vector store with embeddings"""
        if not self.embedder:
            raise NotImplementedError("Embedding model not available. Install sentence-transformers.")
        
        if not texts:
            return
        
        collection_name = index.meta.get("collection_name", f"rag_index_{index.index_id}")
        try:
            collection = self.client.get_collection(collection_name)
        except:
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"index_id": index.index_id}
            )
        
        # Generate embeddings
        embeddings = self.embedder.encode(texts, show_progress_bar=False).tolist()
        
        # Prepare metadatas
        if metadatas is None:
            metadatas = [{}] * len(texts)
        
        # Generate IDs
        ids = [f"{index.index_id}_{i}" for i in range(len(texts))]
        
        # Add to collection
        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def query(
        self,
        index: RAGIndex,
        query_text: str,
        top_k: int = 3,
    ) -> List[dict]:
        """
        Query the vector store and return list of hits.
        Each hit includes: {"text": "...", "score": 0.0, "metadata": {...}}
        """
        if not self.embedder:
            return []  # Stub mode: return empty results
        
        collection_name = index.meta.get("collection_name", f"rag_index_{index.index_id}")
        try:
            collection = self.client.get_collection(collection_name)
        except:
            return []  # Collection doesn't exist
        
        # Generate query embedding
        query_embedding = self.embedder.encode([query_text], show_progress_bar=False).tolist()[0]
        
        # Query collection
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        hits = []
        if results.get("documents") and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                hit = {
                    "text": doc,
                    "score": 1.0 - (results.get("distances", [[1.0]])[0][i] if results.get("distances") else 1.0),
                    "metadata": results.get("metadatas", [[]])[0][i] if results.get("metadatas") else {}
                }
                hits.append(hit)
        
        return hits
