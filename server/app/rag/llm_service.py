"""
LLM Service - Simplified main interface for the RAG system
This file provides backward compatibility while using the new modular structure
"""
from typing import Dict
from .rag_service import RAGService


class EnergyRAGSystem:
 """
 RAG (Retrieval Augmented Generation) system for solar energy feasibility reports
 This is now a simplified interface that delegates to the modular RAG service
 """

 def __init__(self):
    # Initialize the RAG service which handles all components
    self.rag_service = RAGService()

    # Backward compatibility properties
    self.llm_available = self.rag_service.llm_manager.is_available()
    self.vectorstore = self.rag_service.vector_manager.vectorstore

    async def generate_feasibility_report(self, user_input: Dict, calculations: Dict) -> str:
        """
        Generate comprehensive feasibility report using RAG system

        Args:
        user_input: User's input parameters
        calculations: Results from solar and ROI calculations

        Returns:
        Formatted feasibility report
        """
        return await self.rag_service.generate_feasibility_report(user_input, calculations)

 def get_live_price_fact(self, location: str = "Germany") -> str:
    """
    Use the tool to get the latest electricity price for a location.
    """
    return self.rag_service.get_live_price_fact(location)

 def get_policy_summary(self) -> Dict:
    """Get summary of current German solar policies"""
    return self.rag_service.get_policy_summary()

 def get_system_status(self) -> Dict:
    """Get status of all RAG system components"""
    return self.rag_service.get_system_status()

 def refresh_policy_data(self):
    """Refresh policy documents and rebuild vector database"""
    return self.rag_service.refresh_policy_data()
