"""
📋 Document Management Module
Tracks and manages all uploaded documents with metadata
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Tuple
import hashlib


class DocumentManager:
    """Manages document metadata and tracking"""
    
    def __init__(self, metadata_path: str = None):
        if metadata_path is None:
            metadata_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "document_metadata.json"
            )
        self.metadata_path = os.path.abspath(metadata_path)
        self.ensure_metadata_file()
    
    def ensure_metadata_file(self):
        """Create metadata file if it doesn't exist"""
        if not os.path.exists(self.metadata_path):
            initial_data = {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "documents": [],
                "statistics": {
                    "total_uploaded": 0,
                    "total_ingested": 0,
                    "total_chunks": 0
                }
            }
            self.save(initial_data)
    
    def load(self) -> Dict:
        """Load metadata from file"""
        try:
            with open(self.metadata_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading metadata: {e}")
            return {"documents": [], "statistics": {}}
    
    def save(self, data: Dict):
        """Save metadata to file"""
        try:
            os.makedirs(os.path.dirname(self.metadata_path), exist_ok=True)
            with open(self.metadata_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving metadata: {e}")
    
    def add_document(self, filename: str, file_size: int, chunks: int) -> Dict:
        """Add a new document entry"""
        data = self.load()
        
        doc_id = len(data.get("documents", [])) + 1
        
        doc_entry = {
            "id": doc_id,
            "filename": filename,
            "file_size": file_size,
            "file_hash": self._hash_filename(filename),
            "chunks": chunks,
            "upload_date": datetime.now().isoformat(),
            "status": "indexed",
            "indexed_date": datetime.now().isoformat()
        }
        
        if "documents" not in data:
            data["documents"] = []
        
        data["documents"].append(doc_entry)
        
        # Update statistics
        if "statistics" not in data:
            data["statistics"] = {}
        
        data["statistics"]["total_uploaded"] = len(data["documents"])
        data["statistics"]["total_ingested"] = len([d for d in data["documents"] if d["status"] == "indexed"])
        data["statistics"]["total_chunks"] = sum(d.get("chunks", 0) for d in data["documents"])
        
        self.save(data)
        return doc_entry
    
    def get_all_documents(self) -> List[Dict]:
        """Get all indexed documents"""
        data = self.load()
        return data.get("documents", [])
    
    def get_document(self, filename: str) -> Dict or None:
        """Get a specific document by filename"""
        data = self.load()
        for doc in data.get("documents", []):
            if doc["filename"] == filename:
                return doc
        return None
    
    def update_document(self, filename: str, **kwargs) -> bool:
        """Update document metadata"""
        data = self.load()
        
        for doc in data.get("documents", []):
            if doc["filename"] == filename:
                doc.update(kwargs)
                if "updated_date" not in kwargs:
                    doc["updated_date"] = datetime.now().isoformat()
                self.save(data)
                return True
        
        return False
    
    def delete_document(self, filename: str) -> bool:
        """Delete a document from metadata"""
        data = self.load()
        
        initial_count = len(data.get("documents", []))
        data["documents"] = [d for d in data.get("documents", []) if d["filename"] != filename]
        
        if len(data["documents"]) < initial_count:
            # Update statistics
            if "statistics" in data:
                data["statistics"]["total_uploaded"] = len(data["documents"])
                data["statistics"]["total_ingested"] = len([d for d in data["documents"] if d["status"] == "indexed"])
                data["statistics"]["total_chunks"] = sum(d.get("chunks", 0) for d in data["documents"])
            
            self.save(data)
            return True
        
        return False
    
    def get_statistics(self) -> Dict:
        """Get document statistics"""
        data = self.load()
        
        docs = data.get("documents", [])
        
        stats = {
            "total_documents": len(docs),
            "total_chunks": sum(d.get("chunks", 0) for d in docs),
            "indexed_documents": len([d for d in docs if d["status"] == "indexed"]),
            "pending_documents": len([d for d in docs if d["status"] == "pending"]),
            "failed_documents": len([d for d in docs if d["status"] == "failed"]),
            "total_size_kb": sum(d.get("file_size", 0) for d in docs) / 1024,
            "average_chunks_per_doc": sum(d.get("chunks", 0) for d in docs) / len(docs) if docs else 0
        }
        
        return stats
    
    @staticmethod
    def _hash_filename(filename: str) -> str:
        """Generate hash for filename"""
        return hashlib.md5(filename.encode()).hexdigest()[:8]
    
    def export_report(self) -> str:
        """Generate a summary report"""
        data = self.load()
        stats = self.get_statistics()
        
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║              📊 DOCUMENT MANAGEMENT REPORT                     ║
╚════════════════════════════════════════════════════════════════╝

📈 STATISTICS:
  • Total Documents: {stats['total_documents']}
  • Total Chunks: {stats['total_chunks']}
  • Indexed Documents: {stats['indexed_documents']}
  • Pending Documents: {stats['pending_documents']}
  • Failed Documents: {stats['failed_documents']}
  • Total Size: {stats['total_size_kb']:.2f} KB
  • Avg Chunks/Doc: {stats['average_chunks_per_doc']:.1f}

📄 INDEXED DOCUMENTS:
"""
        
        for doc in data.get("documents", []):
            status_symbol = "✅" if doc["status"] == "indexed" else "⚠️" if doc["status"] == "pending" else "❌"
            report += f"\n  {status_symbol} {doc['filename']}"
            report += f"\n     └─ Chunks: {doc.get('chunks', 0)} | Size: {doc.get('file_size', 0)/1024:.1f} KB"
            report += f"\n     └─ Uploaded: {doc.get('upload_date', 'N/A')[:10]}"
        
        report += "\n\n" + "═" * 66 + "\n"
        
        return report


if __name__ == "__main__":
    # Test the manager
    manager = DocumentManager()
    
    print(manager.export_report())
    print(manager.get_statistics())
