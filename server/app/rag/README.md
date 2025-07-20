# RAG System - Modular Architecture

This directory contains a modular RAG (Retrieval Augmented Generation) system for generating personalized solar energy feasibility reports. The system has been refactored into separate, focused modules for better maintainability and professional organization.

## 🏗️ Architecture Overview

```
rag/
├── __init__.py           # Module exports and initialization
├── llm_service.py        # 🔄 Main interface (backward compatibility)
├── rag_service.py        # 🎯 Main orchestration service
├── llm_manager.py        # 🤖 LLM initialization and management
├── vector_manager.py     # 📊 Vector database operations
├── policy_manager.py     # 📋 Policy document management
├── report_generator.py   # 📝 Report template generation
├── tools.py             # 🔧 Utility tools and functions
└── README.md            # 📖 This documentation
```

## 📁 Module Descriptions

### `llm_service.py` - Main Interface

- **Purpose**: Simplified interface for backward compatibility
- **Key Class**: `EnergyRAGSystem`
- **Function**: Delegates to the modular RAG service while maintaining existing API

### `rag_service.py` - Main Orchestration

- **Purpose**: Central orchestration of all RAG components
- **Key Class**: `RAGService`
- **Function**: Coordinates LLM, vector database, policy management, and report generation

### `llm_manager.py` - LLM Management

- **Purpose**: Handles LLM initialization and configuration
- **Key Class**: `LLMManager`
- **Features**:
  - Ollama LLM initialization
  - API key management
  - Connection testing
  - Async response generation

### `vector_manager.py` - Vector Database

- **Purpose**: Manages document embedding and retrieval
- **Key Class**: `VectorManager`
- **Features**:
  - FAISS vector database operations
  - Document chunking and embedding
  - Similarity search
  - Database persistence

### `policy_manager.py` - Policy Management

- **Purpose**: Handles German energy policy documents
- **Key Class**: `PolicyManager`
- **Features**:
  - Policy document loading from files
  - Hardcoded policy baselines
  - Document caching
  - Keyword-based search

### `report_generator.py` - Report Generation

- **Purpose**: Generates various types of reports
- **Key Class**: `ReportGenerator`
- **Features**:
  - LLM prompt template creation
  - Enhanced template reports with policy context
  - Basic fallback reports
  - Feasibility assessment logic

## 🚀 Usage Examples

### Basic Usage (Backward Compatible)

```python
from app.rag import EnergyRAGSystem

# Initialize the system
rag_system = EnergyRAGSystem()

# Generate a report
user_input = {
    'location': 'Munich',
    'roof_area': 50,
    'orientation': 'south'
}

calculations = {
    'annual_kwh': 8500,
    'total_investment': 15000,
    'annual_savings': 1200,
    'payback_period': 12.5,
    'roi_percentage': 8.0
}

report = await rag_system.generate_feasibility_report(user_input, calculations)
```

### Advanced Usage (Direct Module Access)

```python
from app.rag import RAGService, LLMManager, VectorManager

# Use specific components
llm_manager = LLMManager()
if llm_manager.is_available():
    response = await llm_manager.generate_response("Custom prompt")

# Or use the full service
rag_service = RAGService()
status = rag_service.get_system_status()
```

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Google Gemini API key for LLM services
- `OLLAMA_BASE_URL`: Optional Ollama server URL (defaults to localhost)

### File Paths

- Vector Database: `../data/vector_db/`
- Policy Documents: `../data/policy_documents/`

## 📊 Features

### LLM Integration

- ✅ Ollama LLM support with multiple fallback imports
- ✅ Automatic connection testing
- ✅ Graceful degradation to template mode
- ✅ Async response generation

### Vector Database

- ✅ FAISS-based semantic search
- ✅ Document chunking for optimal retrieval
- ✅ Automatic database creation and persistence
- ✅ Similarity search with configurable results

### Policy Management

- ✅ File-based policy document loading
- ✅ Hardcoded baseline German energy policies
- ✅ Document caching for performance
- ✅ Keyword-based policy search

### Report Generation

- ✅ Multiple report templates (basic, enhanced, LLM-powered)
- ✅ Automatic feasibility assessment
- ✅ Policy context integration
- ✅ Professional formatting with emojis and structure

## 🛠️ Maintenance

### Adding New Policy Documents

1. Place `.txt` or `.md` files in `../data/policy_documents/`
2. Call `rag_service.refresh_policy_data()` to rebuild vector database

### Updating Report Templates

- Modify methods in `ReportGenerator` class
- Templates support dynamic content injection
- Feasibility assessment logic can be customized

### LLM Configuration

- Update `LLMManager` for new LLM providers
- Modify temperature and model parameters as needed
- Add new prompt templates in `ReportGenerator`

## 🔍 Debugging

### System Status

```python
status = rag_service.get_system_status()
print(status)
# Output: {
#   'llm_available': True,
#   'vector_db_available': True,
#   'vector_db_documents': 15,
#   'policy_documents_loaded': 8,
#   'tools_available': True
# }
```

### Component Testing

```python
# Test LLM
llm_manager = LLMManager()
print(f"LLM Available: {llm_manager.is_available()}")

# Test Vector DB
vector_manager = VectorManager("path/to/db")
print(f"Vector DB Available: {vector_manager.is_available()}")
print(f"Document Count: {vector_manager.get_document_count()}")
```

## 📈 Performance

### Optimization Tips

- Vector database is loaded once and cached
- Policy documents are cached after first load
- LLM responses use connection pooling
- Template generation is fast fallback for all scenarios

### Memory Usage

- Vector embeddings: ~50MB for typical policy document set
- LLM model: Depends on Ollama configuration
- Policy cache: ~1MB for all German energy policies

## 🔒 Error Handling

The system implements graceful degradation:

1. **LLM Unavailable**: Falls back to enhanced templates
2. **Vector DB Failed**: Uses policy manager keyword search
3. **Policy Files Missing**: Uses hardcoded baseline policies
4. **Complete Failure**: Generates basic fallback report

Each component logs appropriate warnings and continues operation.

---

This modular architecture ensures the RAG system is maintainable, testable, and scalable while providing a clean separation of concerns.
