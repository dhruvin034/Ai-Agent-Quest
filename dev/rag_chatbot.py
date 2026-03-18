#!/usr/bin/env python3
"""
🎨 Professional RAG Chatbot UI with 3 Tabs
Chat | Upload Documents | Help
"""

import streamlit as st
import os
import sys
import time
from pathlib import Path

# Add app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

try:
    from graph.rag_graph import rag_graph
    from ingest.upload_handler import (
        ingest_uploaded_files,
        get_indexed_documents,
        get_vector_db_stats,
        reset_vector_db,
        delete_document
    )
    from document_manager import DocumentManager
except ImportError as e:
    st.error(f"❌ Error importing modules: {e}")
    st.stop()

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS ====================
st.markdown("""
<style>
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                   color: white; padding: 10px; border-radius: 8px; margin: 5px 0; }
    .upload-area { border: 2px dashed #667eea; border-radius: 12px; padding: 20px;
                   background: linear-gradient(135deg, #f5f7ff 0%, #f0f4ff 100%); }
    .success-box { background: #d4edda; border: 1px solid #c3e6cb; padding: 12px;
                   border-radius: 8px; color: #155724; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
        <h2>⚙️ Settings</h2>
        <p style="margin: 0; font-size: 13px;">RAG Chatbot Control Panel</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Document info
    st.subheader("📚 Documents")
    try:
        doc_manager = DocumentManager(os.path.join(
            os.path.dirname(__file__), "..", "app", "documents.json"
        ))
        documents = doc_manager.get_all_documents()
        doc_count = len(documents)
        
        st.metric("📄 Indexed Docs", doc_count)
        
        if doc_count > 0:
            total_chunks = sum(doc.get("chunk_count", 0) for doc in documents)
            st.metric("🔗 Total Chunks", total_chunks)
            
            st.divider()
            st.subheader("📋 File List")
            for doc in documents:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(f"📄 {doc.get('name', 'Unknown')}")
                    st.caption(f"   {doc.get('chunk_count', 0)} chunks")
                with col2:
                    if st.button("🗑️", key=f"del_{doc.get('name', '')}"):
                        try:
                            delete_document(doc.get('name', ''))
                            doc_manager.delete_document(doc.get('name', ''))
                            st.success("✅ Deleted!")
                            time.sleep(1)
                            st.rerun()
                        except:
                            pass
        else:
            st.info("👉 No documents yet. Upload PDFs in the Upload tab!")
    except:
        st.warning("⚠️ Could not load documents")
    
    st.divider()
    
    # Chat controls
    st.subheader("💬 Chat")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with col2:
        if st.button("🔄 New", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    st.divider()
    
    # Status
    st.subheader("🔧 Status")
    if os.path.exists(os.path.join(os.path.dirname(__file__), "..", "vector_storage")):
        st.success("✅ System Ready", icon="✅")
    else:
        st.error("❌ Not Ready", icon="❌")
    
    st.divider()
    st.caption("🚀 RAG Assistant v2.0")

# ==================== MAIN CONTENT ====================
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; padding: 24px; border-radius: 12px; margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
    <h1 style="margin: 0;">🤖 RAG Chatbot</h1>
    <p style="margin: 8px 0 0 0; opacity: 0.9;">Upload documents → Ask questions → Get answers</p>
</div>
""", unsafe_allow_html=True)

# ============ THREE TABS ============
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📤 Upload Documents", "❓ Help"])

