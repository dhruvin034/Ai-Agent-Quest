#!/usr/bin/env python3
"""
🎨 PROFESSIONAL STREAMLIT PERFORMANCE DASHBOARD

Beautiful, real-time performance monitoring dashboard for the RAG system.
Shows metrics, charts, and detailed test results.

Usage:
    streamlit run dev/performance_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
import sys
from pathlib import Path

# Add app to path
app_path = os.path.join(os.path.dirname(__file__), "..", "app")
sys.path.insert(0, app_path)

from performance_tester import DynamicPerformanceTester, get_test_queries


# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="🧪 RAG Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
    .success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .info {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    </style>
""", unsafe_allow_html=True)


# ==================== SIDEBAR ====================
st.sidebar.title("⚙️ Performance Control")
st.sidebar.divider()

tab_mode = st.sidebar.radio(
    "Select Mode:",
    ["📊 Dashboard", "🧪 Run Tests", "📈 Detailed Analysis"]
)

# ==================== HELPER FUNCTIONS ====================

@st.cache_resource
def load_results():
    """Load previous test results"""
    results_file = Path(__file__).parent.parent / "metrics_results.json"
    if results_file.exists():
        with open(results_file, "r") as f:
            return json.load(f)
    return None


def get_grade(percentage):
    """Get letter grade for percentage"""
    if percentage >= 90:
        return "🏆 A+ (Excellent)"
    elif percentage >= 80:
        return "👏 A (Very Good)"
    elif percentage >= 70:
        return "✅ B (Good)"
    elif percentage >= 60:
        return "⚠️ C (Fair)"
    elif percentage >= 50:
        return "❌ D (Poor)"
    else:
        return "🔴 F (Not Ready)"


def metric_card(label, value, unit, status="info"):
    """Create a metric card"""
    col_style = "success" if status == "success" else "warning" if status == "warning" else "info"
    color_style = "color: #11998e;" if status == "success" else "color: #f5576c;" if status == "warning" else "color: #4facfe;"
    
    return f"""
    <div style="background: linear-gradient(135deg, {'#11998e' if status == 'success' else '#f5576c' if status == 'warning' else '#4facfe'} 0%, {'#38ef7d' if status == 'success' else '#f5576c' if status == 'warning' else '#00f2fe'} 100%); 
         padding: 20px; border-radius: 10px; color: white; text-align: center; margin: 10px 0;">
        <div style="font-size: 0.9em; opacity: 0.9;">{label}</div>
        <div style="font-size: 2.5em; font-weight: bold; margin: 10px 0;">{value}</div>
        <div style="font-size: 0.85em; opacity: 0.8;">{unit}</div>
    </div>
    """


