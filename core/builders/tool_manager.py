import importlib, inspect, sys, glob, os
from langchain_core.tools import Tool
from typing import List, Type
from dotenv import load_dotenv
from pathlib import Path
from langchain_core.tools import BaseTool
from loguru import logger

# Load environment variables from a .env file
load_dotenv()

class ToolManager:
    # A class to manage and retrieve tools

    def __init__(self) -> None:
        """
        Initializes the ToolManager with a dictionary of mapped tools.
        """

        self.instances = get_tool_instances()

        mapped_tools = {}
        for instance in self.instances:
            mapped_tools[instance.name] = instance

        logger.debug(f"[TOOL_MANAGER] {len(mapped_tools)} tools initialized.")
        self.MAPPED_TOOLS = mapped_tools

    @staticmethod
    def all() -> List[Type[Tool]]:
        """
        Returns a list of all available tool instances.
        
        Returns:
            List[Type[Tool]]: A list containing all tool instances.
        """
        return get_tool_instances() 

    def get_tool(self, tools: list) -> List[Type[Tool]]:
        """
        Retrieves the tool instances based on the provided tool names.
        
        Args:
            tools (list): A list of tool names to retrieve.
        
        Returns:
            List[Type[Tool]]: A list of tool instances corresponding to the provided tool names.
        """
        return [self.MAPPED_TOOLS[tool] for tool in tools if tool in self.MAPPED_TOOLS]

def get_tool_instances() -> List[Type[Tool]]:
    instances = []
    path = os.path.abspath(os.curdir)
    for file in glob.glob(f"{path}/app/agents/tools/*.py"):
        p,f = os.path.split(file)
        path_pyfile = Path(file)
        sys.path.append(str(path_pyfile.parent))
        tool_module = importlib.import_module(path_pyfile.stem)
        for name_local in dir(tool_module):
            if (not name_local.endswith("py") 
                and inspect.isclass(getattr(tool_module, name_local))
                and issubclass(getattr(tool_module, name_local), BaseTool) 
                and name_local not in ['BaseTool']):
                    ToolClass = getattr(tool_module, name_local)
                    instances.append(ToolClass())
    return instances
