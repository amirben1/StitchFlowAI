import os
import json
from tools import ReadERPTool, ReadTrendsTool, ReadLocalMarketTool

def test_tools_read_existing_files():
    assert "budget_tnd" in ReadERPTool()._run()
    assert "trends" in ReadTrendsTool()._run()
    assert "competitors" in ReadLocalMarketTool()._run()

def test_tools_handle_missing_files():
    # temporarily rename data dir to test error handling
    os.rename("data", "data_tmp")
    try:
        assert "Error" in ReadERPTool()._run()
    finally:
        os.rename("data_tmp", "data")
