# StitchFlowAI 🧵🤖

StitchFlowAI is an autonomous Multi-Agent System (MAS) built for fashion importers and retail logistics. It replaces traditional procurement guesswork with data-driven precision by orchestrating a team of AI agents that analyze your ERP data, cross-reference it with live global trends, and monitor competitor pricing.

## 🚀 Features

- **Autonomous Agent Team**: Built on CrewAI, orchestrating 4 distinct AI agents with specialized roles.
- **Python Code Execution**: Agents write and execute their own Python code (via an isolated subprocess) to run complex regressions and data analytics on large datasets.
- **Live Web Searching**: Agents use DuckDuckGo to browse the live internet and validate fashion trends in real-time before making procurement decisions.
- **LaTeX PDF Generation**: The Chief Reporter agent synthesizes the findings and autonomously writes and compiles a production-ready PDF report using `pdflatex`.
- **Custom OpenCode Adapter**: Built using LangChain to connect CrewAI to the `hy3-free` endpoint for cost-effective inference.

## 🏗️ Architecture

```text
StitchFlowAI/
├── data/                     # Mock ERP, Market, and Trend datasets
├── scripts/
│   └── generate_mock_data.py # Script to generate massive realistic datasets
├── src/
│   └── stitchflow/
│       ├── llm.py            # ChatOpenAI and LangChain adapter config
│       ├── tools.py          # ExecutePython, WebSearch, and JSON tools
│       ├── agents.py         # CrewAI Agent definitions
│       └── tasks.py          # CrewAI Task prompt engineering
└── main.py                   # The main orchestrator
```

## 🤖 The AI Crew

1. **Inventory & Capacity Analyst**: Writes Python scripts to parse massive ERP datasets, calculating Month-over-Month sales velocity and pinpointing exponential trends. It also strictly manages the physical warehouse constraints (m³) and the available capital (TND).
2. **Global Fashion Trend Analyst**: Parses digital trend data and uses the live internet to validate if a trend (e.g., Gorpcore, Y2K) is still growing or already dead.
3. **Local Market Analyst**: Uses Python to analyze local competitor pricing and out-of-stock rates to identify supply gaps in the market.
4. **Strategic Procurement Reporter**: The "boss" agent. It takes the output from the first 3 agents, decides what to buy, what to clearance, and formats the output into a strictly valid LaTeX document.

## 🛠️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/amirben1/StitchFlowAI.git
   cd StitchFlowAI
   ```

2. **Install Dependencies:**
   ```bash
   pip install crewai langchain-openai fpdf duckduckgo-search python-dotenv
   ```
   *Note: You also need `pdflatex` installed on your system to compile the PDF.*

3. **Configure Environment:**
   Create a `.env` file in the root directory:
   ```env
   OPENCODE_API_KEY=your_api_key_here
   ```

## 🎯 Usage

To trigger the autonomous procurement pipeline:
```bash
python main.py
```
*The agents will run their analysis and output `Procurement_Optimization_Report.pdf` in the root directory.*

To regenerate new complex mock data for testing:
```bash
python scripts/generate_mock_data.py
```

## 🏆 Built For
This project was built during an AI Hackathon to demonstrate the power of giving LLMs full agentic tools (Code Execution + Web Search) within a strict supply-chain constraint model.
