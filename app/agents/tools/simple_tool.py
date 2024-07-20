from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Union, Type

# Define a Pydantic model for the input schema of the tool
class SimpleToolScriptInput(BaseModel):
    name: str = Field(description="Person's name")

# Define a tool class that greets a user by name
class SimpleTool(BaseTool):
    # Set the name and description of the tool
    name: str = "SimpleTool"
    description: str = (
        """
        Greet the user in the terminal when they provide their name
        """
    )
    # Specify the input schema for the tool
    args_schema: Type[BaseModel] = SimpleToolScriptInput

    def _run(
        self,
        name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **args,
    ) -> Union[str, Exception]:
        """
        Run the tool synchronously to greet the user.
        
        Args:
            name (str): The name of the person to greet.
            run_manager (Optional[CallbackManagerForToolRun]): Optional manager for handling callbacks.
        
        Returns:
            Union[str, Exception]: Returns True if successful, otherwise an error message.
        """
        try:
            # Print a greeting message to the terminal
            print(f"Hola, {name}!")
            return True
        except Exception as e:
            # Return the exception message if an error occurs
            return repr(e)

    async def _arun(
        self,
        name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **args,
    ) -> Union[str, Exception]:
        """
        Run the tool asynchronously to greet the user.
        
        Args:
            name (str): The name of the person to greet.
            run_manager (Optional[CallbackManagerForToolRun]): Optional manager for handling callbacks.
        
        Returns:
            Union[str, Exception]: Returns True if successful, otherwise an error message.
        """
        try:
            # Print a greeting message to the terminal
            print(f"Hola, {name}!")
            return True
        except Exception as e:
            # Return the exception message if an error occurs
            return repr(e)
