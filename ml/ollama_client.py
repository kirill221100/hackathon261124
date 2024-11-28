import requests
from typing import List, Dict, Any, Optional

class OllamaClient:
    def __init__(
        self, 
        host: str = "localhost",
        llm_port: int = 11434,
        temperature: float = 0.0,
        model_name: str = "gemma2:9b",
        embedding_model: str = "nextfire/paraphrase-multilingual-minilm:l12-v2"
    ):
        self.base_url = f"http://{host}:{llm_port}"
        self.temperature = temperature
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.available_models = self.list_models()

    def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Pull/download a model and return status."""
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name}
            )
            return {
                "success": response.status_code == 200,
                "message": f"Model {model_name} downloaded successfully" if response.status_code == 200 else f"Failed to download {model_name}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error downloading model: {str(e)}"
            }

    def list_models(self) -> List[str]:
        """Return list of available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return [model['name'] for model in response.json()['models']]
            return []
        except Exception as e:
            return []

    def set_model(self, model_name: str, model_type: str = "llm") -> Dict[str, Any]:
        """Set and validate model, return status."""
        if model_name not in self.available_models:
            pull_result = self.pull_model(model_name)
            if not pull_result["success"]:
                return pull_result
            self.available_models = self.list_models()

        if model_type == "llm":
            self.model_name = model_name
        elif model_type == "embedding":
            self.embedding_model = model_name
            
        return {
            "success": True,
            "message": f"Successfully set {model_type} model to {model_name}",
            "model_type": model_type,
            "model_name": model_name
        }

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "temperature": self.temperature
        }
        if system:
            payload["system"] = system
        response = requests.post(f"{self.base_url}/api/generate", json=payload)
        return response.json()['response']

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.embedding_model, "prompt": text}
            )
            if response.status_code == 200:
                embeddings.append(response.json()["embedding"])
        return embeddings