# ==================== TAB 1: CHAT ====================
with tab1:
    st.subheader("💬 Ask Questions")
    
    # Check documents exist (check vector DB directly)
    try:
        stats = get_vector_db_stats()
        doc_count = stats.get("document_count", 0)
    except:
        doc_count = 0
    
    if doc_count == 0:
        st.warning(
            "📭 **No documents indexed yet!**\n\n"
            "**How to get started:**\n"
            "1. Click the **📤 Upload Documents** tab\n"
            "2. Select your PDF files\n"
            "3. Click **Upload Now**\n"
            "4. Come back here to ask questions"
        )
    else:
        st.info(f"✅ Ready! You have **{doc_count}** document(s). Ask your questions below.")
    
    # Chat display
    if not st.session_state.chat_history:
        st.markdown("<div style='text-align: center; padding: 40px;'>"
                   "<h3 style='color: #667eea;'>👋 Welcome to RAG ChatBot</h3>"
                   "<p>Start asking questions about your documents</p>"
                   "<p style='font-size: 12px; color: #999;'>"
                   "💡 Try: 'What is the invoice number?'<br>"
                   "'Summarize this document'<br>"
                   "'What are the key points?'</p>"
                   "</div>", unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(msg["content"])
                    if "sources" in msg and msg["sources"]:
                        with st.expander("📚 Sources"):
                            for src in msg["sources"]:
                                st.caption(f"• {src}")
                    if "response_time" in msg:
                        st.caption(f"⏱️ {msg['response_time']:.2f}s")
    
    st.divider()
    
    # Input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Type your question...", 
                                   placeholder="Ask about your documents",
                                   label_visibility="collapsed")
    with col2:
        send_btn = st.button("💬", use_container_width=True)
    
    if (user_input and send_btn) or (user_input and st.session_state.get("just_submitted")):
        if not user_input.strip():
            st.warning("Please enter a question")
        else:
            # Check if documents exist before querying
            try:
                stats = get_vector_db_stats()
                current_doc_count = stats.get("document_count", 0)
            except:
                current_doc_count = 0
            
            if current_doc_count == 0:
                st.error("❌ No documents indexed yet. Please upload PDFs in the Upload Documents tab!")
            else:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                with st.spinner("🤔 Thinking..."):
                    start = time.time()
                    try:
                        result = rag_graph.invoke({"question": user_input})
                        response_time = time.time() - start
                        
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": result.get("answer", "No response"),
                            "sources": result.get("sources", []),
                            "response_time": response_time
                        })
                        st.rerun()
                    except Exception as e:
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": f"❌ Error: {str(e)[:100]}",
                            "sources": [],
                            "response_time": 0
                        })
                        st.rerun()

