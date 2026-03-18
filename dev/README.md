# 🔧 Development & Debugging Tools

This folder contains temporary scripts and utilities for development, testing, and debugging. These are **NOT** part of the production application.

---

## 📁 Contents

### **DEBUG_RAG.py** - System Diagnostics
**Purpose**: Check if the RAG pipeline is working correctly

**What it checks**:
- ✅ Are PDFs in `data/` folder?
- ✅ Is vector database initialized?
- ✅ Document count in vector DB
- ✅ Can retriever find documents?
- ✅ Is LLM API working?
- ✅ Query classification working?

**Usage**:
```bash
python dev/DEBUG_RAG.py
```

**Output**: Diagnostic report showing system health

**When to use**: When system isn't working as expected, start here

---

### **TEST_CLASSIFICATION.py** - Query Router Tests
**Purpose**: Test how the system classifies queries

**What it tests**:
- Document queries: "What is the invoice number?"
- Chat queries: "What is my name?"
- Edge cases: Ambiguous queries

**Usage**:
```bash
python dev/TEST_CLASSIFICATION.py
```

**Output**: Query classification results

**When to use**: After modifying query routing logic

---

### **REINDEX_PDFS.py** - Force Reindexing
**Purpose**: Recreate vector database from PDFs

**What it does**:
1. Deletes old vector_storage folder
2. Verifies PDFs exist
3. Loads and chunks all PDFs
4. Creates embeddings
5. Saves to Chroma DB

**Usage**:
```bash
python dev/REINDEX_PDFS.py
```

**When to use**: When vector DB is corrupted or empty

---

## 🚀 Development Workflow

### Fresh Installation Test
```bash
# 1. Run diagnostics
python dev/DEBUG_RAG.py

# 2. If empty, reindex
python dev/REINDEX_PDFS.py

# 3. Run the application
cd app
python main.py

# 4. Ask a test query
# Expected: "What is the invoice number?" → Finds document answer
```

### Testing Query Classification
```bash
python dev/TEST_CLASSIFICATION.py

# Check if routing decisions are correct:
# Document queries → route="rag"
# Chat queries → route="chat"
```

### Debugging Issues
```bash
# Step 1: Run diagnostic
python dev/DEBUG_RAG.py
# → Shows what's broken

# Step 2: Check output carefully
# Common issues:
#   - "Vector DB is EMPTY" → Run REINDEX_PDFS.py
#   - "LLM error" → Check OPENROUTER_API_KEY in .env
#   - "Classification error" → Check TEST_CLASSIFICATION.py

# Step 3: Fix issue
# - Add missing API key to .env
# - Verify PDFs exist in data/
# - Reindex if needed

# Step 4: Test again
python dev/DEBUG_RAG.py
```

---

## 📊 File Statistics

These scripts help with:
- ❌ **NOT** for production (use app/main.py instead)
- ✅ Development and testing
- ✅ Troubleshooting issues
- ✅ Verifying components
- ✅ Fresh installation validation

---

## 🔐 Security

These debug scripts are development-only and should:
- ❌ Not be committed in production
- ❌ Not be run in customer environments
- ✅ Only be used during development
- ✅ Be kept in `dev/` folder (separate from production)

---

## 📝 Notes

- All three scripts use the same imports as `app/main.py`
- They're helpful for understanding how components work
- Consider running `DEBUG_RAG.py` before submitting issues
- Keep these scripts for future maintenance

---

**Last Updated**: March 17, 2026  
**Status**: Development tools for testing & debugging
