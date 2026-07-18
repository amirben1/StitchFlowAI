# Multi-Agent Capacity Optimization System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python-based Multi-Agent System using CrewAI to automate procurement and capacity optimization for apparel importers.

**Architecture:** A 4-agent CrewAI system. Agents 1, 2, and 3 use custom JSON-parsing tools to gather context (Internal ERP, Digital Trends, Local Market). Agent 4 (Reporter) synthesizes this context into a markdown report, which is then converted to PDF using `fpdf2`.

**Tech Stack:** Python 3.10+, `crewai`, `langchain-google-genai`, `fpdf2`, `pydantic`.

## Global Constraints

- Language: Python 3.10+
- Agent Framework: crewai (latest version)
- LLM: google-generativeai (Gemini 1.5 Flash or Pro) via langchain-google-genai
- PDF Generation: fpdf2
- Data Handling: json, pydantic
- Robust error handling required in Custom Tools so missing files do not crash the agents.

---

### Task 1: Setup Directory and Data Mocks

**Files:**
- Create: `requirements.txt`
- Create: `data/mock_erp.json`
- Create: `data/mock_digital_trends.json`
- Create: `data/mock_local_market.json`

**Interfaces:**
- Produces: JSON files for tools to parse.

- [ ] **Step 1: Create requirements.txt**
```txt
crewai
langchain-google-genai
fpdf2
pydantic
```

- [ ] **Step 2: Create `data/mock_erp.json`**
```json
{
  "budget_tnd": 150000,
  "warehouse_capacity_m3": 500,
  "used_capacity_m3": 350,
  "inventory": [
    {"sku": "TSHIRT-BLK-M", "name": "Black T-Shirt M", "stock_level": 5, "velocity": "high", "volume_per_unit_m3": 0.005},
    {"sku": "JACKET-WIN-L", "name": "Winter Jacket L", "stock_level": 50, "velocity": "low", "volume_per_unit_m3": 0.02}
  ]
}
```

- [ ] **Step 3: Create `data/mock_digital_trends.json`**
```json
{
  "trends": [
    {"style_name": "Oversized Hoodies", "platform": "TikTok", "engagement_score": 95, "est_lead_time_days": 14, "est_cost_per_unit_tnd": 25},
    {"style_name": "Cargo Pants", "platform": "Instagram", "engagement_score": 88, "est_lead_time_days": 21, "est_cost_per_unit_tnd": 35}
  ]
}
```

- [ ] **Step 4: Create `data/mock_local_market.json`**
```json
{
  "competitors": [
    {"name": "Competitor A", "top_selling": "Oversized Hoodies", "price_tnd": 45, "stock_status": "Out of Stock"}
  ],
  "customer_feedback": [
    {"source": "Instagram Comments", "sentiment": "positive", "theme": "Looking for affordable cargo pants"}
  ]
}
```

- [ ] **Step 5: Commit**
```bash
git add requirements.txt data/
git commit -m "chore: setup dependencies and mock data"
```

---

### Task 2: Implement Custom Tools (tools.py)

**Files:**
- Create: `tools.py`
- Create: `tests/test_tools.py`

**Interfaces:**
- Consumes: The JSON files in `data/`
- Produces: `ReadERPTool`, `ReadTrendsTool`, `ReadLocalMarketTool` string outputs.

- [ ] **Step 1: Write the failing test**
```python
import os
import json
from tools import ReadERPTool, ReadTrendsTool, ReadLocalMarketTool

def test_tools_read_existing_files():
    assert "budget_tnd" in ReadERPTool()._run()
    assert "trends" in ReadTrendsTool()._run()
    assert "competitors" in ReadLocalMarketTool()._run()

def test_tools_handle_missing_files():
    # temporarily rename data dir to test error handling
    os.rename("data", "data_tmp")
    try:
        assert "Error" in ReadERPTool()._run()
    finally:
        os.rename("data_tmp", "data")
```

- [ ] **Step 2: Run test to verify it fails**
Run: `pytest tests/test_tools.py`
Expected: FAIL with "ModuleNotFoundError" or "ImportError".

- [ ] **Step 3: Write minimal implementation**
```python
import json
import os
from crewai.tools import BaseTool

class ReadERPTool(BaseTool):
    name: str = "Read ERP Data"
    description: str = "Reads internal ERP data regarding budget and capacity."
    
    def _run(self) -> str:
        filepath = "data/mock_erp.json"
        if not os.path.exists(filepath):
            return json.dumps({"Error": "mock_erp.json not found."})
        with open(filepath, 'r') as f:
            return f.read()

class ReadTrendsTool(BaseTool):
    name: str = "Read Digital Trends Data"
    description: str = "Reads digital fashion trends data."
    
    def _run(self) -> str:
        filepath = "data/mock_digital_trends.json"
        if not os.path.exists(filepath):
            return json.dumps({"Error": "mock_digital_trends.json not found."})
        with open(filepath, 'r') as f:
            return f.read()

class ReadLocalMarketTool(BaseTool):
    name: str = "Read Local Market Data"
    description: str = "Reads local market and competitor data."
    
    def _run(self) -> str:
        filepath = "data/mock_local_market.json"
        if not os.path.exists(filepath):
            return json.dumps({"Error": "mock_local_market.json not found."})
        with open(filepath, 'r') as f:
            return f.read()
```

