from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
import operator, json
from typing import Annotated, TypedDict, Union, Callable
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import AIMessage, message_to_dict

class AgentState(TypedDict):
    """
    State of the agent during the conversation.

    Attributes:
        input (str): The input string.
        chat_history (list[BaseMessage]): List of previous messages in the conversation.
        agent_outcome (Union[AgentAction, AgentFinish, None]): The result of a call to the agent.
        intermediate_steps (Annotated[list[tuple[AgentAction, str]], operator.add]): List of actions and corresponding observations.
    """
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]

class RunnableExecutor:
    """
    Executes a Runnable object with retry capability.

    Attributes:
        runnable (Runnable): The Runnable object to execute.
        name (str): The name of the Runnable.
        max_retries (int): Maximum number of retries.
    """

    def __init__(self, runnable: Runnable, max_retries: int = 2):
        """
        Initializes RunnableExecutor with the Runnable and the maximum number of retries.

        Args:
            runnable (Runnable): The Runnable object to execute.
            max_retries (int, optional): Maximum number of retries. Default is 2.
        """
        self.runnable = runnable
        self.name = runnable.name
        self.max_retries = max_retries

    async def __invoke(self, state: AgentState, config: RunnableConfig):
        """
        Invokes the Runnable with the provided state and configuration.

        Args:
            state (AgentState): The state of the agent.
            config (RunnableConfig): The configuration for the execution.

        Returns:
            BaseMessage: The result of the Runnable execution.
        """
        result = await self.runnable.ainvoke(state, config=config)

        # Ensure tool call responses are handled properly
        if not result.additional_kwargs.get('tool_calls', []) and (
            not result.content
            or isinstance(result.content, list) and not result.content[0].get("text")
        ):
            human_message_handle = HumanMessage(content="Please provide a valid output.")
            state["messages"].append(human_message_handle)

        return result
    
    async def __call__(self, state: AgentState, config: RunnableConfig, invoke_funk: Callable = None):
        """
        Calls the Runnable with retries in case of failures.

        Args:
            state (AgentState): The state of the agent.
            config (RunnableConfig): The configuration for the execution.
            invoke_funk (Callable, optional): Alternative invocation function.

        Returns:
            dict: Dictionary with the resulting message or an error message in case of failure.
        """
        for i in range(self.max_retries):
            try:
                result = await self.__invoke(state, config) if not invoke_funk else await invoke_funk(state, config)
                break
            except Exception:
                if i == self.max_retries - 1:
                    return {"messages": AIMessage(content="I cannot resolve the task. Retry.")}

        if isinstance(result, BaseMessage):
            result = self.__get_message_type(result)
        
        return {"messages": result}

    def __get_message_type(self, from_: BaseMessage):
        """
        Returns the message type from the base message.

        Args:
            from_ (BaseMessage): The base message.

        Returns:
            BaseMessage: The original message.
        """
        return from_
