# retriever.py
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


class FAQRetriever:
    def __init__(self, path: str = "data/faqs.txt"):
        print("STEP 1: Loading FAQ file...")
        text = Path(path).read_text(encoding="utf-8")
        self.chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
        print(f"STEP 2: Loaded {len(self.chunks)} chunks")

        print("STEP 3: Loading SentenceTransformer model...")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        print("STEP 4: Model loaded successfully")

        print("STEP 5: Creating ChromaDB client...")
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(name="faqs")
        print("STEP 6: ChromaDB collection ready")

        if self.collection.count() == 0:
            print("STEP 7: Embedding FAQ chunks...")
            embeddings = self.embedder.encode(self.chunks).tolist()
            ids = [f"faq_{i}" for i in range(len(self.chunks))]
            self.collection.add(documents=self.chunks, embeddings=embeddings, ids=ids)
            print("STEP 8: FAQs indexed successfully")

    def get_relevant(self, query: str, k: int = 3):
        query_embedding = self.embedder.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(k, len(self.chunks)),
        )
        docs = results["documents"][0] if results["documents"] else []
        distances = results["distances"][0] if results["distances"] else []
        relevant = [doc for doc, dist in zip(docs, distances) if dist < 1.0]
        if not relevant and docs:
            relevant = [docs[0]]
        return relevant