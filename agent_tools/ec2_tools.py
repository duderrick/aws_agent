"""Tools for EC2 instances"""

from langchain_core.tools import tool

from utils.aws_utils import get_ec2_instances_sizes
from utils.constants import REGION


@tool(return_direct=True, response_format='content_and_artifact')
def get_ec2_instance_size_tool(ip_address: str) -> str:
    """Get EC2 instance size"""
    print('calling get_ec2_instance_size_tool()...')
    all_ec2_instances = get_ec2_instances_sizes(REGION)
    filtered_instances = list(filter(lambda x: x[2] == ip_address, all_ec2_instances))
    if len(filtered_instances) > 0:
        filtered = filtered_instances[0]
        content = f'The ip address \"{ip_address}\" was found {filtered}'
    else:
        content = f'There are not matched found for this ip \"{ip_address}\"'
        filtered = ''
    return (content, filtered[1])

