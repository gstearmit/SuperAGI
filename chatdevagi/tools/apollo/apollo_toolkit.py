from abc import ABC
from typing import List

from chatdevagi.tools.apollo.apollo_search import ApolloSearchTool
from chatdevagi.tools.base_tool import BaseToolkit, BaseTool, ToolConfiguration
from chatdevagi.types.key_type import ToolConfigKeyType


class ApolloToolkit(BaseToolkit, ABC):
    name: str = "ApolloToolkit"
    description: str = "Apollo Tool kit contains all tools related to apollo.io tasks"

    def get_tools(self) -> List[BaseTool]:
        return [ApolloSearchTool()]

    def get_env_keys(self) -> List[str]:
        return [ToolConfiguration(key="APOLLO_SEARCH_KEY", key_type=ToolConfigKeyType.STRING, is_required=True)]