# ==================== DASHBOARD MODE ====================
if tab_mode == "📊 Dashboard":
    st.title("🧪 RAG Agent Performance Dashboard")
    st.markdown("Real-time performance metrics and analysis of your RAG system")
    
    # Load results
    results = load_results()
    
    if results is None:
        st.warning("⚠️ No test results found. Please run tests first using the '🧪 Run Tests' tab.")
    else:
        summary = results.get("summary", {})
        test_cases = results.get("test_cases", [])
        
        # ==================== TOP METRICS ====================
        st.markdown("### 📈 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(metric_card(
                "🎯 Final Score",
                f"{summary.get('final_score', 0):.0f}",
                "/ 10,000",
                "success" if summary.get('final_score', 0) > 7000 else "warning"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(metric_card(
                "📊 Accuracy",
                f"{summary.get('accuracy_avg', 0):.1f}",
                "/ 100",
                "success" if summary.get('accuracy_avg', 0) > 80 else "warning"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(metric_card(
                "🛡️ Hallucination Prevention",
                f"{summary.get('hallucination_prevention_avg', 0):.1f}",
                "/ 100",
                "success" if summary.get('hallucination_prevention_avg', 0) > 80 else "warning"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(metric_card(
                "⚡ Speed",
                f"{summary.get('response_time_avg', 0):.2f}",
                "seconds avg",
                "success" if summary.get('response_time_avg', 0) < 2 else "warning"
            ), unsafe_allow_html=True)
        
        # ==================== GRADE & PERCENTAGE ====================
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            percentage = summary.get('final_score_percentage', 0)
            grade = get_grade(percentage)
            
            fig = go.Figure(data=[go.Indicator(
                mode="gauge+number+delta",
                value=percentage,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Overall Performance %"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "#f5576c"},
                        {'range': [50, 70], 'color': "#f093fb"},
                        {'range': [70, 85], 'color': "#ffd89b"},
                        {'range': [85, 100], 'color': "#38ef7d"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 70
                    }
                }
            )])
            
            fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"""
            ### 📊 Performance Grade: {grade}
            
            **Score: {summary.get('final_score', 0):.0f} / 10,000**
            
            **Percentage: {percentage:.2f}%**
            
            #### Test Summary:
            - ✅ Successful Tests: {summary.get('successful_tests', 0)}/{summary.get('total_tests', 0)}
            - 📚 Source Citation Rate: {summary.get('source_citation_rate', 0):.2f}%
            - ⏱️ Response Time (Min-Max): {summary.get('response_time_min', 0):.2f}s - {summary.get('response_time_max', 0):.2f}s
            """)
        
        # ==================== PERFORMANCE BREAKDOWN ====================
        st.divider()
        st.markdown("### 📊 Performance Breakdown by Dimension")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Radar chart
            categories = ['Accuracy', 'Hallucination\nPrevention', 'Speed', 'Citation Rate']
            values = [
                summary.get('accuracy_avg', 0),
                summary.get('hallucination_prevention_avg', 0),
                min((2.5 / max(summary.get('response_time_avg', 2.5), 0.1)) * 100, 100),  # Speed normalized
                summary.get('source_citation_rate', 0)
            ]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                marker=dict(color='rgba(102, 126, 234, 0.6)')
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                height=400,
                margin=dict(l=50, r=50, t=30, b=30)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar chart
            fig = go.Figure(data=[
                go.Bar(
                    name='Score',
                    x=categories,
                    y=values,
                    marker_color=['#667eea', '#764ba2', '#f093fb', '#11998e']
                )
            ])
            
            fig.update_layout(
                yaxis_title="Score (/100)",
                xaxis_title="Dimension",
                height=400,
                showlegend=False,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # ==================== TEST RESULTS TABLE ====================
        st.divider()
        st.markdown("### 📋 Detailed Test Results")
        
        # Create dataframe from test cases
        test_data = []
        for test in test_cases:
            if test.get("metrics", {}).get("success"):
                metrics = test["metrics"]
                test_data.append({
                    "Question": test["question"][:50] + "..." if len(test["question"]) > 50 else test["question"],
                    "Accuracy": f"{metrics.get('accuracy', 0):.0f}",
                    "Prevention": f"{metrics.get('hallucination_prevention', 0):.0f}",
                    "Speed (s)": f"{metrics.get('response_time_seconds', 0):.2f}",
                    "Overall": f"{metrics.get('overall_score', 0):.0f}",
                    "Sources": len(test.get("sources", [])),
                })
        
        if test_data:
            df = pd.DataFrame(test_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # ==================== TIMESTAMP ====================
        st.divider()
        st.caption(f"📅 Last Test Run: {results.get('timestamp', 'Unknown')}")


# ==================== RUN TESTS MODE ====================
elif tab_mode == "🧪 Run Tests":
    st.title("🧪 Run Performance Tests")
    st.markdown("Execute a comprehensive performance test suite on your RAG system")
    
    st.info("""
    This will run a series of performance tests against your RAG system:
    - ✅ Accuracy tests (answer quality)
    - 🛡️ Hallucination prevention (avoiding false answers)
    - ⚡ Speed tests (response time)
    - 📚 Source citation tests (evidence-based answers)
    """)
    
    if st.button("🚀 START PERFORMANCE TESTS", key="run_tests"):
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_container = st.container()
        
        try:
            # Initialize tester
            status_text.info("🔍 Initializing RAG system...")
            tester = DynamicPerformanceTester()
            
            if not tester.initialize_rag():
                st.error("❌ Failed to initialize RAG system")
                st.stop()
            
            # Get test queries
            test_queries = get_test_queries()
            
            # Run tests
            status_text.info(f"🚀 Running {len(test_queries)} test cases...")
            
            for i, test_query in enumerate(test_queries):
                progress = (i + 1) / len(test_queries)
                progress_bar.progress(progress)
                status_text.info(f"⏳ Running test {i+1}/{len(test_queries)}...")
                
                # Run the test
                result = tester.test_query(
                    test_query["question"],
                    test_query.get("expected_type", "document")
                )
                
                tester.results["test_cases"].append(result)
                
                if result.get("metrics", {}).get("success"):
                    metrics = result["metrics"]
                    tester.metrics["response_times"].append(metrics.get("response_time_seconds", 0))
                    tester.metrics["accuracy_scores"].append(metrics.get("accuracy", 0))
                    tester.metrics["hallucination_flags"].append(100 - metrics.get("hallucination_prevention", 0))
                    tester.metrics["relevance_scores"].append(metrics.get("overall_score", 0))
                    tester.metrics["source_citations"].append(1 if result.get("sources") else 0)
            
            # Calculate summary
            tester._calculate_summary()
            
            # Save results
            output_file = Path(__file__).parent.parent / "metrics_results.json"
            with open(output_file, "w") as f:
                json.dump(tester.results, f, indent=2)
            
            progress_bar.progress(1.0)
            status_text.success("✅ Tests completed successfully!")
            
            # Display results
            st.divider()
            st.success("### ✅ Test Results")
            
            summary = tester.results["summary"]
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🎯 Final Score", f"{summary.get('final_score', 0):.0f}/10000")
            col2.metric("📊 Accuracy Avg", f"{summary.get('accuracy_avg', 0):.1f}%")
            col3.metric("🛡️ Hallucination Prevention", f"{summary.get('hallucination_prevention_avg', 0):.1f}%")
            col4.metric("⚡ Response Time Avg", f"{summary.get('response_time_avg', 0):.2f}s")
            
            st.divider()
            st.info(f"📈 Overall Grade: {get_grade(summary.get('final_score_percentage', 0))}")
            st.info(f"💾 Results saved to: metrics_results.json")
            
            # Clear cache to reload dashboard
            st.cache_resource.clear()
            
        except Exception as e:
            st.error(f"❌ Error during testing: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


# ==================== DETAILED ANALYSIS MODE ====================
elif tab_mode == "📈 Detailed Analysis":
    st.title("📈 Detailed Performance Analysis")
    st.markdown("In-depth analysis of your RAG system's performance")
    
    results = load_results()
    
    if results is None:
        st.warning("⚠️ No test results found. Please run tests first.")
    else:
        summary = results.get("summary", {})
        test_cases = results.get("test_cases", [])
        
        # Tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Metrics", "🔍 Test Cases", "🎯 Trends", "💡 Insights"])
        
        with tab1:
            st.markdown("### Performance Metrics Summary")
            
            metrics_df = pd.DataFrame({
                "Metric": [
                    "Final Score",
                    "Accuracy Average",
                    "Hallucination Prevention",
                    "Response Time Average",
                    "Response Time Min",
                    "Response Time Max",
                    "Source Citation Rate",
                    "Success Rate"
                ],
                "Value": [
                    f"{summary.get('final_score', 0):.0f}/10000",
                    f"{summary.get('accuracy_avg', 0):.2f}%",
                    f"{summary.get('hallucination_prevention_avg', 0):.2f}%",
                    f"{summary.get('response_time_avg', 0):.2f}s",
                    f"{summary.get('response_time_min', 0):.2f}s",
                    f"{summary.get('response_time_max', 0):.2f}s",
                    f"{summary.get('source_citation_rate', 0):.2f}%",
                    f"{summary.get('successful_tests', 0)}/{summary.get('total_tests', 0)} ({(summary.get('successful_tests', 0) / max(summary.get('total_tests', 1), 1) * 100):.1f}%)"
                ]
            })
            
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        with tab2:
            st.markdown("### Individual Test Case Results")
            
            test_data = []
            for idx, test in enumerate(test_cases, 1):
                if test.get("metrics", {}).get("success"):
                    metrics = test["metrics"]
                    test_data.append({
                        "#": idx,
                        "Question": test["question"],
                        "Accuracy": f"{metrics.get('accuracy', 0):.0f}",
                        "Hallucination": f"{metrics.get('hallucination_prevention', 0):.0f}",
                        "Speed (s)": f"{metrics.get('response_time_seconds', 0):.3f}",
                        "Overall": f"{metrics.get('overall_score', 0):.0f}",
                        "Sources": len(test.get("sources", []))
                    })
            
            if test_data:
                df = pd.DataFrame(test_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        with tab3:
            st.markdown("### Performance Trends")
            
            # Extract response times for trend
            response_times = []
            for test in test_cases:
                if test.get("metrics", {}).get("success"):
                    response_times.append(test.get("metrics", {}).get("response_time_seconds", 0))
            
            if response_times:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    y=response_times,
                    mode='lines+markers',
                    name='Response Time',
                    line=dict(color='#667eea', width=2),
                    marker=dict(size=8)
                ))
                fig.update_layout(
                    title="Response Time Trend",
                    xaxis_title="Test #",
                    yaxis_title="Time (seconds)",
                    height=400,
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.markdown("### 💡 Performance Insights")
            
            percentage = summary.get('final_score_percentage', 0)
            accuracy = summary.get('accuracy_avg', 0)
            hallucination = summary.get('hallucination_prevention_avg', 0)
            response_time = summary.get('response_time_avg', 0)
            citation_rate = summary.get('source_citation_rate', 0)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ✅ Strengths")
                
                if hallucination > 85:
                    st.success("🛡️ Excellent hallucination prevention - system rarely makes up answers")
                
                if citation_rate > 80:
                    st.success("📚 Great source citation - system backs up answers with evidence")
                
                if response_time < 1.5:
                    st.success("⚡ Fast response times - system is quick and responsive")
                
                if accuracy > 85:
                    st.success("🎯 High accuracy - system gives correct answers")
            
            with col2:
                st.markdown("### 🔧 Areas for Improvement")
                
                if percentage < 70:
                    st.warning(f"📊 Overall score is {percentage:.1f}% - there's room for improvement")
                
                if accuracy < 70:
                    st.warning("🎯 Accuracy could be improved - consider expanding document collection")
                
                if hallucination < 70:
                    st.warning("🛡️ Hallucination rate is high - system may need better verification")
                
                if response_time > 3:
                    st.warning("⚡ Response times are slow - consider optimizing retriever")
                
                if citation_rate < 70:
                    st.warning("📚 Low source citation rate - improve document relevance")


# ==================== FOOTER ====================
st.divider()
st.markdown("""
---
**🧪 RAG Performance Dashboard** | Version 1.0
Built with Streamlit | Data-driven performance monitoring
""")