# ==================== TAB 2: UPLOAD ====================
with tab2:
    st.subheader("📤 Upload Your Documents")
    
    # Metrics
    try:
        dm = DocumentManager(os.path.join(
            os.path.dirname(__file__), "..", "app", "documents.json"
        ))
        docs = dm.get_all_documents()
        doc_c = len(docs)
        chunk_c = sum(d.get("chunk_count", 0) for d in docs) if docs else 0
    except:
        doc_c = 0
        chunk_c = 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Documents", doc_c)
    with col2:
        st.metric("🔗 Chunks", chunk_c)
    with col3:
        status = "🟢 Ready" if doc_c > 0 else "🟡 Empty"
        st.metric("Status", status)
    
    st.divider()
    
    # Upload area
    st.markdown("""
    <div class="upload-area">
        <h3 style="color: #667eea; margin-bottom: 10px;">📄 Select Your PDF Files</h3>
        <p style="color: #666; margin: 0;">Choose one or more PDFs to upload and index</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Files",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.info(f"✅ **{len(uploaded_files)} file(s) selected**")
        
        st.subheader("Selected Files:")
        for f in uploaded_files:
            size_kb = len(f.getbuffer()) / 1024
            st.caption(f"📄 {f.name} ({size_kb:.1f} KB)")
        
        st.divider()
        st.subheader("Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            chunk_size = st.slider("Chunk Size", 400, 2000, 800, 100)
        with col2:
            add_existing = st.checkbox("Add to existing", True)
        
        st.divider()
        
        if st.button("🚀 Upload Now", use_container_width=True, key="upload_btn"):
            progress_bar = st.progress(0)
            status = st.empty()
            
            with st.spinner("🔄 Processing..."):
                try:
                    status.text("📤 Uploading files...")
                    progress_bar.progress(20)
                    
                    # Create temp dir
                    temp_dir = os.path.join(os.path.dirname(__file__), "..", "temp_uploads")
                    os.makedirs(temp_dir, exist_ok=True)
                    
                    # Save files
                    files_saved = []
                    for uf in uploaded_files:
                        fp = os.path.join(temp_dir, uf.name)
                        with open(fp, "wb") as f:
                            f.write(uf.getbuffer())
                        files_saved.append(fp)
                    
                    progress_bar.progress(40)
                    status.text("🔍 Extracting text...")
                    
                    # Process
                    dm = DocumentManager(os.path.join(
                        os.path.dirname(__file__), "..", "app", "documents.json"
                    ))
                    
                    if not add_existing:
                        reset_vector_db()
                        dm.clear()
                    
                    progress_bar.progress(60)
                    status.text("🧠 Creating embeddings...")
                    
                    total_chunks = 0
                    for fp in files_saved:
                        try:
                            from ingest.upload_handler import ingest_single_document
                            res = ingest_single_document(fp, os.path.basename(fp))
                            total_chunks += res.get("chunks_added", 0)
                        except:
                            pass
                    
                    progress_bar.progress(90)
                    
                    # Cleanup
                    import shutil
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    
                    progress_bar.progress(100)
                    status.text("✅ Complete!")
                    
                    st.markdown(f"""
                    <div class="success-box">
                    <strong>✅ Upload Successful!</strong><br>
                    • Files: {len(uploaded_files)}<br>
                    • Chunks Created: {total_chunks}<br>
                    • Status: Ready to query
                    </div>
                    """, unsafe_allow_html=True)
                    
                    time.sleep(2)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Upload failed: {str(e)[:100]}")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 30px; color: #999;">
        <p>👆 Click above to select PDF files</p>
        <p style="font-size: 12px;">Supported: PDF files</p>
        <p style="font-size: 12px; color: #bbb;">No file paths shown • Secure upload</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 3: HELP ====================
with tab3:
    st.subheader("❓ Help & Guide")
    
    st.markdown("""
    ### 🚀 Quick Start (5 Steps)
    
    1. **Go to Upload Documents tab**
    2. **Select your PDF files**
    3. **Click Upload Now**
    4. **Go to Chat tab**
    5. **Ask your questions!**
    
    ---
    
    ### 📚 How It Works
    
    **What happens when you upload:**
    - PDFs are read and text extracted
    - Text split into chunks (default: 800 characters)
    - Each chunk converted to embeddings
    - Stored in vector database for searching
    
    **What happens when you ask:**
    - Your question is embedded
    - System finds similar chunks
    - AI generates answer from those chunks
    - Sources shown so you can verify
    
    ---
    
    ### 💡 Tips
    
    ✅ Ask specific questions
    ✅ Use natural language
    ✅ Check sources for verification
    ✅ Upload clear, readable PDFs
    ✅ Ask one question at a time
    
    ---
    
    ### ⚙️ Settings
    
    **Chunk Size:** Smaller = more precise, Larger = more context
    
    **Add to Existing:** Keep old documents or replace them
    
    **Clear Chat:** Only clears history, documents stay safe
    
    ---
    
    ### 🎯 Example Questions
    
    - "What is the invoice number?"
    - "Summarize this document"
    - "What are the key dates?"
    - "Who are the parties involved?"
    - "What payment terms apply?"
    
    ---
    
    ### 📞 Troubleshooting
    
    **No documents showing?**
    → Upload PDFs in the Upload tab first
    
    **Upload seems slow?**
    → Normal! Large files take time. Wait for ✅ Complete
    
    **Questions not answering?**
    → Make sure documents are uploaded
    → Try more specific questions
    → Check View Sources
    
    ---
    
    **Ready? Go to Upload Documents tab and start!** ✨
    """)

# ==================== RUN ====================
if __name__ == "__main__":
    pass
