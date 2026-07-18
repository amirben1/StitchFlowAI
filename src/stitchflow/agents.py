from crewai import Agent
from src.stitchflow.llm import llm
from src.stitchflow.tools import (
    ReadERPTool, 
    RunDigitalScraperTool, 
    ReadLocalMarketTool, 
    ExecutePythonTool, 
    WebSearchTool
)

# Instantiate Tools
erp_tool = ReadERPTool()
scraper_tool = RunDigitalScraperTool()
market_tool = ReadLocalMarketTool()
py_tool = ExecutePythonTool()
search_tool = WebSearchTool()

agent_erp = Agent(
    role="Inventory & Capacity Analyst",
    goal="Analyze internal ERP data to calculate exact remaining budget (TND), available warehouse space (m³), and current stock velocity to identify what apparel items need to be restocked or cleared.",
    backstory="You are an expert fashion retail logistics analyst managing physical warehouse constraints and capital for an apparel importer.",
    verbose=True,
    allow_delegation=False,
    tools=[erp_tool, py_tool],
    llm=llm
)

agent_trends = Agent(
    role="Global & Digital Fashion Trend Analyst",
    goal="Parse digital trend data to identify the top trending apparel styles, ranking them by engagement score and estimating lead times.",
    backstory="You are a data-driven fashion trend forecaster.",
    verbose=True,
    allow_delegation=False,
    tools=[scraper_tool, search_tool],
    llm=llm
)

agent_market = Agent(
    role="Local Market & Competitor Analyst",
    goal="Analyze local Tunisian fashion market data, including competitor pricing and customer feedback.",
    backstory="You are a competitive intelligence expert specializing in the Tunisian apparel and retail market.",
    verbose=True,
    allow_delegation=False,
    tools=[market_tool, search_tool],
    llm=llm
)

agent_reporter = Agent(
    role="Strategic Procurement & Capacity Reporter",
    goal="Synthesize the inputs from the Internal, Trend, and Local Market analysts to generate a final, actionable procurement list. Ensure recommendations strictly respect the available budget and warehouse capacity. Generate a complete, valid LaTeX document.",
    backstory="You are the Chief Procurement Orchestrator for an apparel brand. You make the final purchasing decisions based on hard data constraints. You output strictly in LaTeX format.",
    verbose=True,
    allow_delegation=False,
    tools=[py_tool],
    llm=llm
)
