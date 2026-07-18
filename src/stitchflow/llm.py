import os
from typing import Any
from dotenv import load_dotenv
from crewai.llms.base_llm import BaseLLM
from langchain_openai import ChatOpenAI

load_dotenv()

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
