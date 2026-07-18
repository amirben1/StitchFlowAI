from unittest.mock import patch
from tools import ReadERPTool, ReadTrendsTool, ReadLocalMarketTool

def test_tools_read_existing_files():
    assert "budget_tnd" in ReadERPTool()._run()
    assert "trends" in ReadTrendsTool()._run()
    assert "competitors" in ReadLocalMarketTool()._run()

@patch('builtins.open')
def test_tools_handle_missing_files(mock_open):
    mock_open.side_effect = FileNotFoundError("No such file or directory")
    
    assert "Error" in ReadERPTool()._run()
    assert "Error" in ReadTrendsTool()._run()
    assert "Error" in ReadLocalMarketTool()._run()
