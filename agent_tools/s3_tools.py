"""Tools for accessing s3 buckets"""

from langchain_core.tools import tool

from utils.aws_utils import list_all_buckets, find_public_buckets, list_files


@tool(return_direct=True, response_format='content_and_artifact')
def list_all_buckets_tool() -> list[str]:
    """Lists all buckets"""
    print('calling list_all_buckets()...')
    all_buckets = list_all_buckets()
    content = f'Successfully retrieved all {len(all_buckets)} buckets {all_buckets}'
    return (content, all_buckets)


@tool(return_direct=True, response_format='content_and_artifact')
def get_public_buckets_count_tool() -> list[str]:
    """Lists all public buckets"""
    print('calling get_public_buckets_count_tool()...')
    buckets = list_all_buckets()
    #take first 25 buckets due to long run times with increasing bucket length
    public_buckets = find_public_buckets(buckets)
    content = f'Successfully retrieved {len(public_buckets)} public buckets.'
    return (content, public_buckets)


@tool(return_direct=True, response_format='content_and_artifact')
def fetch_files_from_bucket_tool(bucket_name) -> list[str]:
    """Lists all files from the bucket"""
    print('calling fetch_files_from_bucket_tool()...')
    if not bucket_name.startswith('s3://'):
        s3_bucket = f's3://{bucket_name}'
    else:
        s3_bucket = bucket_name
    all_files = list_files(s3_bucket)
    content = f'Successfully retrieved files: {all_files} from bucket {s3_bucket}'
    return (content, all_files)