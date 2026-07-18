"""
Thin, provider-agnostic wrapper so the rest of the pipeline never cares
whether the reasoning step runs on Gemini or Claude.

Set env var LLM_PROVIDER=gemini or LLM_PROVIDER=anthropic
Set the matching API key: GEMINI_API_KEY or ANTHROPIC_API_KEY

If neither key is present, `complete()` returns a clearly-labeled
placeholder string instead of crashing, so the rest of the pipeline
(fusion, reports) can still be demoed end-to-end without a key.
"""
import os

def complete(system_prompt: str, user_prompt: str, max_tokens: int = 1200) -> str:
    try:
        from src.stitchflow.llm import langchain_llm
        from langchain_core.messages import SystemMessage, HumanMessage
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = langchain_llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"[LLM Narrative Generation Failed: {str(e)}. Showing raw fused trend data instead.]"
