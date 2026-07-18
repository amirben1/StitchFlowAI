import os
from crewai import Agent, Task, Crew, Process
from crewai.llms.base_llm import BaseLLM
from langchain_openai import ChatOpenAI
from tools import ReadERPTool, ReadTrendsTool, ReadLocalMarketTool, ExecutePythonTool, WebSearchTool
from fpdf import FPDF
import re
from typing import Any

# Adapter to pass LangChain models to CrewAI v1.15.4
class CrewAILangChainAdapter(BaseLLM):
    llm: Any
    
    def call(self, messages, *args, **kwargs):
        response = self.llm.invoke(messages)
        return response.content

# Initialize LLM
langchain_llm = ChatOpenAI(
    model="hy3-free",
    api_key=os.environ.get("OPENCODE_API_KEY"),
    base_url="https://opencode.ai/zen/v1"
)
llm = CrewAILangChainAdapter(model="hy3-free", llm=langchain_llm)

import json

# Load Data Directly to bypass broken tool calling in hy3-free
try:
    with open("data/mock_erp.json", "r") as f:
        erp_data = json.dumps(json.load(f), indent=2)
    with open("data/mock_digital_trends.json", "r") as f:
        trends_data = json.dumps(json.load(f), indent=2)
    with open("data/mock_local_market.json", "r") as f:
        market_data = json.dumps(json.load(f), indent=2)
except Exception as e:
    erp_data = trends_data = market_data = f"Error loading data: {e}"

# Instantiate Tools
erp_tool = ReadERPTool()
trends_tool = ReadTrendsTool()
market_tool = ReadLocalMarketTool()
py_tool = ExecutePythonTool()
search_tool = WebSearchTool()

# Define Agents
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
    tools=[trends_tool, search_tool],
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

# Define Tasks
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

# Crew
crew = Crew(
    agents=[agent_erp, agent_trends, agent_market, agent_reporter],
    tasks=[task_erp, task_trends, task_market, task_report],
    process=Process.sequential
)

import subprocess

def latex_to_pdf(latex_text, filename_base="Procurement_Optimization_Report"):
    # Remove markdown code block wrappers if the LLM accidentally added them
    latex_text = re.sub(r'^```latex\n?', '', latex_text.strip(), flags=re.IGNORECASE)
    latex_text = re.sub(r'^```\n?', '', latex_text.strip())
    latex_text = re.sub(r'\n?```$', '', latex_text.strip())
    
    # Inject geometry package to fix margins and prevent Overfull \hbox
    if "\\usepackage[margin=1in]{geometry}" not in latex_text:
        latex_text = re.sub(r'(\\documentclass\[.*?\]\{.*?\}|\\documentclass\{.*?\})', r'\1\n\\usepackage[margin=1in]{geometry}', latex_text, count=1)
        
    tex_filename = f"{filename_base}.tex"
    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(latex_text)
    
    # Run pdflatex
    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_filename], check=True)

if __name__ == "__main__":
    try:
        result = crew.kickoff()
        latex_output = str(result)
        print("Crew finished. Generating PDF via pdflatex...")
        latex_to_pdf(latex_output)
        print("PDF Generated successfully.")
    except Exception as e:
        print(f"An error occurred during execution: {e}")
