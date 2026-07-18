import os
os.environ['GEMINI_API_KEY'] = 'dummy'
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
agent = Agent(role='test', goal='test', backstory='test', llm='gemini/gemini-1.5-pro')
agent.llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro')
task = Task(description='test', expected_output='test', agent=agent)
crew = Crew(agents=[agent], tasks=[task])
crew.kickoff()
