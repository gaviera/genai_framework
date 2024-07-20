import os, sys

# Add the project base path to the system path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE)

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage

# Import the scrapper agent
from app.agents.scrapper_agent import scrapper_agent, scrapper_runnable

# Run an infinite loop to continuously take user input
while True:
    prompt = input()
    # If the user provided a prompt, process it with the scrapper agent
    if prompt:
        response = scrapper_agent.invoke(input={"messages": [HumanMessage(content=prompt)]})
        print(response)  # Print the agent's response
