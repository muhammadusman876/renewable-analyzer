"""
Vector Database Manager - Handles document embedding and retrieval
"""
from typing import List, Optional
import os

# LangChain vector store imports
try:
 from langchain.text_splitter import RecursiveCharacterTextSplitter
 from langchain_community.vectorstores import FAISS
 from langchain_community.embeddings import HuggingFaceEmbeddings
 LANGCHAIN_AVAILABLE = True
except ImportError as e:
 LANGCHAIN_AVAILABLE = False
 print(f"WARNING: LangChain not available for vector operations: {e}")


class VectorManager:
 """
 Manages vector database operations for document retrieval
 """

 def __init__(self, vector_db_path: str):
    self.vector_db_path = vector_db_path
    self.vectorstore = None
    self.embeddings = None
    self._initialize_embeddings()
    self._load_or_create_vectorstore()

 def _initialize_embeddings(self):
    """Initialize embedding model"""
    if not LANGCHAIN_AVAILABLE:
        print("WARNING: Vector database requires LangChain - using hardcoded documents")
        return

    try:
        self.embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("SUCCESS: Embeddings model initialized")
    except Exception as e:
        print(f"WARNING: Failed to initialize embeddings: {e}")

 def _load_or_create_vectorstore(self):
    """Load existing vectorstore or prepare for creation"""
    if not LANGCHAIN_AVAILABLE or not self.embeddings:
        return

    # Check if vector database exists
    if os.path.exists(os.path.join(self.vector_db_path, "index.faiss")):
        try:
            self.vectorstore = FAISS.load_local(self.vector_db_path, self.embeddings)
            print("SUCCESS: Loaded existing vector database")
            return
        except Exception as e:
            print(f"WARNING: Failed to load existing vector database: {e}")

            print("INFO: Vector database will be created when documents are added")

 def create_vectorstore(self, documents: List[str]) -> bool:
    """Create vector database from documents"""
    if not LANGCHAIN_AVAILABLE or not self.embeddings:
        print("WARNING: Cannot create vectorstore - LangChain not available")
        return False

    if not documents:
        print("WARNING: No documents provided for vectorstore creation")
        return False

    try:
        print(f"INFO: Creating vector database with {len(documents)} documents...")

        # Chunk documents for better retrieval
        chunked_docs = self._chunk_documents(documents)

        self.vectorstore = FAISS.from_texts(
        texts=chunked_docs,
        embedding=self.embeddings
        )

        # Save the vector database
        os.makedirs(self.vector_db_path, exist_ok=True)
        self.vectorstore.save_local(self.vector_db_path)
        print(f"SUCCESS: Vector database created and saved with {len(chunked_docs)} chunks")
        return True

    except Exception as e:
        print(f"WARNING: Vector database creation failed: {e}")
        return False

 def _chunk_documents(self, documents: List[str]) -> List[str]:
    """Split documents into chunks for better retrieval"""
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

        chunked_docs = []
        for doc in documents:
            chunks = text_splitter.split_text(doc)
            chunked_docs.extend(chunks)

        return chunked_docs
    except Exception as e:
        print(f"WARNING: Document chunking failed: {e}")
        return documents

 def similarity_search(self, query: str, k: int = 3) -> List[str]:
    """Search for similar documents"""
    if not self.vectorstore:
        print("WARNING: Vector database not available")
        return []

    try:
        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
    except Exception as e:
        print(f"WARNING: Document retrieval failed: {e}")
        return []

 def is_available(self) -> bool:
    """Check if vector database is available"""
    return self.vectorstore is not None

 def get_document_count(self) -> int:
    """Get number of documents in the vectorstore"""
    if not self.vectorstore:
        return 0

    try:
        return self.vectorstore.index.ntotal
    except:
        return 0
