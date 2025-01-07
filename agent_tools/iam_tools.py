"""tools to support IAM"""

from langchain_core.tools import tool

from utils.aws_utils import get_user_policies


@tool(return_direct=True, response_format='content_and_artifact')
def get_user_permissions_tool(username: str):
    """Gets the permissions of the user: username"""
    print('calling get_user_permissions_tool()...')
    user_policies = get_user_policies(username)
    content = f'The user {username} has access to {user_policies}'
    return (content, user_policies)
