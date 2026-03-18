# 📊 Performance Testing System - User Guide

Professional performance benchmarking system for your RAG agent with real-time metrics and Streamlit dashboard.

---

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Performance Tests
Generate fresh performance metrics:
```bash
python dev/RUN_PERFORMANCE_TESTS.py
```

### Step 3: View Results in Dashboard
Launch the professional interactive dashboard:
```bash
streamlit run dev/performance_dashboard.py
```

Then select your tab:
- **📊 Dashboard**: View key metrics and gauges
- **🧪 Run Tests**: Execute tests directly from UI
- **📈 Detailed Analysis**: Deep dive into performance data

---

## 📁 Files

### New Files
- ✅ `dev/performance_tester.py` - Dynamic test engine with real metrics calculation
- ✅ `dev/performance_dashboard.py` - Professional Streamlit dashboard
- ✅ `dev/RUN_PERFORMANCE_TESTS.py` - Command-line test runner (updated)

### Updated Files
- ✅ `requirements.txt` - Added: streamlit, plotly, pandas

---

## 🎯 Key Features

### ✅ Dynamic Metrics
- Tests executed **in REAL-TIME** against your RAG system
- Metrics calculated **AFTER each response**
- Results saved to `metrics_results.json`

### ✅ Comprehensive Testing
Measures across 5 dimensions:
- **Accuracy**: Quality of answers (0-100)
- **Hallucination Prevention**: Avoids false information (0-100)
- **Speed**: Response time in seconds
- **Source Citations**: Evidence-based answers (%)
- **Overall Score**: 1-10,000 scale

### ✅ Professional Dashboard
- Real-time metric cards with gauge charts
- Radar charts showing multi-dimensional performance
- Bar charts comparing dimensions
- Detailed performance breakdown by test
- Interactive data tables
- Performance trends visualization
- Automated insights and recommendations

---

## 📊 Scoring System

### How It Works
```
Final Score = Weighted combination of:
  - Accuracy (40% weight)
  - Hallucination Prevention (30% weight)
  - Speed (15% weight)
  - Source Citation Rate (15% weight)
```

### Grade Scale
| Grade | Score | Performance |
|-------|-------|-------------|
| **A+** | 90%+ | Excellent - Production ready |
| **A** | 80%+ | Very Good - High quality |
| **B** | 70%+ | Good - Acceptable performance |
| **C** | 60%+ | Fair - Needs work |
| **D** | 50%+ | Poor - Significant issues |
| **F** | <50% | Not Ready - Major problems |

---

## 📈 Test Metrics Explained

### Accuracy Score (0-100)
How well the system answers questions from documents.

**Scoring:**
- 75: Got some answer
- 85: Provided detailed answer
- 90: Answer backed with sources

**Example:**
```
Q: "What is the invoice number?"
A: "The invoice number is 870630" → 90/100 ✅ (has sources)
```

### Hallucination Prevention (0-100)
How well system avoids making false answers.

**Good vs. Bad Examples:**
```
Q: "What is the hourly rate?" (not in document)

✅ Good (85): "This information is not in the document"
❌ Bad (20): "The hourly rate is $75/hour" (false!)
```

### Speed Score (0-100)
Response time performance.

**Benchmarks:**
- 100 points: < 0.3 seconds (very fast)
- 95 points: 0.3-0.5 seconds
- 80 points: 0.5-2 seconds (ideal)
- 80 points: 2-3 seconds
- 40 points: > 5 seconds (slow)

### Source Citation Score (0-100)
Percentage of answers backed by document sources.

**Examples:**
- 100%: All answers have sources ✅
- 50%: Half of answers have sources ⚠️
- 0%: No sources provided ❌

### Overall Score (1-10,000)
Combined performance across all metrics.

```
Calculation:
(Accuracy×0.40 + Hallucination×0.30 + Speed×0.20 + Citations×0.10) × 100 = 1-10,000
```

---

## 🔧 Customizing Tests

To modify test queries, edit `get_test_queries()` in `dev/performance_tester.py`:

```python
def get_test_queries() -> List[Dict]:
    return [
        {
            "question": "What is the invoice number?",
            "expected_type": "document"
        },
        {
            "question": "What is AI?",
            "expected_type": "chat"
        },
        # Add more tests...
    ]
```

**expected_type values:**
- `"document"`: Question should be answered from PDFs
- `"chat"`: General knowledge question

---

## 📈 Reading the Dashboard

### Main Dashboard Tab

**1. KPIs (Key Performance Indicators)**
- Final Score: 0-10,000 overall rating
- Accuracy: Average correct answer rate
- Hallucination Prevention: Average honesty rate
- Speed: Average response time

