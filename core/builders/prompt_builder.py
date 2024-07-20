from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class PromptBuilder:
    # A class that builds chat prompts using specified templates and placeholders.
    
    @staticmethod
    def create(system_prompt: str, conversation_history: bool = False) -> ChatPromptTemplate:
        """
        Creates a chat prompt template with the given system prompt and optional conversation history.
        
        Args:
            system_prompt (str): The system-level prompt to be included in the chat template.
            conversation_history (bool): A flag indicating whether to include conversation history. Defaults to False.
        
        Returns:
            ChatPromptTemplate: The constructed chat prompt template.
        """
        
        # Create a history placeholder if conversation_history is True, otherwise use a default tuple
        history_placeholder = MessagesPlaceholder(variable_name="history") if conversation_history else ("system", "")

        try:
            # Create the chat prompt template from the provided messages and placeholders
            created_prompt = ChatPromptTemplate.from_messages(
                [("system", system_prompt),
                 history_placeholder,
                 MessagesPlaceholder(variable_name="messages")]
            )
            return created_prompt
        except Exception as e:
            # Raise a ValueError if there is an error during the creation of the prompt
            raise ValueError(f"Error creating prompt: {e}")
