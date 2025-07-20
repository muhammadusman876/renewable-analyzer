"""
RAG (Retrieval Augmented Generation) System for Solar Energy Analysis

This module provides a modular RAG system for generating personalized solar energy
feasibility reports using LLM technology and vector databases.

Main Components:
- LLMManager: Handles LLM initialization and configuration
- VectorManager: Manages document embedding and retrieval
- PolicyManager: Handles policy document loading and context management
- ReportGenerator: Generates report templates and formatting
- RAGService: Main orchestration service
- EnergyRAGSystem: Simplified interface for backward compatibility
"""

from .llm_service import EnergyRAGSystem
from .rag_service import RAGService
from .llm_manager import LLMManager
from .vector_manager import VectorManager
from .policy_manager import PolicyManager
from .report_generator import ReportGenerator

__all__ = [
 'EnergyRAGSystem',
 'RAGService',
 'LLMManager',
 'VectorManager',
 'PolicyManager',
 'ReportGenerator'
]
