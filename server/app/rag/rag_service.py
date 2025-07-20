"""
RAG Service - Main orchestration service for Retrieval Augmented Generation
"""
from typing import Dict, List
import os
from .llm_manager import LLMManager
from .vector_manager import VectorManager
from .policy_manager import PolicyManager
from .report_generator import ReportGenerator

# Tool imports for live data
try:
    from .tools import get_live_electricity_price_tool
    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False


class RAGService:
    """
    Main RAG service that orchestrates all components for report generation
    """

    def __init__(self):
        # Initialize paths
        self.vector_db_path = os.path.join(os.path.dirname(__file__), "..", "data", "vector_db")
        self.policy_docs_path = os.path.join(os.path.dirname(__file__), "..", "data", "policy_documents")

        # Initialize components
        self.llm_manager = LLMManager()
        self.vector_manager = VectorManager(self.vector_db_path)
        self.policy_manager = PolicyManager(self.policy_docs_path)
        self.report_generator = ReportGenerator()

        # Setup vector database with policy documents
        self._initialize_vector_database()

        print(f"SUCCESS: RAG service initialized (LLM: {'enabled' if self.llm_manager.is_available() else 'disabled'})")

    def _initialize_vector_database(self):
        """Initialize vector database with policy documents"""
        if not self.vector_manager.is_available():
            # Try to create vector database
            policy_documents = self.policy_manager.load_policy_documents()
            self.vector_manager.create_vectorstore(policy_documents)

    async def generate_feasibility_report(self, user_input: Dict, calculations: Dict) -> str:
        """
        Generate comprehensive feasibility report using RAG system
        """
        try:
            # Get relevant policy context
            query = f"Solar installation {user_input.get('location', 'Germany')} {calculations.get('system_capacity_kw', '')}kW"
            policy_context = self._retrieve_relevant_documents(query)
            
            # Generate report using LLM if available
            if self.llm_manager.is_available():
                prompt = f"Generate a solar feasibility report for: {user_input} with calculations: {calculations}"
                
                response = self.llm_manager.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.llm_manager.working_model,
                    max_tokens=2000,
                    temperature=0.7
                )
                
                return response.choices[0].message.content
            else:
                # Fallback to template-based report
                return f"Solar Feasibility Report\n\nSystem: {calculations.get('system_capacity_kw', 'N/A')}kW\nLocation: {user_input.get('location', 'N/A')}\n\nPolicy Context: {len(policy_context)} documents found."
                
        except Exception as e:
            print(f"ERROR: Report generation failed: {e}")
            return f"Error generating report: {e}"

    def _retrieve_relevant_documents(self, query: str, k: int = 3) -> List[str]:
        """Retrieve relevant documents from vector store"""
        try:
            if self.vector_manager.is_available():
                return self.vector_manager.similarity_search(query, k)
        except Exception:
            pass
        
        # Fallback to policy manager search
        return self.policy_manager.load_policy_documents()[:k]

    def get_live_price_fact(self, location: str = "Germany") -> str:
        """
        Get the latest electricity price for a location using tools
        """
        try:
            from app.core.electricity_price import get_electricity_price
            price = get_electricity_price()
            return f"The latest electricity price in {location} is €{price:.3f} per kWh."
        except Exception as e:
            return f"Unable to fetch electricity price: {e}"

    def get_policy_summary(self) -> Dict:
        """Get summary of available policy information"""
        return {"policy_documents": len(self.policy_manager.load_policy_documents())}

    def get_system_status(self) -> Dict:
        """Get status of all RAG components"""
        return {
            "llm_available": self.llm_manager.is_available(),
            "vector_db_available": self.vector_manager.is_available(),
            "policy_docs_loaded": len(self.policy_manager.load_policy_documents())
        }

    def refresh_policy_data(self):
        """Refresh policy data cache"""
        self.policy_manager._cached_documents = None
        self._initialize_vector_database()