- [ ] **Step 4: Run test to verify it passes**
Run: `pytest tests/test_tools.py`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add tools.py tests/test_tools.py
git commit -m "feat: implement JSON parsing tools with error handling"
```

---

### Task 3: Implement Main Orchestration and PDF Generation (main.py)

**Files:**
- Create: `main.py`

**Interfaces:**
- Consumes: `tools.py` (Custom tools), `langchain_google_genai`, `fpdf2`
- Produces: `Procurement_Optimization_Report.pdf` in root dir.

- [ ] **Step 1: Write minimal implementation**
```python
import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import ReadERPTool, ReadTrendsTool, ReadLocalMarketTool
from fpdf import FPDF
import re

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Instantiate Tools
erp_tool = ReadERPTool()
trends_tool = ReadTrendsTool()
market_tool = ReadLocalMarketTool()

# Define Agents
agent_erp = Agent(
    role="Inventory & Capacity Analyst",
    goal="Analyze internal ERP data to calculate exact remaining budget (TND), available warehouse space (m³), and current stock velocity to identify what needs to be restocked or cleared.",
    backstory="You are an expert logistics analyst managing physical warehouse constraints and capital.",
    verbose=True,
    allow_delegation=False,
    tools=[erp_tool],
    llm=llm
)

agent_trends = Agent(
    role="Global & Digital Fashion Trend Analyst",
    goal="Parse digital trend data to identify the top trending apparel styles, ranking them by engagement score and estimating lead times.",
    backstory="You are a data-driven fashion trend forecaster.",
    verbose=True,
    allow_delegation=False,
    tools=[trends_tool],
    llm=llm
)

agent_market = Agent(
    role="Local Market & Competitor Analyst",
    goal="Analyze local Tunisian market data, including competitor pricing, customer feedback, and regional demand spikes.",
    backstory="You are a competitive intelligence expert specializing in the Tunisian retail market.",
    verbose=True,
    allow_delegation=False,
    tools=[market_tool],
    llm=llm
)

agent_reporter = Agent(
    role="Strategic Procurement & Capacity Reporter",
    goal="Synthesize the inputs from the Internal, Trend, and Local Market analysts to generate a final, actionable procurement list. Ensure recommendations strictly respect the available budget and warehouse capacity. Generate a markdown report.",
    backstory="You are the Chief Procurement Orchestrator. You make the final purchasing decisions based on hard data constraints.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define Tasks
task_erp = Task(
    description="Use your tool to read the ERP data. Extract remaining budget, capacity, and stock velocity.",
    expected_output="A structured summary of available capacity, budget, and high/low performing SKUs.",
    agent=agent_erp
)

task_trends = Task(
    description="Use your tool to read the digital trends data. Rank the styles by engagement and note lead times.",
    expected_output="A ranked list of trending styles with engagement metrics and lead times.",
    agent=agent_trends
)

task_market = Task(
    description="Use your tool to read the local market data. Extract competitor pricing and customer sentiment.",
    expected_output="A summary of local competitor moves, customer sentiment, and localized demand trends.",
    agent=agent_market
)

task_report = Task(
    description="Using the context from the previous tasks, write a highly structured, professional markdown report containing: Executive Summary, Recommended Procurement List (with quantities and estimated costs), Capacity Utilization Forecast, and Risk Assessment. MUST be in markdown.",
    expected_output="A complete Markdown formatted report.",
    agent=agent_reporter,
    context=[task_erp, task_trends, task_market]
)

# Crew
crew = Crew(
    agents=[agent_erp, agent_trends, agent_market, agent_reporter],
    tasks=[task_erp, task_trends, task_market, task_report],
    process=Process.sequential
)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Procurement Optimization Report', 0, 1, 'C')
        self.ln(10)

def markdown_to_pdf(markdown_text, filename="Procurement_Optimization_Report.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Strip basic markdown for FPDF compatibility
    lines = markdown_text.split('\n')
    for line in lines:
        clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line) # Remove bold
        clean_line = re.sub(r'\*(.*?)\*', r'\1', clean_line) # Remove italic
        clean_line = re.sub(r'#+\s(.*)', r'\1', clean_line) # Remove headers
        clean_line = clean_line.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, txt=clean_line)
    pdf.output(filename)

if __name__ == "__main__":
    result = crew.kickoff()
    markdown_output = str(result)
    print("Crew finished. Generating PDF...")
    markdown_to_pdf(markdown_output)
    print("PDF Generated successfully.")
```

- [ ] **Step 2: Run application to verify**
Run: `python main.py`
Expected: Agents execute, console shows thinking, and `Procurement_Optimization_Report.pdf` is generated.

- [ ] **Step 3: Commit**
```bash
git add main.py
git commit -m "feat: implement CrewAI agents, tasks, and PDF generation"
```
