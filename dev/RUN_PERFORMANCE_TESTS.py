#!/usr/bin/env python3
"""
🧪 PERFORMANCE TEST SUITE FOR RAG AGENT (DYNAMIC VERSION)

This script measures your agent's performance on a 1-10,000 scale
with REAL queries and DYNAMIC metrics calculation.

Usage:
    python dev/RUN_PERFORMANCE_TESTS.py

Output:
    - Performance metrics (accuracy, hallucination, speed, reliability)
    - Final score out of 10,000
    - Detailed breakdown with calculations
    - Results saved to: metrics_results.json

For Professional Streamlit Dashboard:
    streamlit run dev/performance_dashboard.py
"""

import os
import sys
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import the new dynamic tester
from performance_tester import DynamicPerformanceTester, get_test_queries


def main():
    """Run the performance test suite"""
    
    try:
        # Initialize tester
        tester = DynamicPerformanceTester()
        
        # Get test queries
        test_queries = get_test_queries()
        
        # Run complete test suite
        results = tester.run_test_suite(test_queries)
        
        # Save results
        output_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "metrics_results.json"
        )
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        print("\n" + "="*70)
        print("  📊 DASHBOARD AVAILABLE")
        print("="*70)
        print("\n🎨 To view results in professional dashboard, run:")
        print("   streamlit run dev/performance_dashboard.py\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
