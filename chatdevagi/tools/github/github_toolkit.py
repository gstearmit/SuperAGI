from abc import ABC
from typing import List
from chatdevagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from chatdevagi.tools.github.add_file import GithubAddFileTool
from chatdevagi.tools.github.delete_file import GithubDeleteFileTool
from chatdevagi.tools.github.fetch_pull_request import GithubFetchPullRequest
from chatdevagi.tools.github.search_repo import GithubRepoSearchTool
from chatdevagi.tools.github.review_pull_request import GithubReviewPullRequest
from chatdevagi.types.key_type import ToolConfigKeyType


class GitHubToolkit(BaseToolkit, ABC):
    name: str = "GitHub Toolkit"
    description: str = "GitHub Tool Kit contains all github related to tool"

    def get_tools(self) -> List[BaseTool]:
        return [GithubAddFileTool(), GithubDeleteFileTool(), GithubRepoSearchTool(), GithubReviewPullRequest(),
                GithubFetchPullRequest()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return [
            ToolConfiguration(key="GITHUB_ACCESS_TOKEN", key_type=ToolConfigKeyType.STRING, is_required= True, is_secret = True),
            ToolConfiguration(key="GITHUB_USERNAME", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=False)
        ]


