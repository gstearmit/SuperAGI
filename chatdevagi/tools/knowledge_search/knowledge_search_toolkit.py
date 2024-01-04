from abc import ABC
from typing import List
from chatdevagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from chatdevagi.tools.knowledge_search.knowledge_search import KnowledgeSearchTool
from chatdevagi.types.key_type import ToolConfigKeyType

class KnowledgeSearchToolkit(BaseToolkit, ABC):
    name: str = "Knowledge Search Toolkit"
    description: str = "Toolkit containing tools for performing search on the knowledge base."

    def get_tools(self) -> List[BaseTool]:
        return [KnowledgeSearchTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return [
            ToolConfiguration(key="OPENAI_API_KEY", key_type=ToolConfigKeyType.STRING, is_required=False, is_secret=True)
        ]