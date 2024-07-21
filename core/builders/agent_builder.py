from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableSerializable
from langchain_core.language_models import BaseChatModel
from core.builders.tool_manager import ToolManager
from core.builders.prompt_builder import PromptBuilder
from typing import List

class Agent:
    # A class to create an agent with a specific name, prompt, conversation history setting,
    # language model, and a list of tools.

    def __init__(self, 
                 name: str, 
                 system_prompt: str,
                 conversation_history: bool,
                 llm: BaseChatModel,
                 tools: List[str]) -> None:
        """
        Initializes the Agent with the given parameters.
        
        Args:
            name (str): The name of the agent.
            system_prompt (str): The system prompt for the agent.
            conversation_history (bool): A flag indicating whether to include conversation history.
            llm (BaseChatModel): The language model used by the agent.
            tools (List[str]): A list of tool names to be used by the agent.
        """
        
        self.name: str = name
        self.system_prompt: str = system_prompt
        self.conversation_history: bool = conversation_history
        self.llm: BaseChatModel = llm
        self.tools: List[str] = tools

    def create(self) -> RunnableSerializable:
        """
        Creates a runnable agent with the specified parameters.
        
        Returns:
            RunnableSerializable: The runnable agent with the specified prompt, model, and tools.
        """
        try:
            # Create the prompt using the PromptBuilder
            prompt = PromptBuilder.create(system_prompt=self.system_prompt, 
                                          conversation_history=self.conversation_history)

            # Get tool instances from the ToolManager
            tools_instances = ToolManager().get_tool(self.tools)

            # Create the runnable by combining the prompt, model, and tools
            runnable = prompt | self.llm.bind_tools(tools_instances)
            runnable.name = self.name

            return runnable
         
        except ValueError as e:
            # Print an error message if there is an issue creating the agent
            print(f"Error creating the agent {self.name}: {str(e)}")
