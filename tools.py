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

class ReadTrendsTool(BaseTool):
    name: str = "Read Digital Trends Data"
    description: str = "Reads digital fashion trends data."
    
    def _run(self) -> str:
        return _read_json_file("data/mock_digital_trends.json")

class ReadLocalMarketTool(BaseTool):
    name: str = "Read Local Market Data"
    description: str = "Reads local market and competitor data."
    
    def _run(self) -> str:
        return _read_json_file("data/mock_local_market.json")
