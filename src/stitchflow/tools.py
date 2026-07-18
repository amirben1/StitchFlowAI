import json
from crewai.tools import BaseTool

def _read_json_file(filepath: str) -> str:
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        filename = filepath.split('/')[-1]
        return json.dumps({"Error": f"{filename} not found or could not be read: {str(e)}"})

class ReadERPTool(BaseTool):
    name: str = "Read ERP Data"
    description: str = "Reads internal ERP data regarding budget and capacity."
    
    def _run(self) -> str:
        return _read_json_file("data/mock_erp.json")

class RunDigitalScraperTool(BaseTool):
    name: str = "Run Digital Trends Scraper"
    description: str = "Scrapes live data from Google Trends, TikTok, and YouTube to gather fashion sentiment and velocity."
    
    def _run(self) -> str:
        try:
            from src.stitchflow.scraper.main import run_pipeline
            # Run the teammate's scraper pipeline
            report = run_pipeline(mock=False)
            return report.to_json()
        except Exception as e:
            # Fallback to mock data if there are network/rate limit issues
            from src.stitchflow.scraper.main import run_pipeline
            report = run_pipeline(mock=True)
            return f"Live scrape failed ({str(e)}). Falling back to mock data: {report.to_json()}"

class ReadLocalMarketTool(BaseTool):
    name: str = "Read Local Market Data"
    description: str = "Reads local market and competitor data."
    
    def _run(self) -> str:
        return _read_json_file("data/mock_local_market.json")

import subprocess

class ExecutePythonTool(BaseTool):
    name: str = "Execute Python Code"
    description: str = "Executes python code in a subprocess and returns the stdout and stderr. Use this to do math, analyze data, or run scripts. Input should be raw python code string."
    
    def _run(self, code: str) -> str:
        try:
            # write code to a temp file and execute
            with open("temp_agent_script.py", "w") as f:
                f.write(code)
            result = subprocess.run(
                ["python", "temp_agent_script.py"],
                capture_output=True,
                text=True,
                timeout=30
            )
            return f"Stdout:\n{result.stdout}\nStderr:\n{result.stderr}"
        except Exception as e:
            return f"Error executing code: {e}"

class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Searches the internet using DuckDuckGo and returns snippets. Input should be a search query string."
    
    def _run(self, query: str) -> str:
        try:
            from langchain_community.tools import DuckDuckGoSearchRun
            search = DuckDuckGoSearchRun()
            return search.run(query)
        except Exception as e:
            return f"Error searching web: {e}"
