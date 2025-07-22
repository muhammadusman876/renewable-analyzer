"""
RAG Service - Main orchestration service for Retrieval Augmented Generation
Enhanced with LangChain support for structured LLM interactions
"""
from typing import Dict, List
import os
from .llm_manager import LLMManager
from .vector_manager import VectorManager
from .policy_manager import PolicyManager
from .report_generator import ReportGenerator
from .prompt_templates import (
    SOLAR_ANALYSIS_TEMPLATE,
    WEATHER_ANALYSIS_TEMPLATE,
    ROI_CALCULATION_TEMPLATE,
    POLICY_ANALYSIS_TEMPLATE,
    FEASIBILITY_REPORT_TEMPLATE
)

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
        Generate comprehensive feasibility report using RAG system with LangChain
        """
        try:
            # Get relevant policy context
            query = f"Solar installation {user_input.get('location', 'Germany')} {calculations.get('system_capacity_kw', '')}kW"
            policy_context = self._retrieve_relevant_documents(query)
            
            # Use LangChain if available, fallback to direct API
            if self.llm_manager.is_langchain_available():
                return await self._generate_with_langchain(user_input, calculations, policy_context)
            elif self.llm_manager.is_available():
                return await self._generate_with_direct_api(user_input, calculations, policy_context)
            else:
                # Fallback to template-based report
                return self._generate_template_report(user_input, calculations, policy_context)
                
        except Exception as e:
            print(f"ERROR: Report generation failed: {e}")
            return f"Solar Feasibility Report\n\nSystem: {calculations.get('system_capacity_kw', 'N/A')}kW\nLocation: {user_input.get('location', 'N/A')}\n\nError: {e}"

    async def _generate_with_langchain(self, user_input: Dict, calculations: Dict, policy_context: List[str]) -> str:
        """Generate report using LangChain structured approach"""
        try:
            # Create chain for feasibility analysis
            chain = self.llm_manager.create_chain(
                template=FEASIBILITY_REPORT_TEMPLATE,
                input_variables=[
                    "location", "system_size", "budget", "roof_area", 
                    "consumption", "technical_analysis", "financial_analysis"
                ]
            )
            
            if chain:
                # Prepare input data
                chain_input = {
                    "location": user_input.get('location', 'Germany'),
                    "system_size": calculations.get('system_capacity_kw', 0),
                    "budget": user_input.get('budget', 0),
                    "roof_area": user_input.get('roof_area', 0),
                    "consumption": user_input.get('household_consumption', 0),
                    "technical_analysis": self._format_technical_analysis(calculations),
                    "financial_analysis": self._format_financial_analysis(calculations)
                }
                
                # Run the chain
                result = await self.llm_manager.run_chain(chain, **chain_input)
                return result
            else:
                # Fallback if chain creation fails
                return await self._generate_with_direct_api(user_input, calculations, policy_context)
                
        except Exception as e:
            print(f"LangChain generation failed: {e}")
            return await self._generate_with_direct_api(user_input, calculations, policy_context)

    async def _generate_with_direct_api(self, user_input: Dict, calculations: Dict, policy_context: List[str]) -> str:
        """Generate report using direct API calls"""
        try:
            # Create structured prompt
            context_text = "\n".join(policy_context[:3]) if policy_context else "German renewable energy policies"
            prompt = f"""
            You are an expert solar energy consultant for the German market.

            Context: {context_text}

            Analysis Request:
            - Location: {user_input.get('location', 'Germany')}
            - Roof Area: {user_input.get('roof_area', 0)} m²
            - Budget: €{user_input.get('budget', 0)}
            - Annual Consumption: {user_input.get('household_consumption', 0)} kWh
            - System Size: {calculations.get('system_capacity_kw', 0)} kWp

            Provide a comprehensive feasibility analysis including:
            1. Technical assessment
            2. Financial analysis and ROI
            3. Risk factors
            4. Recommendations specific to German market

            Analysis:
            """
            
            # Generate response using the LLM manager's unified method
            response = await self.llm_manager.generate_response(prompt)
            return response
            
        except Exception as e:
            print(f"Direct API generation failed: {e}")
            return self._generate_template_report(user_input, calculations, policy_context)

    def _generate_template_report(self, user_input: Dict, calculations: Dict, policy_context: List[str]) -> str:
        """Generate basic template report as fallback"""
        return f"""
        Solar Feasibility Report

        Project Overview:
        - Location: {user_input.get('location', 'Germany')}
        - System Size: {calculations.get('system_capacity_kw', 'N/A')} kWp
        - Budget: €{user_input.get('budget', 'N/A')}
        - Roof Area: {user_input.get('roof_area', 'N/A')} m²

        Technical Analysis:
        Based on the provided parameters, this solar installation appears technically feasible.

        Financial Analysis:
        Investment analysis requires detailed calculations based on current market conditions.

        Recommendations:
        Consider local German regulations and current feed-in tariff rates.

        Policy Context: {len(policy_context)} relevant documents analyzed.
        """

    def _format_technical_analysis(self, calculations: Dict) -> str:
        """Format technical analysis data"""
        return f"""
        System Size: {calculations.get('system_capacity_kw', 0)} kWp
        Annual Production: {calculations.get('annual_production_kwh', 0)} kWh
        Capacity Factor: {calculations.get('capacity_factor', 0):.2f}%
        Solar Irradiance: {calculations.get('solar_irradiance', 0)} kWh/m²/year
        """

    def _format_financial_analysis(self, calculations: Dict) -> str:
        """Format financial analysis data"""
        return f"""
        Total Investment: €{calculations.get('total_cost', 0)}
        Annual Savings: €{calculations.get('annual_savings', 0)}
        Payback Period: {calculations.get('payback_period', 0)} years
        20-year NPV: €{calculations.get('npv_20_years', 0)}
        IRR: {calculations.get('irr', 0):.2f}%
        """

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
