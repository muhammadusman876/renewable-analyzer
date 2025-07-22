"""
LLM Manager - Handles LLM initialization and configuration
Uses LangChain with Groq API for structured LLM interactions
"""
from typing import Optional
import os
from dotenv import load_dotenv

# Groq API imports (direct)
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError as e:
    GROQ_AVAILABLE = False
    print(f"Groq not available: {e}. Please install: pip install groq")

# LangChain imports
try:
    from langchain_groq import ChatGroq
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langchain.schema import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    print(f"LangChain not available: {e}. Please install: pip install langchain langchain-groq")


class LLMManager:
    """
    Manages LLM connections using both direct Groq API and LangChain
    Provides fallback between LangChain and direct API calls
    """

    def __init__(self):
        load_dotenv()
        self.groq_api_key = self._load_groq_api_key()
        
        # Direct Groq client (fallback)
        self.groq_client = None
        
        # LangChain client (preferred)
        self.langchain_llm = None
        
        self.llm_available = False
        self.langchain_available = False
        self.working_model = "llama-3.1-8b-instant"  # Default model
        
        # Initialize both systems
        self._initialize_langchain()
        if not self.langchain_available:
            self._initialize_groq_fallback()

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

    def _initialize_langchain(self):
        """Initialize LangChain with Groq (preferred method)"""
        if not LANGCHAIN_AVAILABLE:
            print("LangChain not available, falling back to direct Groq API")
            return

        if not self.groq_api_key:
            print("GROQ_API_KEY not found for LangChain initialization")
            return

        try:
            print("Initializing LangChain with Groq...")
            
            # Initialize ChatGroq
            self.langchain_llm = ChatGroq(
                groq_api_key=self.groq_api_key,
                model_name=self.working_model,
                temperature=0.3,
                max_tokens=2000
            )

            # Test the connection
            test_message = HumanMessage(content="Hello, test connection")
            test_response = self.langchain_llm.invoke([test_message])
            
            if test_response:
                self.langchain_available = True
                self.llm_available = True
                print("LangChain with Groq initialized successfully!")
                print(f"Using model: {self.working_model}")
            else:
                print("LangChain test failed, falling back to direct Groq")

        except Exception as e:
            print(f"LangChain initialization failed: {e}")
            print("Falling back to direct Groq API")

    def _initialize_groq_fallback(self):
        """Initialize direct Groq client as fallback"""
        if not GROQ_AVAILABLE:
            print("Groq library not available, using template system")
            print("Install with: pip install groq")
            return

        if not self.groq_api_key:
            print("GROQ_API_KEY not found in environment variables")
            print("Falling back to template-based reports")
            return

        try:
            print("Initializing direct Groq API as fallback...")

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
                    if GROQ_AVAILABLE and self.groq_client:
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

            if test_successful and working_model:
                self.working_model = working_model
                self.llm_available = True
                print("Direct Groq API initialized successfully!")
                print(f"Using model: {working_model}")
            else:
                print("No working Groq models found, using template system")
                self.llm_available = False

        except Exception as e:
            print(f"Groq initialization failed: {e}")
            print("Falling back to template-based reports")
            self.llm_available = False

    def get_llm(self):
        """Get the initialized LLM (LangChain preferred, Groq fallback)"""
        if self.langchain_available:
            return self.langchain_llm
        elif self.llm_available:
            return self.groq_client
        else:
            return None

    def get_langchain_llm(self):
        """Get specifically the LangChain LLM"""
        return self.langchain_llm if self.langchain_available else None

    def is_available(self) -> bool:
        """Check if any LLM is available and working"""
        return self.langchain_available or self.llm_available

    def is_langchain_available(self) -> bool:
        """Check if LangChain is available"""
        return self.langchain_available

    def create_chain(self, template: str, input_variables: list = None):
        """Create a LangChain chain with a prompt template"""
        if not self.langchain_available:
            return None
            
        if input_variables is None:
            input_variables = ["input"]
            
        prompt = PromptTemplate(
            input_variables=input_variables,
            template=template
        )
        
        if LANGCHAIN_AVAILABLE and hasattr(self, 'langchain_llm'):
            chain = LLMChain(
                llm=self.langchain_llm,
                prompt=prompt
            )
            return chain
        return None

    async def run_chain(self, chain, **kwargs) -> str:
        """Run a LangChain chain asynchronously"""
        if not chain:
            raise Exception("Chain not available")
            
        try:
            # Check if arun method exists (newer versions)
            if hasattr(chain, 'arun'):
                result = await chain.arun(**kwargs)
            else:
                # Fallback to synchronous run
                import asyncio
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, lambda: chain.run(**kwargs))
            return result
        except Exception as e:
            raise Exception(f"Chain execution failed: {e}")

    async def generate_response(self, prompt: str) -> str:
        """Generate response using available LLM (LangChain preferred)"""
        
        # Try LangChain first
        if self.langchain_available:
            try:
                if LANGCHAIN_AVAILABLE and hasattr(self, 'langchain_llm'):
                    message = HumanMessage(content=prompt)
                    # Check if ainvoke exists (async)
                    if hasattr(self.langchain_llm, 'ainvoke'):
                        response = await self.langchain_llm.ainvoke([message])
                    else:
                        # Fallback to synchronous invoke
                        import asyncio
                        loop = asyncio.get_event_loop()
                        response = await loop.run_in_executor(None, lambda: self.langchain_llm.invoke([message]))
                    return response.content
            except Exception as e:
                print(f"LangChain failed, falling back to direct Groq: {e}")
        
        # Fallback to direct Groq API
        if self.llm_available and self.groq_client and self.working_model:
            try:
                import asyncio
                import concurrent.futures

                loop = asyncio.get_event_loop()

                def run_groq():
                    if GROQ_AVAILABLE and self.groq_client:
                        response = self.groq_client.chat.completions.create(
                            messages=[{"role": "user", "content": prompt}],
                            model=self.working_model,
                            max_tokens=2000,
                            temperature=0.3
                        )
                        return response.choices[0].message.content
                    return None

                result = await loop.run_in_executor(None, run_groq)
                return result or ""
            except Exception as e:
                raise Exception(f"Direct Groq API generation failed: {e}")
        
        raise Exception("No LLM available for response generation")


# Alias for backwards compatibility
GroqLLMManager = LLMManager
