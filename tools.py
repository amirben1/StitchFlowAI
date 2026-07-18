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
