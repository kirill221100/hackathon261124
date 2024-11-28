import json
from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.http import models
from scripts.ollama_client import OllamaClient

class TextIndexer:
    def __init__(self, text: str, ollama_client: OllamaClient, qdrant_client: QdrantClient, 
                 scs: int = 50, bcs: int = 500, overlap: float = 0.1):
        self.text = text
        self.ollama = ollama_client
        self.qdrant = qdrant_client
        self.collection_name = "text"
        
        self.scs, self.bcs, self.overlap = scs, bcs, overlap
        self.chunk_index = {
            "small_chunks": {},
            "large_chunks": {}
        }

    def create_collection(self):
        test_emb = self.ollama.get_embeddings(["test"])[0]
        
        self.qdrant.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=len(test_emb),
                distance=models.Distance.COSINE
            )
        )

    def chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[Dict]:
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            if end >= len(text):
                chunk_text = text[start:]
            else:
                last_space = text[start:end].rfind(' ')
                if last_space != -1:
                    end = start + last_space
                chunk_text = text[start:end]
            
            chunks.append({
                "text": chunk_text,
                "start": start,
                "end": end
            })
            
            start = end - overlap
            
        return chunks

    def index_chunks(self, chunks: List[Dict], start_id: int, chunk_type: str):
        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = self.ollama.get_embeddings(chunk_texts)
        
        points = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = start_id + idx
            
            self.chunk_index[f"{chunk_type}_chunks"][chunk_id] = {
                "text": chunk["text"],
                "start": chunk["start"],
                "end": chunk["end"]
            }
            
            points.append(
                models.PointStruct(
                    id=chunk_id,
                    vector=embedding,
                    payload={
                        "text": chunk["text"],
                        "start": chunk["start"],
                        "end": chunk["end"],
                        "type": chunk_type
                    }
                )
            )
        
        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def process_file(self):
        self.create_collection()
        small_chunks = self.chunk_text(self.text, chunk_size=self.scs, overlap=int(self.scs * self.overlap))
        self.index_chunks(small_chunks, start_id=0, chunk_type="small")
        large_chunks = self.chunk_text(self.text, chunk_size=self.bcs, overlap=int(self.bcs * self.overlap))
        self.index_chunks(large_chunks, start_id=len(small_chunks), chunk_type="large")
        with open('chunk_index.json', 'w') as f:
            json.dump(self.chunk_index, f)

    def retrieve(self, query_vector: List[float], top_k: int = 10) -> List[Dict]:
        results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        return [{"score": hit.score, "payload": hit.payload} for hit in results]
