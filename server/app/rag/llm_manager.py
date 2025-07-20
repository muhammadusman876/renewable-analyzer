"""
LLM Manager - Handles LLM initialization and configuration
Uses Groq API for fast, reliable LLM responses
"""
from typing import Optional
import os
from dotenv import load_dotenv

# Groq API imports
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError as e:
    GROQ_AVAILABLE = False
    print(f"Groq not available: {e}. Please install: pip install groq")


class LLMManager:
    """
    Manages Groq LLM connections and configurations for the RAG system
    """

    def __init__(self):
        load_dotenv()
        self.groq_api_key = self._load_groq_api_key()
        self.groq_client = None
        self.llm_available = False
        self.working_model = "llama-3.1-8b-instant"  # Default model
        self._initialize_groq()

    def _load_groq_api_key(self) -> Optional[str]:
        """Load Groq API key from environment"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            # Fallback: try to load from .env file
            try:
                env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
                if os.path.exists(env_path):
                    with open(env_path, 'r') as f:
                        for line in f:
                            if line.startswith('GROQ_API_KEY='):
                                api_key = line.split('=', 1)[1].strip()
                                break
            except Exception as e:
                print(f"Error reading .env file: {e}")

        return api_key

    def _initialize_groq(self):
        """Initialize the Groq client"""
        if not GROQ_AVAILABLE:
            print("Groq library not available, using template system")
            print("Install with: pip install groq")
            return

        if not self.groq_api_key:
            print("GROQ_API_KEY not found in environment variables")
            print("Falling back to template-based reports")
            return

        try:
            print("Initializing Groq LLM...")

            self.groq_client = Groq(api_key=self.groq_api_key)

            # Test the connection with a simple query - try multiple current models
            models_to_try = [
                "llama-3.1-8b-instant",
                "llama-3.3-70b-versatile",
                "gemma2-9b-it"
            ]

            test_successful = False
            working_model = None

            for model in models_to_try:
                try:
                    test_response = self.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": "Hello"}],
                        model=model,
                        max_tokens=50,
                        temperature=0.1
                    )

                    if test_response and test_response.choices:
                        test_successful = True
                        working_model = model
                        break
                except Exception as model_error:
                    print(f" Model {model} not available: {model_error}")
                    continue

            if test_successful:
                self.working_model = working_model
                self.llm_available = True
                print("Groq LLM initialized successfully!")
                print(f"Using model: {working_model}")
            else:
                print("No working Groq models found, using template system")
                self.llm_available = False

        except Exception as e:
            print(f"Groq initialization failed: {e}")
            print("Falling back to template-based reports")
            self.llm_available = False

    def get_llm(self):
        """Get the initialized Groq client"""
        return self.groq_client if self.llm_available else None

    def is_available(self) -> bool:
        """Check if LLM is available and working"""
        return self.llm_available

    async def generate_response(self, prompt: str) -> str:
        """Generate response using Groq LLM"""
        if not self.llm_available:
            raise Exception("Groq LLM not available")

        try:
            import asyncio
            import concurrent.futures

            loop = asyncio.get_event_loop()

            def run_groq():
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.working_model,  # Use the working model found during init
                    max_tokens=2000,
                    temperature=0.3
                )
                return response.choices[0].message.content

            result = await loop.run_in_executor(None, run_groq)
            return result or ""
        except Exception as e:
            raise Exception(f"Groq LLM generation failed: {e}")


# Alias for backwards compatibility
GroqLLMManager = LLMManager