**2. Performance Gauge**
- Visual 0-100% gauge
- Color coded: Red (0-50%), Yellow (50-70%), Green (70-100%)
- Shows current percentage

**3. Test Summary**
- Tests passed/total
- Source citation rate
- Response time range (min-max)

**4. Performance Charts**
- Radar chart: 5-dimension comparison
- Bar chart: Dimension breakdown

**5. Detailed Test Results**
- Individual test scores
- Response times
- Sources found
- Full answers

### Run Tests Tab

1. Click **"START PERFORMANCE TESTS"** button
2. Watch progress bar as tests execute
3. Review results immediately after completion
4. Dashboard updates automatically

### Detailed Analysis Tab

- **Metrics Summary**: All calculated metrics in table
- **Test Cases**: Individual test results
- **Performance Trends**: Response time visualization
- **Insights**: Strengths and improvement areas

---

## 💾 Output Data

### metrics_results.json

Contains complete test results:

```json
{
  "test_cases": [
    {
      "question": "What is the invoice number?",
      "answer": "The invoice number is 870630",
      "sources": ["page 1 of demo-invoice-20tax-8.pdf"],
      "metrics": {
        "accuracy": 90,
        "hallucination_prevention": 85,
        "speed": 80,
        "overall_score": 85.25
      }
    }
  ],
  "summary": {
    "final_score": 7350,
    "final_score_percentage": 73.5,
    "accuracy_avg": 87.5,
    "hallucination_prevention_avg": 84.2,
    "response_time_avg": 1.45,
    "source_citation_rate": 95.0
  }
}
```

---

## 🐛 Troubleshooting

### ERROR: "No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit plotly pandas
```

### ERROR: "No module named 'app'"
**Solution:** Make sure you're running from project root:
```bash
cd d:\Ai_Rag_Quest
python dev/RUN_PERFORMANCE_TESTS.py
```

### ERROR: "No vector database found"
**Solution:** Reindex PDFs first:
```bash
python dev/REINDEX_PDFS.py
```

### ERROR: "Dashboard loads but no data"
**Solution:** Run tests first:
```bash
python dev/RUN_PERFORMANCE_TESTS.py
```

### Dashboard is slow
**Solution:** Clear cache or use incognito mode:
```bash
streamlit run dev/performance_dashboard.py --logger.level=error
```

---

## 📚 Example Workflow

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate baseline metrics
```bash
python dev/RUN_PERFORMANCE_TESTS.py
```

**Output:**
```
✅ Tests completed successfully!
📊 Final Score: 7350 / 10,000 (73.5%)
Grade: B+ (Good)
```

### 3. View results in dashboard
```bash
streamlit run dev/performance_dashboard.py
```

Opens browser at: `http://localhost:8501`

### 4. Review insights
- ✅ Check KPIs
- ✅ Look at detailed metrics
- ✅ Read improvement recommendations
- ✅ Check individual test results

### 5. Iterate improvements
- Modify RAG system
- Run tests again
- Compare scores
- Track optimizations

---

## 🎯 Optimization Targets

### Current Status
**Before Fix:** Score 8.5/100 (F) - Had import errors ❌
**After Fix:** Dynamic, real-time metrics ✅

### Target Goals
- ✅ **Get to 70+** (B grade) - Good system
- ✅ **Get to 80+** (A grade) - Excellent  
- ✅ **Get to 90+** (A+ grade) - Production ready

### Areas to Optimize
| Area | Impact | How to Improve |
|------|--------|----------------|
| **Accuracy** | High | Better document retrieval, chunking strategy |
| **Hallucination** | High | Stronger verification, confidence thresholds |
| **Speed** | Medium | Vector DB optimization, caching |
| **Citations** | Medium | Better source extraction, metadata tracking |

---

## 📞 Architecture

### Performance Tester Module
- **DynamicPerformanceTester** class: Core testing engine
- **get_test_queries()**: Test case data
- Real-time metrics calculation after each query
- Automatic summary statistics
- JSON export for persistence

### Dashboard Module
- **Streamlit** for UI framework
- **Plotly** for interactive charts
- **Pandas** for data manipulation
- Multiple dashboard tabs for different views
- Auto-cache for performance

---

## 🔐 Data Privacy

All data is stored locally:
- `metrics_results.json` - Local file, never sent anywhere
- Dashboard runs on `localhost:8501` only
- No external API calls for metrics
- Complete privacy and control

---

## 📝 Notes

- Tests are **non-destructive** - no data is modified
- Safe to run multiple times
- Results are cumulative (new results overwrite old ones)
- All metrics are calculated in real-time
- Dashboard works offline (after data generated)

---

**Happy Testing! 🎉**
