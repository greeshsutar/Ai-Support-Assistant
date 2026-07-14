# retriever.py
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


class FAQRetriever:
    def __init__(self, path: str = "data/faqs.txt"):
        # Load FAQ file
        text = Path(path).read_text(encoding="utf-8")

        # Split FAQs into blocks separated by blank lines
        self.chunks = [c.strip() for c in text.split("\n\n") if c.strip()]

        # Load embedding model
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        # Set up in-memory ChromaDB client + collection
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name="faqs")

        # Embed and index all FAQ chunks (only if collection is empty)
        if self.collection.count() == 0:
            embeddings = self.embedder.encode(self.chunks).tolist()
            ids = [f"faq_{i}" for i in range(len(self.chunks))]
            self.collection.add(
                documents=self.chunks,
                embeddings=embeddings,
                ids=ids,
            )

    def get_relevant(self, query: str, k: int = 3):
        # Embed the query
        query_embedding = self.embedder.encode([query]).tolist()

        # Semantic search against ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(k, len(self.chunks)),
        )

        docs = results["documents"][0] if results["documents"] else []
        distances = results["distances"][0] if results["distances"] else []

        # Filter out weak matches (lower distance = more similar)
        # Cosine distance threshold — tune based on testing
        relevant = [doc for doc, dist in zip(docs, distances) if dist < 1.0]

        # Fallback: if nothing passes the threshold, return the closest match anyway
        if not relevant and docs:
            relevant = [docs[0]]

        return relevant