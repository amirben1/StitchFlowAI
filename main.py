import os
from crewai import Agent, Task, Crew, Process, LLM
from tools import ReadERPTool, ReadTrendsTool, ReadLocalMarketTool
from fpdf import FPDF
import re

# Initialize LLM
llm = LLM(model="gemini/gemini-1.5-pro")

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
