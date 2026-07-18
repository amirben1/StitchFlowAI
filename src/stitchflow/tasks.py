from crewai import Task
from src.stitchflow.agents import agent_erp, agent_trends, agent_market, agent_reporter

task_erp = Task(
    description="You need to analyze the ERP dataset located at 'data/mock_erp.json'. This file contains 200+ SKUs with historical sales data. Use the Execute Python Code tool to write a script that loads this JSON, calculates the sales velocity trend for the last 6 months for each SKU, and identifies which items are spiking exponentially (like a viral trend). Calculate the exact remaining budget and available capacity.",
    expected_output="A data-driven summary highlighting the fastest growing SKUs, mathematically calculated remaining budget, and available warehouse capacity.",
    agent=agent_erp
)

task_trends = Task(
    description="Analyze the trends dataset located at 'data/mock_digital_trends.json'. Then, use the Web Search tool to cross-reference the top trending styles (like 'Gorpcore' or 'Olive Cargo Pants') on the live internet to see if they are still relevant or dying out.",
    expected_output="A validated list of trends backed by both the internal dataset and live web search data.",
    agent=agent_trends
)

task_market = Task(
    description="Analyze the local market dataset located at 'data/mock_local_market.json'. Use the Execute Python Code tool to write a script that analyzes competitor pricing and stock status for the trending items identified in the trends data. Are our competitors sold out?",
    expected_output="A statistical summary of competitor stock-outs and pricing for trending items.",
    agent=agent_market
)

task_report = Task(
    description="Using the outputs from the previous tasks, write a highly structured, professional LaTeX document containing: Executive Summary, Recommended Procurement List (with exact quantities and estimated costs), Capacity Utilization Forecast, and Risk Assessment. The output MUST be a complete, valid LaTeX document starting with \\documentclass{article} and ending with \\end{document}. Do NOT wrap the output in markdown code blocks.",
    expected_output="A complete LaTeX formatted report.",
    agent=agent_reporter,
    context=[task_erp, task_trends, task_market]
)
