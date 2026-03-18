# 🤖 RAG Document Assistant

A professional Retrieval-Augmented Generation (RAG) system with a modern Streamlit interface for uploading PDF documents and asking AI-powered questions about them.

**Status:** ✅ Production Ready | **Version:** 2.0 | **Last Updated:** March 18, 2026

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [What is This?](#what-is-this)
3. [Features](#features)
4. [System Requirements](#system-requirements)
5. [Installation](#installation)
6. [How to Use](#how-to-use)
7. [Architecture](#architecture)
8. [File Structure](#file-structure)
9. [Configuration](#configuration)
10. [Troubleshooting](#troubleshooting)
11. [Examples](#examples)
12. [Advanced Usage](#advanced-usage)

---

## 🚀 Quick Start

### For Impatient Users (5 Minutes)

```bash
# 1. Navigate to project
cd d:\New Project

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Run setup (first time only)
python setup.py

# 4. Configure API key
# Edit .env file and add your OpenRouter API key:
OPENROUTER_API_KEY=your_key_here

# 5. Start the app
streamlit run dev/rag_chatbot.py

# 6. Open browser (automatic)
# http://localhost:8501
```

**Then:**
1. Go to **📤 Upload Documents** tab
2. Select your PDF files
3. Click **🚀 Upload Now**
4. Go to **💬 Chat** tab
5. Ask your questions!

---

## 📚 What is This?

This is a **Retrieval-Augmented Generation (RAG)** system that lets you:

- 📤 **Upload PDF documents** through a web interface
- 💬 **Ask questions** about those documents in natural language
- 🤖 **Get AI-powered answers** based on the actual document content
- 📍 **See sources** - know exactly where the answer came from
- ⚡ **Work in parallel** - upload documents while asking questions

### How It Works (Simple Explanation)

```
User Upload → PDF Processing → Vector Embeddings → Vector Database
                                                          ↓
                                                    Stored & Ready
                                                          ↓
User Question → Search Similar Content → Find Answer → AI Response
```

### Why RAG?

Instead of relying on an AI's training data (which may be outdated or hallucinated), RAG:
1. ✅ Finds relevant parts of your documents
2. ✅ Gives the AI model that content
3. ✅ Generates answers based only on your documents
4. ✅ Cites sources so you can verify

---

## ✨ Features

### 🎨 User Interface
- **3-Tab Design:** Chat | Upload Documents | Help
- **Modern HTML5 UI** with gradient colors
- **Real-time Progress** bars for file uploads
- **Document Sidebar** showing all indexed documents
- **Chat History** with response times and sources
- **Zero File Paths Shown** - professional, clean interface

### 📤 Document Upload
- ✅ Upload multiple PDFs at once
- ✅ Customizable chunk size (400-2000 characters)
- ✅ Progress tracking with status messages
- ✅ Add to existing documents or replace all
- ✅ Automatic chunk count calculation
- ✅ Success feedback with statistics

### 💬 Question Answering
- ✅ Ask questions in natural language
- ✅ Get AI-generated answers in 2-5 seconds
- ✅ View source citations (which document/page)
- ✅ See response time for each answer
- ✅ Continue conversation with chat history
- ✅ Clear/New Chat buttons for fresh starts

### ⚡ Parallel Processing
- ✅ Upload documents while asking questions
- ✅ No blocking between tabs
- ✅ Switch between tabs freely
- ✅ Upload continues in background
- ✅ Seamless multitasking

### 🔧 System Features
- ✅ Semantic search (understands meaning, not just keywords)
- ✅ Hybrid retrieval (vector + keyword search)
- ✅ Automatic document chunking
- ✅ Persistent vector database (survives restarts)
- ✅ Error recovery and graceful failures
- ✅ Comprehensive logging

---

## 💻 System Requirements

### Minimum Requirements
- **OS:** Windows 10+, macOS 10.14+, Linux
- **Python:** 3.8 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 2GB for dependencies + vector DB
- **Internet:** Required (for LLM API calls)

### Recommended Setup
- **Python:** 3.10 or 3.11
- **RAM:** 8GB+
- **Disk:** SSD (faster embedding generation)
- **Stable Internet:** For OpenRouter API

### Check Your Python Version
```bash
python --version
# Should show 3.8 or higher
```

---

## 📥 Installation

### Step 1: Clone/Download Project

```bash
# If cloning from git
git clone <repository-url>
cd "New Project"

# Or if manually downloaded, just navigate to folder
cd d:\New Project
```

### Step 2: Create Python Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# You should see (venv) in terminal prompt
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `streamlit` - Web interface framework
- `langchain` - LLM orchestration
- `chromadb` - Vector database
- `pypdf` - PDF reading
- `sentence-transformers` - Embeddings
- `openrouter` - LLM API
- And 10+ more dependencies

### Step 4: Run Setup Script (First Time Only)

```bash
python setup.py
```

**This does:**
- ✅ Creates necessary directories (data/, uploads/, vector_storage/, etc.)
- ✅ Checks dependencies are installed
- ✅ Creates .env template if missing
- ✅ Generates startup scripts
- ✅ Validates system setup

### Step 5: Configure API Key

**Get your API key:**
1. Go to https://openrouter.ai/
2. Sign up (free account)
3. Copy your API key

**Add to .env file:**
```bash
# Open .env file (in project root)
# Add this line:
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxx

# Save and close
```

### Step 6: Verify Installation

```bash
# Test everything works
streamlit run dev/rag_chatbot.py

# Should see:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
```

---

## 🎯 How to Use

### First Time Using the App?

**Follow these 5 steps:**

1. **Start the Application**
   ```bash
   streamlit run dev/rag_chatbot.py
   ```
   - Browser opens automatically at http://localhost:8501
   - You see the app with 3 tabs

2. **Go to Upload Documents Tab** (📤 tab)
   - Click the upload area
   - Select 1-3 PDF files
   - Watch file names and sizes appear

3. **Click Upload Now Button**
   - See progress bar: `[████░░░░░░] 50%`
   - Wait for: "✅ Complete!" message
   - See: "3 files, 847 chunks, Ready to query"

4. **Go to Chat Tab** (💬 tab)
   - See: "Ready! You have 3 documents"
   - Type a question: "What is the invoice number?"
   - Press Enter or click 💬 button

5. **Get Your Answer** (2-5 seconds)
   - See AI response: "The invoice number is INV-2024-001..."
   - Click [📚 View Sources] to see which document
   - See response time: [⏱️ 2.34s]

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────┐
│         STREAMLIT WEB INTERFACE             │
│  (dev/rag_chatbot.py - 3 tabs)             │
└────────────────┬────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
┌─────────────────┐   ┌──────────────────┐
│  UPLOAD PATH    │   │  CHAT PATH        │
├─────────────────┤   ├──────────────────┤
│ 1. File Upload  │   │ 1. Question      │
│ 2. PDF Loading  │   │ 2. Embedding     │
│ 3. Chunking     │   │ 3. Search        │
│ 4. Embedding    │   │ 4. Retrieve      │
│ 5. Vector DB    │   │ 5. Generate      │
└────────┬────────┘   │ 6. Verify        │
         │            │ 7. Format        │
         │            └────────┬─────────┘
         │                     │
         └──────────┬──────────┘
                    ▼
        ┌──────────────────────┐
        │ VECTOR DATABASE      │
        │ (Chroma - Local)     │
        ├──────────────────────┤
        │ • Embeddings         │
        │ • Chunks             │
        │ • Metadata           │
        │ • Search Index       │
        └──────────────────────┘
```

### Component Details

| Component | Purpose | Technology |
|-----------|---------|------------|
| **UI Layer** | Web interface | Streamlit (Python) |
| **Upload Handler** | PDF ingestion | PyPDFLoader + chunking |
| **Embedding** | Text to vectors | BAAI/bge-small-en-v1.5 |
| **Vector DB** | Store & search | Chroma (local) |
| **Retrieval** | Find relevant docs | Hybrid (vector + keyword) |
| **Generation** | Generate answers | OpenRouter LLM |
| **Verification** | Check hallucination | LLM verification |
| **Memory** | Chat history | JSON files |

### Data Flow

**Upload Flow:**
```
PDF File → Save to Temp → Load PDF → Extract Text → Split into Chunks
→ Generate Embeddings → Insert into Vector DB → Clean Temp → Show Success
```

**Query Flow:**
```
User Question → Embed Question → Search Vector DB → Retrieve Top Chunks
→ Send to LLM with Context → Generate Answer → Verify Answer → Format
→ Show with Sources and Timing
```

---

## 📂 File Structure

### Root Directory

```
d:\New Project\
│
├── README.md                              ← YOU ARE HERE
├── requirements.txt                       ← Dependencies list
├── setup.py                               ← First-time setup script
├── .env                                   ← API keys (NEVER commit)
├── .env.example                           ← Template
├── .gitignore                            ← Git ignore rules
│
├── app/                                  ← Core application
│   ├── main.py                          ← Entry point (if using CLI)
│   ├── documents.json                   ← Metadata tracking
│   ├── chat_memory.json                 ← Chat history
│   │
│   ├── ingest/                          ← PDF processing
│   │   ├── pdf_ingest.py               ← CLI ingestion
│   │   └── upload_handler.py           ← UI upload handling
│   │
│   ├── config/                          ← Configuration
│   │   ├── embeddings.py               ← Embedding model setup
│   │   └── llm.py                      ← LLM configuration
│   │
│   ├── graph/                           ← LangGraph pipeline
│   │   └── rag_graph.py                ← Main RAG pipeline
│   │
│   ├── rag/                             ← RAG components
│   │   ├── retriever.py                ← Search logic
│   │   ├── generator.py                ← Answer generation
│   │   ├── verifier.py                 ← Verification
│   │   ├── query_router.py             ← Classification
│   │   └── query_rewriter.py           ← Query enhancement
│   │
│   ├── tools/                           ← Tool definitions
│   │   ├── chat_tool.py                ← Chat responses
│   │   └── rag_tool.py                 ← Document Q&A
│   │
│   ├── memory/                          ← Memory management
│   │   └── chat_memory.py              ← Memory logic
│   │
│   └── document_manager.py              ← Metadata management
│
├── dev/                                 ← Development folder
│   ├── rag_chatbot.py                  ← ✨ MAIN APP (Streamlit UI)
│   ├── QUICKSTART.md                   ← Quick start guide
│   ├── SYSTEM_GUIDE.md                 ← Technical guide
│   ├── PARALLEL_WORKFLOW_GUIDE.md      ← Parallel operations
│   └── VISUAL_INTERFACE_GUIDE.md       ← Interface tutorial
│
├── vector_storage/                      ← Vector database (auto-created)
│   └── (Chroma database files)
│
├── temp_uploads/                        ← Temporary files (auto-created)
│   └── (Cleaned up after upload)
│
├── cursor/
│   └── .cursorrules                     ← Development guidelines
│
└── data/                                ← (Optional) Sample PDFs
    └── (Your sample documents)
```

### Key Files Explained

**dev/rag_chatbot.py** (Main Application)
- The Streamlit web interface
- All 3 tabs implemented here
- ~700 lines of code
- Start here if you want to modify the UI

**app/ingest/upload_handler.py** (Upload Logic)
- Handles PDF uploads from UI
- Processes files and adds to vector DB
- Called when user clicks "Upload Now"

**app/graph/rag_graph.py** (RAG Pipeline)
- Main question-answering logic
- Uses LangGraph for orchestration
- Called when user asks a question

**setup.py** (Setup Script)
- One-time initialization
- Creates directories
- Validates environment
- Generates startup scripts

---

## ⚙️ Configuration

### Environment Variables (.env file)

Create a `.env` file in the project root:

```bash
# LLM Configuration
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxx
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openrouter/meta-llama/llama-2-70b-chat  # Or other model

# Embedding Configuration
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
EMBEDDING_DEVICE=cpu  # or 'cuda' for GPU

# Vector Database
VECTOR_DB_PATH=./vector_storage
VECTOR_DB_TYPE=chroma

# Application Settings
CHUNK_SIZE=800
CHUNK_OVERLAP=150
MAX_CHUNKS_PER_QUERY=5
TEMPERATURE=0.2
```

### Customize LLM Models

**Available models on OpenRouter:**
- `openrouter/meta-llama/llama-2-70b-chat` - Free, fast
- `openrouter/openai/gpt-4` - Better quality
- `openrouter/anthropic/claude-3-opus` - Highest quality
- `openrouter/mistral/mistral-7b` - Very fast

**Change in .env:**
```bash
LLM_MODEL=openrouter/openai/gpt-4
```

### Adjust Chunk Size

**In .env:**
```bash
CHUNK_SIZE=800        # Smaller = more precise, Larger = more context
CHUNK_OVERLAP=150     # Overlap between chunks for continuity
```

- **400 characters:** Very precise, but may miss context
- **800 characters:** Good balance (default)
- **1200 characters:** More context, less precision

---

## 🐛 Troubleshooting

### "Vector DB is EMPTY" Error

**Problem:** You ask a question but get "No documents indexed yet"

**Solutions:**
1. Go to **📤 Upload Documents** tab
2. Select PDF files
3. Click **🚀 Upload Now**
4. Wait for "✅ Complete!" message
5. Go back to **💬 Chat** and try again

### Upload is Slow

**Normal behavior:**
- 100 KB PDF: 2-3 seconds
- 500 KB PDF: 8-12 seconds
- 1 MB PDF: 15-20 seconds

**Why?** Embedding generation takes time (creating vectors for AI)

**Solutions:**
- Wait for the progress bar to complete
- Try smaller PDFs first
- Larger PDFs are normal to take longer

### "API Key Invalid" Error

**Problem:** Questions fail with API key error

**Solution:**
1. Go to https://openrouter.ai/
2. Get your API key
3. Open `.env` file
4. Update `OPENROUTER_API_KEY=your_key`
5. Save file
6. Run `streamlit run dev/rag_chatbot.py` again

### App Won't Start

**Problem:** Error when running `streamlit run dev/rag_chatbot.py`

**Solutions:**
1. **Check Python version:**
   ```bash
   python --version
   # Should be 3.8 or higher
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Run setup again:**
   ```bash
   python setup.py
   ```

4. **Check active environment:**
   ```bash
   # Should show (venv) prefix in terminal
   which python  # macOS/Linux
   # or
   where python  # Windows
   ```

### Questions Don't Get Answered

**Problem:** Chat asks question but no answer comes back

**Check:**
1. ✅ Documents uploaded? (Check sidebar)
2. ✅ Sidebar shows documents? (If not, upload first)
3. ✅ API key valid? (Check .env)
4. ✅ Internet connected? (Required for LLM)

**Try:**
- Ask simpler question
- Check if document contains answer
- Click [📚 View Sources] to see what was found

### Files Not Showing After Upload

**Problem:** Uploaded files, but not visible in sidebar

**Solution:**
1. Refresh browser (F5)
2. Check if upload completed (progress bar 100%)
3. Check sidebar scrolls down (might be below fold)
4. Wait 2-3 seconds for sidebar to update

### Out of Memory Error

**Problem:** "MemoryError" or "CUDA out of memory"

**Solution:**
1. Close other applications
2. Reduce chunk size in .env:
   ```bash
   CHUNK_SIZE=600  # Smaller chunks
   ```
3. Restart app
4. Upload smaller PDFs first

---

## 📖 Examples

### Example 1: Upload and Query a Invoice

**Scenario:** You have `invoice.pdf` and want to know the total amount

**Steps:**
1. Open http://localhost:8501
2. Click **📤 Upload Documents** tab
3. Select `invoice.pdf`
4. Click **🚀 Upload Now**
5. Wait for success: "✅ 1 files, 15 chunks, Ready to query"
6. Click **💬 Chat** tab
7. Type: `What is the total amount due?`
8. Press Enter
9. Get answer: `The total amount due is $5,400.00`
10. Click **📚 View Sources** to see which page

### Example 2: Upload Multiple Documents

**Scenario:** You have contracts, invoices, and reports

**Steps:**
1. Go to **📤 Upload Documents**
2. Click upload area
3. Select multiple files:
   - contract.pdf
   - invoice.pdf
   - report.pdf
4. See: "✅ 3 file(s) ready"
5. Click **🚀 Upload Now**
6. Watch progress bar
7. Get success: "✅ 3 files, 847 chunks"
8. Go to **💬 Chat**
9. Ask: `Compare the payment terms across all documents`
10. AI searches all 3 files and summarizes

### Example 3: Parallel Upload & Query

**Scenario:** Upload new documents while reviewing old answers

**Steps:**
1. You're in **💬 Chat** tab with previous answer
2. You get new documents to upload
3. Click **📤 Upload Documents** tab
4. Upload new files (progress bar shows)
5. Click back to **💬 Chat** tab
6. Your old answer is still there!
7. Upload continues in background
8. After upload completes, ask new questions
9. New documents are immediately searchable

---

## 🔧 Advanced Usage

### Using from Command Line

**Ingest PDFs without UI:**
```bash
python -c "from app.ingest.pdf_ingest import ingest_documents; ingest_documents()"
```

This reads all PDFs from `data/` folder and indexes them.

### Access Vector Database Directly

```python
from app.config.embeddings import embeddings_model
from chromadb.config import Settings
import chromadb

# Connect to Chroma
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./vector_storage"
))

# Get collection
collection = client.get_collection("rag_documents")

# Query it
results = collection.query(
    query_embeddings=[[0.1, 0.2, ...]], # Your embedding
    n_results=5
)
```

### Customize LLM Temperature

In `.env`:
```bash
TEMPERATURE=0.3  # Lower = more factual, Higher = more creative
```

- 0.0 = Deterministic (same answer every time)
- 0.2 = Factual (best for document Q&A)
- 0.7 = Creative (good for chat)
- 1.0 = Very random

### Batch Upload PDFs

Keep PDFs in `data/` folder and run:

```bash
python dev/rag_chatbot.py

# Or from Python:
from app.ingest.pdf_ingest import ingest_documents
results = ingest_documents()
print(f"Indexed {results['total_chunks']} chunks")
```

### Check System Status

```python
from app.ingest.upload_handler import get_vector_db_stats

stats = get_vector_db_stats()
print(f"Documents: {stats['document_count']}")
print(f"Chunks: {stats['chunk_count']}")
print(f"Collections: {stats['collections']}")
```

### Clear Vector Database

**WARNING: This deletes all indexed documents!**

```bash
# From Python
from app.ingest.upload_handler import reset_vector_db
reset_vector_db()
print("Vector DB cleared!")

# Or delete folder
# rm -r vector_storage/  (Linux/Mac)
# rmdir /s vector_storage  (Windows)
```

---

## 📚 Additional Guides

After getting started, read these for deeper understanding:

- **[QUICKSTART.md](./dev/QUICKSTART.md)** - 5-minute setup guide
- **[SYSTEM_GUIDE.md](./dev/SYSTEM_GUIDE.md)** - Technical deep dive (500+ lines)
- **[PARALLEL_WORKFLOW_GUIDE.md](./dev/PARALLEL_WORKFLOW_GUIDE.md)** - How parallel operations work
- **[VISUAL_INTERFACE_GUIDE.md](./dev/VISUAL_INTERFACE_GUIDE.md)** - Interface walkthrough with screenshots
- **[CLEAN_INTERFACE_SUMMARY.txt](./CLEAN_INTERFACE_SUMMARY.txt)** - UI improvements summary

---

## 🤝 Support & Contributing

### Getting Help

1. Check [Troubleshooting](#troubleshooting) section above
2. Read the guides in `dev/` folder
3. Check error messages in terminal for specifics
4. Review browser console (F12) for JavaScript errors

### Reporting Issues

When reporting issues, include:
- Python version: `python --version`
- OS and version: Windows 10, macOS 12, etc.
- Error message (full text)
- Steps to reproduce
- Terminal output

### Contributing

To customize the system:

1. **UI Changes:** Edit `dev/rag_chatbot.py`
2. **RAG Logic:** Edit `app/graph/rag_graph.py`
3. **Retrieval:** Edit `app/rag/retriever.py`
4. **Prompts:** Edit `app/rag/generator.py`
5. **Memory:** Edit `app/memory/chat_memory.py`

See `.cursorrules` file for development guidelines.

---

## 📄 License & Attribution

This project uses:
- ✅ LangChain (Apache 2.0)
- ✅ Streamlit (Apache 2.0)
- ✅ Chroma (Apache 2.0)
- ✅ Sentence Transformers (Apache 2.0)
- ✅ PyPDF (BSD 3-Clause)

---

## 🎉 You're Ready!

You now have everything you need to:
- ✅ Install the system
- ✅ Upload documents
- ✅ Ask questions
- ✅ Get AI-powered answers
- ✅ Use parallel operations
- ✅ Customize behavior

**Start with:**
```bash
streamlit run dev/rag_chatbot.py
```

**Questions?** Check the guides in `dev/` folder or review [Troubleshooting](#troubleshooting).

**Happy document querying!** 🚀

---

## 📊 Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | Mar 18, 2026 | 3-tab Streamlit UI, parallel operations, path hiding |
| 1.5 | Mar 10, 2026 | Upload handler, document manager |
| 1.0 | Feb 20, 2026 | Initial RAG system |

---

**Last Updated:** March 18, 2026  
**Status:** ✅ Production Ready  
**Maintained By:** Your Team
