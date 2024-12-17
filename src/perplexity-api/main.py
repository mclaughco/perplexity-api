import os
import json
import requests
from typing import Dict, Optional, Union, Generator
from dotenv import load_dotenv
from dataclasses import dataclass
from cryptography.fernet import Fernet

@dataclass
class PerplexityConfig:
    """
    Configuration class for Perplexity API settings.
    
    Attributes:
        api_key (str): The API key for authentication
        base_url (str): The base URL for the API
        model (str): The AI model to use (default: llama-3.1-sonar-small-128k-online)
        temperature (float): Controls randomness in responses (0.0 to 1.0)
        top_p (float): Controls diversity of responses
        max_tokens (Optional[int]): Maximum tokens in response
        presence_penalty (float): Penalty for new topic introduction
        frequency_penalty (float): Penalty for repetition
    """
    api_key: str
    base_url: str = "https://api.perplexity.ai/chat/completions"
    model: str = "llama-3.1-sonar-small-128k-online"
    temperature: float = 0.2
    top_p: float = 0.9
    max_tokens: Optional[int] = None
    presence_penalty: float = 0
    frequency_penalty: float = 1
    search_domain_filter: Optional[list] = None
    return_images: bool = False
    return_related_questions: bool = False
    search_recency_filter: str = "month"
    top_k: int = 0

class PerplexityAPI:
    """
    Main class for interacting with the Perplexity API.
    """
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Perplexity API client.
        
        Args:
            api_key (Optional[str]): API key for authentication. If not provided,
                                   will attempt to load from environment variables.
        """
        load_dotenv()
        self.config = PerplexityConfig(
            api_key=api_key or os.getenv("PPLX_API_KEY")
        )
        if not self.config.api_key:
            raise ValueError("API key not found. Set PPLX_API_KEY environment variable or pass it directly.")
        
        # Encrypt API key in memory
        self._key = Fernet.generate_key()
        self._fernet = Fernet(self._key)
        self._encrypted_key = self._fernet.encrypt(self.config.api_key.encode())

    def _get_headers(self) -> Dict[str, str]:
        """Generate headers for API requests including authentication."""
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._fernet.decrypt(self._encrypted_key).decode()}"
        }

    def query(self, prompt: str, system_prompt: str = "Be precise and concise.") -> Dict[str, Union[str, dict]]:
        """
        Send a single query to the Perplexity API.
        
        Args:
            prompt (str): The user's prompt
            system_prompt (str): System instructions for the model
            
        Returns:
            Dict[str, Union[str, dict]]: API response
        """
        try:
            payload = {
                "model": self.config.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
                "presence_penalty": self.config.presence_penalty,
                "frequency_penalty": self.config.frequency_penalty,
                "stream": False
            }
            
            # Add optional parameters if set
            if self.config.max_tokens:
                payload["max_tokens"] = self.config.max_tokens
            if self.config.search_domain_filter:
                payload["search_domain_filter"] = self.config.search_domain_filter
            if self.config.search_recency_filter:
                payload["search_recency_filter"] = self.config.search_recency_filter
            
            payload.update({
                "return_images": self.config.return_images,
                "return_related_questions": self.config.return_related_questions,
                "top_k": self.config.top_k
            })

            response = requests.post(
                self.config.base_url,
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")

    def stream_query(self, prompt: str, system_prompt: str = "Be precise and concise.") -> Generator[Dict, None, None]:
        """
        Stream responses from the Perplexity API.
        
        Args:
            prompt (str): The user's prompt
            system_prompt (str): System instructions for the model
            
        Yields:
            Dict: Each chunk of the streaming response as a parsed dictionary
        """
        try:
            payload = {
                "model": self.config.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
                "presence_penalty": self.config.presence_penalty,
                "frequency_penalty": self.config.frequency_penalty,
                "stream": True
            }

            # Add optional parameters
            if self.config.max_tokens:
                payload["max_tokens"] = self.config.max_tokens
            if self.config.search_domain_filter:
                payload["search_domain_filter"] = self.config.search_domain_filter
            if self.config.search_recency_filter:
                payload["search_recency_filter"] = self.config.search_recency_filter
            
            payload.update({
                "return_images": self.config.return_images,
                "return_related_questions": self.config.return_related_questions,
                "top_k": self.config.top_k
            })

            response = requests.post(
                self.config.base_url,
                headers=self._get_headers(),
                json=payload,
                stream=True,
                timeout=30
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line and line.strip():
                    try:
                        # Handle potential data: prefix in SSE
                        data = line.decode('utf-8')
                        if data.startswith('data: '):
                            data = data[6:]
                        yield json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Streaming request failed: {str(e)}")

def main():
    """Example usage of the PerplexityAPI class."""
    try:
        # Initialize API client
        client = PerplexityAPI()
        
        # Example query
        print("Regular query response:")
        response = client.query(
            prompt="How many stars are there in our galaxy?",
            system_prompt="Be precise and concise."
        )
        print(json.dumps(response, indent=2))
        
        # Example streaming query
        print("\nStreaming response:")
        for chunk in client.stream_query("What is the distance to the moon?"):
            # Print only the content from the assistant's message if available
            if 'choices' in chunk and chunk['choices']:
                choice = chunk['choices'][0]
                if 'delta' in choice and 'content' in choice['delta']:
                    content = choice['delta']['content']
                    if content:
                        print(content, end='', flush=True)
        print()  # Add newline at the end
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
