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

    Args:
    user_input: User's input parameters
    calculations: Results from solar and ROI calculations

    Returns:
    Formatted feasibility report
    """
    try:
        # Create search query for RAG
        location = user_input.get('location', 'Germany')
        system_size = calculations.get('system_capacity_kw', 0)

        search_query = f"solar panel installation {location} Germany {system_size}kW financing incentives"

        # Retrieve relevant context using RAG
        policy_context = self._retrieve_relevant_documents(search_query, k=5)

        if self.llm_manager.is_available():
            print("INFO: Generating LLM-powered report...")
            # Use LLM for personalized report generation
            prompt = self.report_generator.create_prompt_template(user_input, calculations, policy_context)
            report = await self.llm_manager.generate_response(prompt)

            # Add RAG indicator
            report += "\n\n---\n*This report was generated using AI with real-time policy data retrieval.*"
            return report
        else:
            print("INFO: Generating enhanced template report...")
            # Use enhanced template with RAG context
            report = self.report_generator.generate_enhanced_template_report(
            user_input, calculations, policy_context
            )
            return report

    except Exception as e:
        print(f"WARNING: Report generation failed: {e}")
        # Fallback to basic template
        return self.report_generator.generate_fallback_report(user_input, calculations, str(e))

 def _retrieve_relevant_documents(self, query: str, k: int = 3) -> List[str]:
    """Retrieve relevant documents from vector database or fallback to policy search"""
    # Try vector database first
    if self.vector_manager.is_available():
        print("DEBUG: Retrieving relevant documents from vector database...")
        docs = self.vector_manager.similarity_search(query, k=k)
        if docs:
            return docs

        print("INFO: Using policy manager search...")
        # Fallback to policy manager search
        return self.policy_manager.search_policy_context(query)

 def get_live_price_fact(self, location: str = "Germany") -> str:
    """
    Get the latest electricity price for a location using tools
    """
    if TOOLS_AVAILABLE:
        try:
            return get_live_electricity_price_tool.run(tool_input=location)
        except Exception:
            pass

    # Fallback to direct import
    try:
        from app.core.electricity_price import get_electricity_price
        price = get_electricity_price()
        return f"The latest electricity price in {location} is €{price:.3f} per kWh."
    except Exception as e:
        return f"Unable to fetch electricity price: {e}"

 def get_policy_summary(self) -> Dict:
    """Get summary of current German solar policies"""
    return self.policy_manager.get_policy_summary()

 def get_system_status(self) -> Dict:
    """Get status of all RAG system components"""
    return {
    "llm_available": self.llm_manager.is_available(),
    "vector_db_available": self.vector_manager.is_available(),
    "vector_db_documents": self.vector_manager.get_document_count(),
    "policy_documents_loaded": len(self.policy_manager.load_policy_documents()),
    "tools_available": TOOLS_AVAILABLE
    }

 def refresh_policy_data(self):
    """Refresh policy documents and rebuild vector database"""
    print("INFO: Refreshing policy data...")

    # Clear cached policy documents
    self.policy_manager.refresh_cache()

    # Reload documents and rebuild vector database
    policy_documents = self.policy_manager.load_policy_documents()
    success = self.vector_manager.create_vectorstore(policy_documents)

    if success:
        print("SUCCESS: Policy data refreshed successfully")
    else:
        print("WARNING: Policy data refresh completed with warnings")

    return success
