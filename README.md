# StitchFlowAI 🧵🤖

StitchFlowAI is an autonomous Multi-Agent System (MAS) built for fashion importers and retail logistics. It replaces traditional procurement guesswork with data-driven precision by orchestrating a team of AI agents that analyze your ERP data, cross-reference it with live global trends, and monitor competitor pricing. 

The AI pipeline is securely paired with a **Human-in-the-loop (HITL) 3D web dashboard** to ensure humans have final authorization over capital allocation.

## 🚀 Key Features

- **Autonomous Agent Team**: Built on CrewAI, orchestrating 4 distinct AI agents with specialized roles.
- **Advanced Social & Search Scraper (NEW!)**: A custom data ingestion pipeline that scrapes real-time sentiment and velocity data from **Google Trends, TikTok Trends, and YouTube** to validate fashion macro-trends before making decisions.
- **Python Code Execution**: Agents write and execute their own Python code (via an isolated subprocess) to run complex regressions and data analytics on large datasets.
- **Stunning 3D HITL Dashboard**: A cinematic, industrial-brutalist React dashboard built with `Three.js` and `React Three Fiber`. It features interactive scroll-driven 3D cloth simulations, cinematic bloom post-processing, and a Multi-Agent Intelligence Network view that exposes the underlying reasoning of the AI swarm.
- **Programmatic State Sync**: The AI agents seamlessly hand off their analysis as a structured JSON feed (`data.json`) to the React dashboard without tangling backend and frontend logic.
- **LaTeX PDF Generation**: For formal record-keeping, the Chief Reporter agent synthesizes the findings and autonomously writes and compiles a production-ready PDF report using `pdflatex`.
- **Custom OpenCode Adapter**: Built using LangChain to connect CrewAI to the `hy3-free` endpoint for cost-effective inference.

## 🏗️ Architecture

```text
StitchFlowAI/
├── dashboard/                # Human-in-the-Loop Vite/React 3D Web App
│   ├── src/App.tsx           # UI, Three.js canvas, and scroll animations
│   └── src/data.json         # Live AI Agent structured output feed
├── data/                     # Mock ERP and Competitor datasets
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
2. **Global Fashion Trend Analyst**: Ingests data from the Google/TikTok/YouTube scraper and uses the live internet to validate if a trend (e.g., Gorpcore, Y2K) is still growing or already dead.
3. **Local Market Analyst**: Uses Python to analyze local competitor pricing and out-of-stock rates to identify supply gaps in the market.
4. **Strategic Procurement Reporter**: The "boss" agent. It takes the output from the first 3 agents, decides what to buy, what to clearance, and formats the output into a strictly valid LaTeX document and a structured JSON payload for the web dashboard.

## 🛠️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/amirben1/StitchFlowAI.git
   cd StitchFlowAI
   ```

2. **Install Python Dependencies (AI Backend):**
   ```bash
   pip install crewai langchain-openai fpdf duckduckgo-search python-dotenv
   ```
   *Note: You also need `pdflatex` installed on your system to compile the PDF.*

3. **Install Node Dependencies (3D Dashboard):**
   ```bash
   cd dashboard
   npm install
   ```

4. **Configure Environment:**
   Create a `.env` file in the root directory:
   ```env
   OPENCODE_API_KEY=your_api_key_here
   ```

## 🎯 Usage

**1. Run the AI Procurement Pipeline:**
```bash
python main.py
```
*The agents will run their analysis, update `dashboard/src/data.json`, and output `Procurement_Optimization_Report.pdf`.*

**2. Launch the Web Dashboard for Authorization:**
```bash
cd dashboard
npm run dev
```
*Navigate to `http://localhost:5173` to interact with the scroll-driven 3D interface, view the Multi-Agent intelligence summaries, and authorize the final purchase orders.*

## 🏆 Built For
This project was built during an AI Hackathon to demonstrate the power of giving LLMs full agentic tools (Code Execution + Web Search + Cross-Platform Scraping) while maintaining strict human oversight through an ultra-premium, interactive 3D UI.
