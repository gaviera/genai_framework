from core.executors.runnable_executor import RunnableExecutor
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
import operator, json
from typing import Annotated, TypedDict, Union, Callable
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import AIMessage, message_to_dict
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb import MongoDBChatMessageHistory
from pymongo import errors

class AgentState(TypedDict):
    """
    State of the agent during a conversation.

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

class RunnableWithMemoryExecutor(RunnableExecutor):
    """
    Extends RunnableExecutor to handle message histories during the execution of Runnable objects.
    Adds the functionality of using message histories to improve decision making and remember previous contexts.
    """

    def __init__(self, runnable: Runnable, max_retries: int = 2):
        """
        Initializes an instance of RunnableWithMemoryExecutor, extending the initialization of RunnableExecutor
        to include handling of message history.
        
        Args:
            runnable (Runnable): The Runnable object to execute.
            max_retries (int): Maximum number of retries. Default is 2.
        """
        super().__init__(runnable=runnable, max_retries=max_retries)
        self.runnable = RunnableWithMessageHistory(
            runnable=runnable,
            get_session_history=self.__get_message_history,
            input_messages_key="messages",
            history_messages_key="history",
        )
        self.max_retries = max_retries

    async def __invoke(self, state: AgentState, config: RunnableConfig):
        """
        Asynchronous method that invokes the Runnable with message history handling. Modifies the state to include
        user information if the last message is not from a human, ensuring the necessary context is present for correct execution.
        
        Args:
            state (AgentState): Current state of the agent, including message history.
            config (RunnableConfig): Configuration for the execution of the Runnable.
        
        Returns:
            BaseMessage: Result of the Runnable execution, including history handling.
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
        Calls the custom __invoke method of this class to execute the Runnable with message history handling.
        Uses retries in case of failures.
        
        Args:
            state (AgentState): Current state of the agent.
            config (RunnableConfig): Configuration for the execution.
        
        Returns:
            dict: Result of the execution, which may include a message or a modified state.
        """
        return await super().__call__(state, config, self.__invoke)

    def __get_message_history(self, session_id: str) -> MongoDBChatMessageHistory:
        """
        Retrieves the message history associated with a given session ID using a MongoDB database.
        
        Args:
            session_id (str): Identifier of the session for which to retrieve the history.
        
        Returns:
            MongoDBChatMessageHistory: Object containing the message history of the session.
        """
        result = CustomMongoDBChatMessageHistory(connection_string="mongodb://localhost:27017", session_id=session_id)
        return result

class CustomMongoDBChatMessageHistory(MongoDBChatMessageHistory):
    """ Extension of the MongoDBChatMessageHistory class """

    def add_message(self, message: BaseMessage) -> None:
        """
        Append the message to the record in MongoDB.
        
        Args:
            message (BaseMessage): The message to add to the history.
        """
        try:
            # If the message is not a tool call or a tool response, save it
            if message_to_dict(message)["data"]["additional_kwargs"].get("tool_calls", None) is None:
                if message_to_dict(message)["type"] != "tool":
                    new_message = {
                        "SessionId": self.session_id,
                        "History": json.dumps(message_to_dict(message)),
                    }
                    if not self.collection.find_one(new_message):
                        self.collection.insert_one(new_message)
        except errors.WriteError as err:
            print(err)

    def clear(self) -> None:
        """
        Clear the message history.
        """
        return super().clear()
