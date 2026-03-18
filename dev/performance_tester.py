#!/usr/bin/env python3
"""
🧪 DYNAMIC PERFORMANCE TEST MODULE FOR RAG AGENT

This module runs real performance tests against the RAG system
and calculates metrics dynamically based on actual responses.

Features:
- Real-time performance calculation
- Tracks: accuracy, speed, hallucination prevention, reliability
- Stores detailed results for dashboard visualization
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Tuple
import statistics

# Add app to path properly
app_path = os.path.join(os.path.dirname(__file__), "..", "app")
sys.path.insert(0, app_path)

try:
    from graph.rag_graph import rag_graph
    from ingest.pdf_ingest import ingest_documents
except ImportError as e:
    print(f"❌ Error importing RAG modules: {e}")
    sys.exit(1)


class DynamicPerformanceTester:
    """Dynamically test RAG agent performance with real queries and responses"""
    
    def __init__(self):
        self.results = {
            "test_cases": [],
            "summary": {},
            "timestamp": datetime.now().isoformat(),
        }
        self.metrics = {
            "response_times": [],
            "accuracy_scores": [],
            "hallucination_flags": [],
            "relevance_scores": [],
            "source_citations": [],
        }
    
    def initialize_rag(self):
        """Initialize RAG system"""
        print("🔍 Initializing RAG system...")
        vector_db_path = os.path.join(os.path.dirname(__file__), "..", "vector_storage")
        vector_db_path = os.path.abspath(vector_db_path)
        
        if not os.path.exists(vector_db_path):
            print(f"📥 Indexing PDF documents...")
            ingest_documents()
            print(f"✅ Vector DB created")
        else:
            print(f"✅ Vector DB found and loaded")
        
        return True
    
    def test_query(self, question: str, expected_type: str = "document") -> Dict:
        """
        Test a single query and measure performance
        
        expected_type: "document" (should find answer in PDFs) or "chat" (general knowledge)
        """
        print(f"\n📝 Testing: {question}")
        
        # Measure response time
        start_time = time.time()
        
        try:
            result = rag_graph.invoke({
                "question": question
            })
            
            response_time = time.time() - start_time
            
            # Extract results
            answer = result.get("answer", "")
            route = result.get("route", "unknown")
            sources = result.get("sources", [])
            
            # Calculate performance metrics
            test_result = {
                "question": question,
                "expected_type": expected_type,
                "answer": answer,
                "route": route,
                "sources": sources,
                "response_time": response_time,
                "timestamp": datetime.now().isoformat(),
            }
            
            # Calculate scores
            test_result["metrics"] = self._calculate_metrics(
                answer, 
                question, 
                sources, 
                response_time,
                expected_type,
                route
            )
            
            # Print results
            self._print_test_result(test_result)
            
            return test_result
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                "question": question,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "metrics": {"success": False}
            }
    
    def _calculate_metrics(self, answer: str, question: str, sources: list, 
                          response_time: float, expected_type: str, route: str) -> Dict:
        """Calculate performance metrics for a single query"""
        
        metrics = {}
        
        # 1. ACCURACY SCORE (0-100)
        accuracy = 0
        if answer and answer != "I don't know":
            accuracy = 75  # Got some answer
            if sources:
                accuracy = 90  # Has sources
            if len(answer) > 50:
                accuracy = 85  # Detailed answer
        
        metrics["accuracy"] = accuracy
        
        # 2. HALLUCINATION SCORE (0-100)
        # High score = low hallucination
        hallucination_score = 100
        
        hallucination_indicators = [
            "i don't have",
            "no relevant",
            "not found",
            "unable to",
            "cannot find",
        ]
        
        if any(indicator in answer.lower() for indicator in hallucination_indicators):
            hallucination_score = 85  # Honest about limitations
        elif "think" in answer.lower() or "maybe" in answer.lower():
            hallucination_score = 75
        elif not sources:
            hallucination_score = 60  # No sources = higher hallucination risk
        
        metrics["hallucination_prevention"] = hallucination_score
        
        # 3. SPEED SCORE (0-100)
        # Ideal response time: 0.5-2 seconds
        speed_score = 100
        if response_time > 5:
            speed_score = 40
        elif response_time > 3:
            speed_score = 60
        elif response_time > 2:
            speed_score = 80
        elif response_time < 0.3:
            speed_score = 95  # Very fast
        
        metrics["speed"] = speed_score
        metrics["response_time_seconds"] = round(response_time, 2)
        
        # 4. ROUTING ACCURACY
        routing_correct = True
        if expected_type == "document" and route != "rag":
            routing_correct = False
        elif expected_type == "chat" and route == "rag":
            if not sources:  # If no sources found for RAG, fallback to chat is OK
                routing_correct = True
        
        metrics["routing_correct"] = routing_correct
        
        # 5. SOURCE CITATION SCORE
        citation_score = 0
        if sources and len(sources) > 0:
            citation_score = 100
        elif not sources and route == "rag":
            citation_score = 40  # RAG route but no sources
        
        metrics["citation_score"] = citation_score
        
        # 6. OVERALL SUCCESS (0-100)
        overall = (
            accuracy * 0.30 +
            hallucination_score * 0.30 +
            speed_score * 0.20 +
            (100 if routing_correct else 0) * 0.10 +
            citation_score * 0.10
        )
        
        metrics["overall_score"] = round(overall, 2)
        metrics["success"] = True
        
        return metrics
    
    def _print_test_result(self, result: Dict):
        """Print formatted test result"""
        if result.get("error"):
            print(f"   ⚠️  Error: {result['error']}")
            return
        
        metrics = result.get("metrics", {})
        print(f"   ⏱️  Response Time: {metrics.get('response_time_seconds', 0)}s")
        print(f"   📊 Accuracy: {metrics.get('accuracy', 0)}/100")
        print(f"   🛡️  Hallucination Prevention: {metrics.get('hallucination_prevention', 0)}/100")
        print(f"   ⚡ Speed: {metrics.get('speed', 0)}/100")
        print(f"   📚 Sources: {len(result.get('sources', []))} found")
        print(f"   ✅ Overall Score: {metrics.get('overall_score', 0)}/100")
    
    def run_test_suite(self, test_queries: List[Dict]) -> Dict:
        """Run a complete test suite"""
        print("\n" + "="*70)
        print("  🧪 RAG AGENT PERFORMANCE TEST SUITE (DYNAMIC)")
        print("="*70)
        
        # Initialize RAG
        if not self.initialize_rag():
            print("❌ Failed to initialize RAG system")
            return {}
        
        print(f"\n🚀 Running {len(test_queries)} test cases...\n")
        
        # Run all tests
        for i, test_query in enumerate(test_queries, 1):
            print(f"\n[{i}/{len(test_queries)}] ACCURACY TEST SET")
            print("-" * 70)
            
            result = self.test_query(
                test_query["question"],
                test_query.get("expected_type", "document")
            )
            
            self.results["test_cases"].append(result)
            
            if result.get("metrics", {}).get("success"):
                metrics = result["metrics"]
                self.metrics["response_times"].append(metrics.get("response_time_seconds", 0))
                self.metrics["accuracy_scores"].append(metrics.get("accuracy", 0))
                self.metrics["hallucination_flags"].append(100 - metrics.get("hallucination_prevention", 0))
                self.metrics["relevance_scores"].append(metrics.get("overall_score", 0))
                self.metrics["source_citations"].append(1 if result.get("sources") else 0)
        
        # Calculate summary statistics
        self._calculate_summary()
        
        # Print summary
        self._print_summary()
        
        return self.results
    
    def _calculate_summary(self):
        """Calculate summary statistics"""
        summary = {}
        
        if self.metrics["accuracy_scores"]:
            summary["accuracy_avg"] = round(statistics.mean(self.metrics["accuracy_scores"]), 2)
            summary["accuracy_median"] = statistics.median(self.metrics["accuracy_scores"])
            
        if self.metrics["hallucination_flags"]:
            hallucination_rate = statistics.mean(self.metrics["hallucination_flags"])
            summary["hallucination_prevention_avg"] = round(100 - hallucination_rate, 2)
            
        if self.metrics["response_times"]:
            summary["response_time_avg"] = round(statistics.mean(self.metrics["response_times"]), 2)
            summary["response_time_min"] = round(min(self.metrics["response_times"]), 2)
            summary["response_time_max"] = round(max(self.metrics["response_times"]), 2)
            
        if self.metrics["relevance_scores"]:
            summary["overall_score_avg"] = round(statistics.mean(self.metrics["relevance_scores"]), 2)
            
        citation_rate = statistics.mean(self.metrics["source_citations"]) if self.metrics["source_citations"] else 0
        summary["source_citation_rate"] = round(citation_rate * 100, 2)
        
        # Calculate final performance score (0-10000 scale)
        # Normalize response time (ideal: <2s, max acceptable: 5s)
        response_time_avg = summary.get("response_time_avg", 0)
        if response_time_avg <= 2:
            response_time_score = 100
        elif response_time_avg >= 5:
            response_time_score = 0
        else:
            # Linear scale between 2-5s
            response_time_score = max(0, 100 - ((response_time_avg - 2) / 3) * 100)
        
        final_score = (
            (summary.get("accuracy_avg", 0) / 100) * 4000 +
            (response_time_score / 100) * 2000 +
            (summary.get("hallucination_prevention_avg", 0) / 100) * 3000 +
            (summary.get("source_citation_rate", 0) / 100) * 1000
        )
        
        # Cap final score at 10000 max
        final_score = min(final_score, 10000)
        
        summary["final_score"] = round(final_score, 0)
        summary["final_score_percentage"] = round((final_score / 10000) * 100, 2)
        summary["total_tests"] = len(self.results["test_cases"])
        summary["successful_tests"] = sum(1 for t in self.results["test_cases"] if t.get("metrics", {}).get("success"))
        
        self.results["summary"] = summary
    
    def _print_summary(self):
        """Print final summary"""
        summary = self.results["summary"]
        
        print("\n" + "="*70)
        print("  📊 FINAL PERFORMANCE ANALYSIS")
        print("="*70)
        
        print(f"\n✅ Tests Completed: {summary.get('successful_tests', 0)}/{summary.get('total_tests', 0)}")
        
        print(f"\n📈 METRICS SUMMARY:")
        print(f"   Accuracy Average:          {summary.get('accuracy_avg', 0):.2f}/100")
        print(f"   Hallucination Prevention:  {summary.get('hallucination_prevention_avg', 0):.2f}/100")
        print(f"   Response Time Average:     {summary.get('response_time_avg', 0):.2f}s")
        print(f"   Source Citation Rate:      {summary.get('source_citation_rate', 0):.2f}%")
        print(f"   Overall Score Average:     {summary.get('overall_score_avg', 0):.2f}/100")
        
        print(f"\n🎯 FINAL PERFORMANCE SCORE:")
        print(f"   Score: {summary.get('final_score', 0):.0f} / 10,000")
        print(f"   Percentage: {summary.get('final_score_percentage', 0):.2f}%")
        
        # Grade
        percentage = summary.get('final_score_percentage', 0)
        if percentage >= 90:
            grade = "A+ (Excellent)"
        elif percentage >= 80:
            grade = "A (Very Good)"
        elif percentage >= 70:
            grade = "B (Good)"
        elif percentage >= 60:
            grade = "C (Fair)"
        elif percentage >= 50:
            grade = "D (Poor)"
        else:
            grade = "F (Not Ready)"
        
        print(f"   Grade: {grade}")
        
        print("\n" + "="*70)


def get_test_queries() -> List[Dict]:
    """Get test queries for the RAG system"""
    return [
        {
            "question": "What is the invoice number in the document?",
            "expected_type": "document"
        },
        {
            "question": "What is the date on the invoice?",
            "expected_type": "document"
        },
        {
            "question": "What are the line items in the invoice?",
            "expected_type": "document"
        },
        {
            "question": "What is the total amount due?",
            "expected_type": "document"
        },
        {
            "question": "Can you explain what the document contains?",
            "expected_type": "document"
        },
        {
            "question": "What company issued this invoice?",
            "expected_type": "document"
        },
        {
            "question": "What is the tax amount?",
            "expected_type": "document"
        },
        {
            "question": "When was this invoice created?",
            "expected_type": "document"
        },
    ]


if __name__ == "__main__":
    tester = DynamicPerformanceTester()
    test_queries = get_test_queries()
    results = tester.run_test_suite(test_queries)
    
    # Save results
    output_file = os.path.join(
        os.path.dirname(__file__),
        "..",
        "metrics_results.json"
    )
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
