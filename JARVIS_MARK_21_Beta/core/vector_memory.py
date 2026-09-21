"""
vector_memory.py - Persistent Vector Memory & RAG Context Engine for JARVIS
"""

import os
import json
import math
import re
from datetime import datetime

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

VECTOR_STORAGE_FILE = os.path.join("DATA", "vector_memory.json")


SYNONYM_MAP = {
    "pet": ["dog", "cat", "animal", "puppy", "pet"],
    "dog": ["pet", "animal", "dog"],
    "cat": ["pet", "animal", "cat"],
    "work": ["project", "task", "job", "deadline", "work"],
    "due": ["deadline", "date", "due", "time"],
    "deadline": ["due", "date", "schedule"],
    "name": ["called", "name", "identity"],
}


def _tokenize(text: str, expand: bool = False) -> list[str]:
    """Tokenize and normalize text into word tokens with optional synonym expansion."""
    tokens = re.findall(r"\w+", text.lower())
    if not expand:
        return tokens
    
    expanded = list(tokens)
    for t in tokens:
        if t in SYNONYM_MAP:
            expanded.extend(SYNONYM_MAP[t])
    return expanded


def _compute_tf_idf(tokens: list[str], idf_dict: dict) -> dict:
    """Calculate TF-IDF vector representation for a list of tokens."""
    tf = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1
    total = len(tokens) or 1
    vector = {}
    for t, count in tf.items():
        vector[t] = (count / total) * idf_dict.get(t, 1.0)
    return vector


def _cosine_similarity(vec1: dict, vec2: dict) -> float:
    """Compute cosine similarity between two sparse vector representations."""
    intersection = set(vec1.keys()) & set(vec2.keys())
    dot_product = sum([vec1[x] * vec2[x] for x in intersection])
    
    norm1 = math.sqrt(sum([val**2 for val in vec1.values()]))
    norm2 = math.sqrt(sum([val**2 for val in vec2.values()]))
    
    if not norm1 or not norm2:
        return 0.0
    return dot_product / (norm1 * norm2)


class VectorMemoryEngine:
    """Episodic RAG Vector Memory Engine."""

    def __init__(self):
        self.chroma_client = None
        self.chroma_collection = None
        
        os.makedirs("DATA", exist_ok=True)
        
        # Initialize ChromaDB if available
        if CHROMADB_AVAILABLE:
            try:
                self.chroma_client = chromadb.PersistentClient(path=os.path.join("DATA", "chroma_db"))
                self.chroma_collection = self.chroma_client.get_or_create_collection("jarvis_episodic_memory")
            except Exception as e:
                print(f"⚠️ ChromaDB initialization fallback: {e}")
                self.chroma_client = None

        self.memories = self._load_local_store()

    def _load_local_store(self) -> list[dict]:
        if os.path.exists(VECTOR_STORAGE_FILE):
            try:
                with open(VECTOR_STORAGE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_local_store(self):
        os.makedirs("DATA", exist_ok=True)
        with open(VECTOR_STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memories, f, indent=4)

    def index_memory(self, content: str, category: str = "chat", metadata: dict = None):
        """Index a piece of text memory into vector storage."""
        if not content or len(content.strip()) < 3:
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "id": f"mem_{len(self.memories) + 1}_{int(datetime.now().timestamp())}",
            "content": content.strip(),
            "category": category,
            "timestamp": timestamp,
            "metadata": metadata or {}
        }

        # Index in ChromaDB if available
        if self.chroma_collection:
            try:
                self.chroma_collection.add(
                    documents=[entry["content"]],
                    metadatas=[{"category": category, "timestamp": timestamp}],
                    ids=[entry["id"]]
                )
            except Exception as e:
                print(f"⚠️ ChromaDB indexing error: {e}")

        # Index in persistent JSON fallback store
        self.memories.append(entry)
        self._save_local_store()

    def retrieve_relevant_memories(self, query: str, top_k: int = 3) -> list[dict]:
        """Perform semantic vector retrieval for top_k relevant memories matching query."""
        if not query or not self.memories:
            return []

        # ChromaDB retrieval path
        if self.chroma_collection:
            try:
                results = self.chroma_collection.query(
                    query_texts=[query],
                    n_results=min(top_k, len(self.memories))
                )
                retrieved = []
                if results and "documents" in results and results["documents"]:
                    docs = results["documents"][0]
                    metas = results["metadatas"][0] if "metadatas" in results else []
                    for i, doc in enumerate(docs):
                        retrieved.append({
                            "content": doc,
                            "timestamp": metas[i].get("timestamp", "") if i < len(metas) else "",
                            "score": 0.9
                        })
                if retrieved:
                    return retrieved
            except Exception as e:
                print(f"⚠️ ChromaDB query error, using local vector fallback: {e}")

        # Local Vector Embedding TF-IDF & Cosine Similarity search fallback
        all_docs_tokens = [_tokenize(m["content"]) for m in self.memories]
        query_tokens = _tokenize(query, expand=True)

        if not query_tokens:
            return []

        # Calculate Document Frequencies for IDF
        doc_count = len(all_docs_tokens)
        df = {}
        for doc in all_docs_tokens:
            unique_terms = set(doc)
            for term in unique_terms:
                df[term] = df.get(term, 0) + 1

        idf_dict = {term: math.log((doc_count + 1) / (freq + 1)) + 1.0 for term, freq in df.items()}

        query_vec = _compute_tf_idf(query_tokens, idf_dict)

        scored_memories = []
        for i, mem in enumerate(self.memories):
            doc_vec = _compute_tf_idf(all_docs_tokens[i], idf_dict)
            sim = _cosine_similarity(query_vec, doc_vec)
            if sim > 0.01:  # Relevance threshold
                scored_memories.append({
                    "content": mem["content"],
                    "category": mem["category"],
                    "timestamp": mem["timestamp"],
                    "score": round(sim, 4)
                })

        # Sort by similarity score descending
        scored_memories.sort(key=lambda x: x["score"], reverse=True)
        return scored_memories[:top_k]

    def get_rag_formatted_context(self, query: str, top_k: int = 3) -> str:
        """Fetch and format relevant memories into a RAG context block for LLM prompt."""
        relevant = self.retrieve_relevant_memories(query, top_k=top_k)
        if not relevant:
            return ""

        context_lines = ["[Relevant Long-Term Memories & Historical Context]:"]
        for item in relevant:
            context_lines.append(f"- ({item['timestamp']}) {item['content']}")
        return "\n".join(context_lines) + "\n\n"


# Global singleton instance
vector_memory_engine = VectorMemoryEngine()


def add_to_vector_memory(text: str, category: str = "chat", metadata: dict = None):
    """Helper function to add memory entry."""
    vector_memory_engine.index_memory(text, category, metadata)


def get_rag_context(user_query: str) -> str:
    """Helper function to retrieve RAG context for prompt."""
    return vector_memory_engine.get_rag_formatted_context(user_query)
