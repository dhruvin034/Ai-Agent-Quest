#!/usr/bin/env python3
"""
🚀 RAG SYSTEM SETUP & INITIALIZATION
Professional setup guide for the Document Upload & Query System
"""

import os
import sys
import subprocess
from pathlib import Path


class RAGSystemSetup:
    """Setup and initialization for RAG system"""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.app_dir = os.path.join(self.project_root, "app")
        self.data_dir = os.path.join(self.project_root, "data")
        self.uploads_dir = os.path.join(self.project_root, "uploads")
        self.vector_db_dir = os.path.join(self.project_root, "vector_storage")
    
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def print_step(self, number: int, description: str):
        """Print step marker"""
        print(f"\n[{number}] {description}")
    
    def create_directories(self):
        """Create necessary directories"""
        self.print_step(1, "Creating directories...")
        
        directories = [
            self.data_dir,
            self.uploads_dir,
            self.vector_db_dir,
            os.path.join(self.project_root, "logs")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"    ✅ Created: {directory}")
    
    def check_dependencies(self):
        """Check required Python dependencies"""
        self.print_step(2, "Checking dependencies...")
        
        required_packages = {
            "streamlit": "streamlit>=1.32.0",
            "langchain": "langchain>=0.1.0",
            "langchain_community": "langchain-community>=0.0.10",
            "langchain_chroma": "langchain-chroma>=0.1.0",
            "langchain_huggingface": "langchain-huggingface>=0.0.0",
            "langchain_openai": "langchain-openai>=0.1.0",
            "langgraph": "langgraph>=0.0.30",
            "chromadb": "chromadb>=0.4.0",
            "pypdf": "pypdf>=3.0.0",
            "pydantic": "pydantic>=2.0.0",
            "python-dotenv": "python-dotenv>=1.0.0"
        }
        
        missing_packages = []
        
        for module_name, package_spec in required_packages.items():
            try:
                __import__(module_name)
                print(f"    ✅ {module_name}")
            except ImportError:
                print(f"    ❌ {module_name} - MISSING")
                missing_packages.append(package_spec)
        
        if missing_packages:
            self.print_step(2.1, "Installing missing packages...")
            for package in missing_packages:
                print(f"    Installing: {package}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("    ✅ All packages installed")
        else:
            print("\n    ✅ All dependencies satisfied")
    
    def create_env_file(self):
        """Create .env template if it doesn't exist"""
        self.print_step(3, "Checking environment configuration...")
        
        env_file = os.path.join(self.project_root, ".env")
        
        if os.path.exists(env_file):
            print("    ✅ .env file exists")
        else:
            print("    ⚠️  .env file not found")
            print("\n    Creating .env template...")
            
            env_content = """# LLM Configuration
OPENROUTER_API_KEY=your_api_key_here

# Optional: Hugging Face
HUGGINGFACE_API_KEY=your_hf_api_key_here

# Optional: Other LLM Providers
OPENAI_API_KEY=your_openai_key_here

# Vector DB Settings
VECTOR_DB_PATH=vector_storage
CHUNK_SIZE=800
CHUNK_OVERLAP=150

# System Settings
DEBUG_MODE=false
LOG_LEVEL=INFO
"""
            
            with open(env_file, 'w') as f:
                f.write(env_content)
            
            print(f"    📝 Created .env template at: {env_file}")
            print("    ⚠️  Please update with your API keys!")
    
    def create_sample_docs(self):
        """Create sample PDF for testing"""
        self.print_step(4, "Checking sample documents...")
        
        # Check if data directory has PDFs
        pdf_files = [f for f in os.listdir(self.data_dir) if f.endswith('.pdf')]
        
        if pdf_files:
            print(f"    ✅ Found {len(pdf_files)} PDF file(s) in data directory:")
            for pdf in pdf_files:
                file_path = os.path.join(self.data_dir, pdf)
                file_size = os.path.getsize(file_path) / 1024  # KB
                print(f"       • {pdf} ({file_size:.1f} KB)")
        else:
            print("    ℹ️  No PDFs found in data directory")
            print("    📌 Place your PDF files in: data/")
    
    def initialize_vector_db(self):
        """Initialize vector database"""
        self.print_step(5, "Initializing vector database...")
        
        if os.path.exists(self.vector_db_dir):
            print(f"    ✅ Vector DB directory exists: {self.vector_db_dir}")
        else:
            print(f"    📁 Vector DB will be created on first document upload")
    
    def create_startup_script(self):
        """Create startup scripts"""
        self.print_step(6, "Creating startup scripts...")
        
        # Windows startup script
        if sys.platform == "win32":
            startup_script = os.path.join(self.project_root, "run_chatbot.bat")
            
            batch_content = """@echo off
echo.
echo 🚀 Starting RAG Document Assistant...
echo.
cd /d "%~dp0"
streamlit run dev/rag_chatbot.py --logger.level=info
pause
"""
            
            with open(startup_script, 'w') as f:
                f.write(batch_content)
            
            print(f"    ✅ Created: {startup_script}")
        
        # Unix startup script
        if sys.platform != "win32":
            startup_script = os.path.join(self.project_root, "run_chatbot.sh")
            
            bash_content = """#!/bin/bash
echo "🚀 Starting RAG Document Assistant..."
cd "$(dirname "$0")"
streamlit run dev/rag_chatbot.py --logger.level=info
"""
            
            with open(startup_script, 'w') as f:
                f.write(bash_content)
            
            os.chmod(startup_script, 0o755)
            print(f"    ✅ Created: {startup_script}")
    
    def run_setup(self):
        """Run complete setup"""
        self.print_header("🚀 RAG SYSTEM INITIALIZATION")
        
        print("\nThis setup will configure your RAG Document Assistant system.")
        print("The system features:")
        print("  • 📤 Document upload from UI")
        print("  • 🔍 Intelligent document search")
        print("  • 🤖 AI-powered Q&A")
        print("  • 📚 Source citations")
        print("  • ⚡ Real-time processing")
        
        try:
            self.create_directories()
            self.check_dependencies()
            self.create_env_file()
            self.create_sample_docs()
            self.initialize_vector_db()
            self.create_startup_script()
            
            self.print_header("✅ SETUP COMPLETE")
            
            print("\n📝 NEXT STEPS:\n")
            print("1. 🔑 Configure API Keys:")
            print("   • Edit .env file with your OpenRouter API key")
            print("   • Get your key from: https://openrouter.ai/\n")
            
            print("2. 📄 Add Documents:")
            print(f"   • Place your PDF files in: {self.data_dir}/")
            print("   • Or upload files through the UI after starting\n")
            
            print("3. 🚀 Start the System:")
            if sys.platform == "win32":
                print("   • On Windows: Double-click run_chatbot.bat")
                print("   • Or in terminal: streamlit run dev/rag_chatbot.py")
            else:
                print("   • On Linux/Mac: ./run_chatbot.sh")
                print("   • Or in terminal: streamlit run dev/rag_chatbot.py")
            
            print("\n4. 💬 Use the System:")
            print("   • Upload PDF documents using the Upload tab")
            print("   • Ask questions in the Chat tab")
            print("   • View sources and citations\n")
            
            print("📚 SYSTEM STRUCTURE:\n")
            structure = f"""
            {self.project_root}/
            ├── app/                    # Application code
            │   ├── graph/             # RAG graph & routing
            │   ├── rag/               # RAG pipeline modules
            │   ├── ingest/            # Document ingestion
            │   │   ├── pdf_ingest.py
            │   │   └── upload_handler.py  ← NEW
            │   ├── config/            # Configuration
            │   ├── tools/             # RAG tools
            │   └── document_manager.py ← NEW
            │
            ├── dev/                   # Development & UI
            │   └── rag_chatbot.py    # Streamlit UI (UPDATED)
            │
            ├── data/                  # PDF documents
            ├── uploads/              # Uploaded files (CREATED)
            ├── vector_storage/       # Vector DB (CREATED)
            │
            ├── .env                  # API Keys
            └── run_chatbot.bat/sh    # Startup script (CREATED)
            """
            print(structure)
            
            print("🎯 KEY FEATURES:\n")
            print("✅ Upload documents from web UI")
            print("✅ Automatic PDF processing & chunking")
            print("✅ Dynamic vector database updates")
            print("✅ Context-aware Q&A system")
            print("✅ Source citations & verification")
            print("✅ Multi-document support")
            print("✅ Document management interface")
            print("✅ Real-time processing status\n")
            
        except Exception as e:
            self.print_header("❌ SETUP FAILED")
            print(f"\nError: {str(e)}")
            print("\nPlease fix the issue and run setup again.")
            sys.exit(1)


def main():
    """Main entry point"""
    setup = RAGSystemSetup()
    setup.run_setup()
    
    print("📧 For help, check the documentation or visit the How to Use tab in the app.\n")


if __name__ == "__main__":
    main()
