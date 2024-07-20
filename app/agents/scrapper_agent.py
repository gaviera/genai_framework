from core.builders.agent_builder import Agent
from core.executors.runnable_executor import RunnableExecutor
from langchain_openai import ChatOpenAI

# Define the system prompt for the scrapper agent
scrapper_prompt = ("""
                You're an assistant to get information in the web from the specific theme that the user sends to you
                """)

# List of tools to be used by the scrapper agent
scrapper_tools = ["simpletool"]

# Create an instance of the Agent class with the specified parameters and create the agent
scrapper_agent = Agent(
    name="scrapper",
    system_prompt=scrapper_prompt,
    conversation_history=False,
    llm=ChatOpenAI(model="gpt-4o-mini"),
    tools=scrapper_tools
).create()

scrapper_runnable = RunnableExecutor(scrapper_agent)