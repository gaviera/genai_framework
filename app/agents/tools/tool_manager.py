from langchain_core.tools import Tool
from app.agents.tools.simple_tool import SimpleTool
from typing import List, Type
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class ToolManager:
    # A class to manage and retrieve tools

    def __init__(self) -> None:
        """
        Initializes the ToolManager with a dictionary of mapped tools.
        """
        self.MAPPED_TOOLS = {
            "simpletool": SimpleTool()  # Map the tool name to its instance
        }

    @staticmethod
    def all() -> List[Type[Tool]]:
        """
        Returns a list of all available tool instances.
        
        Returns:
            List[Type[Tool]]: A list containing all tool instances.
        """
        return [SimpleTool()]

    def get_tool(self, tools: list) -> List[Type[Tool]]:
        """
        Retrieves the tool instances based on the provided tool names.
        
        Args:
            tools (list): A list of tool names to retrieve.
        
        Returns:
            List[Type[Tool]]: A list of tool instances corresponding to the provided tool names.
        """
        return [self.MAPPED_TOOLS[tool] for tool in tools if tool in self.MAPPED_TOOLS]
