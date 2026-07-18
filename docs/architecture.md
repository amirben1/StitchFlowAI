# StitchFlow AI Architecture

This diagram illustrates the autonomous multi-agent pipeline and the flow of data from mocked internal/external sources to the final React Dashboard and LaTeX reports.

```mermaid
graph TD
    %% Styling
    classDef frontend fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#fff
    classDef agent fill:#1e1b4b,stroke:#8b5cf6,stroke-width:2px,color:#fff
    classDef data fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#fff
    classDef output fill:#450a0a,stroke:#ef4444,stroke-width:2px,color:#fff
    classDef core fill:#171717,stroke:#a3a3a3,stroke-width:2px,color:#fff

    %% Components
    subgraph Data Sources
        D1[(mock_erp.json)]:::data
        D2[(mock_local_market.json)]:::data
        D3[Live Web Search API]:::data
    end

    subgraph CrewAI Backend Swarm
        M[main.py Orchestrator]:::core
        A1[🤖 ERP Inventory Analyst<br/>Calculates Velocity & Budget]:::agent
        A2[🤖 Trend Analyst<br/>Validates Viral Micro-trends]:::agent
        A3[🤖 Local Market Analyst<br/>Detects Competitor Stock-outs]:::agent
        A4[🤖 Chief Reporter Agent<br/>Synthesizes Final Strategy]:::agent
    end

    subgraph Outputs
        O1[(dashboard/src/data.json)]:::output
        O2[docs/Procurement_Optimization_Report.pdf]:::output
    end

    subgraph User Interface
        UI[💻 React Dashboard<br/>Cold Luxury UI / Vite]:::frontend
    end

    %% Flow
    D1 -->|Historical Sales & Budget| A1
    D3 -->|Global Trends| A2
    D2 -->|Competitor Pricing| A3

    M -->|Delegates Task| A1
    A1 -->|SKU Candidates| A2
    A2 -->|Validated Trends| A3
    A3 -->|Market Gaps| A4

    A4 -->|Serializes JSON| O1
    A4 -->|Compiles LaTeX| O2

    O1 -->|Hot Module Reload| UI
    O2 -->|Executive Download| UI
```
