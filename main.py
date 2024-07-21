import os, sys
from app.agents.scrapper_agent import scrapper
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from loguru import logger

# Load environment variables from a .env file
load_dotenv()

# Load session_id from parameter, otherwise set default session_id
args = sys.argv[1:]
if len(args) == 1:
    session_id=args[0]
else:
    session_id="default"

# Run an infinite loop to continuously take user input
while True:
    prompt = input("?> ")
    # If the user provided a prompt, process it with the scrapper agent
    if prompt:
        response = scrapper.runnable.invoke(
            config={"configurable":{"session_id":session_id}},
            input={"messages": [HumanMessage(content=prompt)]})
        logger.debug(response)
        print(f"IA> {response.content}")  # Print the agent's response
