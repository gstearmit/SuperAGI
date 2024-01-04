from abc import ABC
from typing import List
from chatdevagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from chatdevagi.tools.file.append_file import AppendFileTool
from chatdevagi.tools.file.delete_file import DeleteFileTool
from chatdevagi.tools.file.list_files import ListFileTool
from chatdevagi.tools.file.read_file import ReadFileTool
from chatdevagi.tools.file.write_file import WriteFileTool
from chatdevagi.types.key_type import ToolConfigKeyType
from chatdevagi.models.tool_config import ToolConfig


class FileToolkit(BaseToolkit, ABC):
    name: str = "File Toolkit"
    description: str = "File Tool kit contains all tools related to file operations"

    def get_tools(self) -> List[BaseTool]:
        return [AppendFileTool(), DeleteFileTool(), ListFileTool(), ReadFileTool(), WriteFileTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return []
