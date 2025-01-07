"""Our AWS LLM agent"""

from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from agent_tools.ec2_tools import get_ec2_instance_size_tool
from agent_tools.iam_tools import get_user_permissions_tool
from agent_tools.s3_tools import list_all_buckets_tool, \
    get_public_buckets_count_tool, fetch_files_from_bucket_tool
from utils.constants import ANTHROPIC_3_SONNET_MODEL_ID
from utils.llm_model_utils import load_model
from utils.message_utils import message_output
from langgraph.graph.graph import CompiledGraph


def list_all_public_buckets(agent: CompiledGraph):
    """Queries our agent to list all public buckets"""
    response = agent.invoke({'messages': [HumanMessage(content='How many S3 buckets are exposed to the public')]})
    message_output(response)
    public_buckets = len(response['messages'][-1].artifact)
    print(f'There are {public_buckets} public s3 buckets.')


def fetch_files_for_bucket(agent: CompiledGraph):
    """Queries our agent to fetch all files in a bucket"""
    s3_bucket = input('Enter your s3 bucket: ')
    response = agent.invoke({'messages':[HumanMessage(content=f'What data does the S3 bucket {s3_bucket} hold')]})
    message_output(response)
    files = response['messages'][-1].artifact
    print(f'The s3 bucket holds {files}')


def get_ec2_size(agent: CompiledGraph):
    """Queries our agent for the ec2 instance size"""
    ip_address = input('Enter your ec2 ip address: ')
    response = agent.invoke({'messages':[HumanMessage(content=f'What is the size of the EC2 instance with IP {ip_address}')]})
    message_output(response)
    size = response['messages'][-1].artifact
    print(f'This is the size of the ec2 instance with ip({ip_address}): {size}')


def get_user_permissions(agent: CompiledGraph):
    """Queries the agent for the user's permissions"""
    username = input('Enter the username of permissions you want to check:')
    response = agent.invoke({'messages':[HumanMessage(content=f'What permissions does the user {username} have?')]})
    message_output(response)
    permissions = response['messages'][-1].artifact
    print(f'These are the user permissions {permissions}')


if __name__ == '__main__':
    model = load_model(ANTHROPIC_3_SONNET_MODEL_ID)
    tools = [list_all_buckets_tool, get_public_buckets_count_tool,
             fetch_files_from_bucket_tool, get_ec2_instance_size_tool,
             get_user_permissions_tool]
    agent_executor = create_react_agent(model, tools)
    list_all_public_buckets(agent_executor)
    fetch_files_for_bucket(agent_executor)
    get_ec2_size(agent_executor)
    get_user_permissions(agent_executor)