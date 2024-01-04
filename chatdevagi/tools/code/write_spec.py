from typing import Type, Optional, List

from pydantic import BaseModel, Field

from chatdevagi.agent.agent_prompt_builder import AgentPromptBuilder
from chatdevagi.helper.error_handler import ErrorHandler
from chatdevagi.helper.prompt_reader import PromptReader
from chatdevagi.helper.token_counter import TokenCounter
from chatdevagi.lib.logger import logger
from chatdevagi.llms.base_llm import BaseLlm
from chatdevagi.models.agent_execution import AgentExecution
from chatdevagi.models.agent_execution_feed import AgentExecutionFeed
from chatdevagi.resource_manager.file_manager import FileManager
from chatdevagi.tools.base_tool import BaseTool
from chatdevagi.models.agent import Agent

class WriteSpecSchema(BaseModel):
    task_description: str = Field(
        ...,
        description="Specification task description.",
    )

    spec_file_name: str = Field(
        ...,
        description="Name of the file to write. Only include the file name. Don't include path."
    )


class WriteSpecTool(BaseTool):
    """
    Used to generate program specification.

    Attributes:
        llm: LLM used for specification generation.
        name : The name of tool.
        description : The description of tool.
        args_schema : The args schema.
        goals : The goals.
        resource_manager: Manages the file resources
    """
    llm: Optional[BaseLlm] = None
    agent_id: int = None
    agent_execution_id: int = None
    name = "WriteSpecTool"
    description = (
        "A tool to write the spec of a program."
    )
    args_schema: Type[WriteSpecSchema] = WriteSpecSchema
    goals: List[str] = []
    resource_manager: Optional[FileManager] = None

    class Config:
        arbitrary_types_allowed = True

    def _execute(self, task_description: str, spec_file_name: str) -> str:
        """
        Execute the write_spec tool.

        Args:
            task_description : The task description.
            spec_file_name: The name of the file where the generated specification will be saved.

        Returns:
            Generated specification or error message.
        """
        prompt = PromptReader.read_tools_prompt(__file__, "write_spec.txt")
        prompt = prompt.replace("{goals}", AgentPromptBuilder.add_list_items_to_string(self.goals))
        prompt = prompt.replace("{task}", task_description)
        messages = [{"role": "system", "content": prompt}]

        organisation = Agent.find_org_by_agent_id(self.toolkit_config.session, agent_id=self.agent_id)
        total_tokens = TokenCounter.count_message_tokens(messages, self.llm.get_model())
        token_limit = TokenCounter(session=self.toolkit_config.session, organisation_id=organisation.id).token_limit(self.llm.get_model())

        result = self.llm.chat_completion(messages, max_tokens=(token_limit - total_tokens - 100))
        
        if 'error' in result and result['message'] is not None:
            ErrorHandler.handle_openai_errors(self.toolkit_config.session, self.agent_id, self.agent_execution_id, result['message'])

        # Save the specification to a file
        write_result = self.resource_manager.write_file(spec_file_name, result["content"])
        if not write_result.startswith("Error"):
            return result["content"] + "\nSpecification generated and saved successfully"
        else:
            return write_result
