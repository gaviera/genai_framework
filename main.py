import os, sys
from app.agents.scrapper_agent import scrapper
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from loguru import logger

# Add the project base path to the system path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE)

# Load environment variables from a .env file
load_dotenv()

# Run an infinite loop to continuously take user input
while True:
    prompt = input("?> ")
    # If the user provided a prompt, process it with the scrapper agent
    if prompt:
        response = scrapper.runnable.invoke(
            config={"configurable":{"session_id":"test1"}},
            input={"messages": [HumanMessage(content=prompt)]})
        logger.debug(response)
        print(f"IA> {response.content}")  # Print the agent's response
