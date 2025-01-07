"""AWS utils to take care of all required functionality"""
from urllib.parse import urlparse

import boto3


s3_client = boto3.client('s3')


def get_ec2_instances_sizes(region: str):
    """Gets all ec2 instances"""
    ec2_client = boto3.client('ec2', region_name=region)
    instances_details = ec2_client.describe_instances(MaxResults=10)
    reservations = instances_details['Reservations']
    instances_sizes = []
    for reservation in reservations:
        instanceType = reservation['Instances'][0]['InstanceType']
        publicIp = None
        try:
            publicIp = reservation['Instances'][0]['PublicIpAddress']
        except:
            pass
        tags = reservation['Instances'][0]['Tags']
        name = None
        for tag in tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
        instances_sizes.append((name, instanceType, publicIp))
    return instances_sizes


def list_files(s3_path):
    """Lists all files under the given s3 path"""
    print(f"list files under '{s3_path}' ...")
    src_parsed = urlparse(s3_path)
    src_bucket = src_parsed.netloc
    src_s3_prefix = src_parsed.path[1:]
    print(f"s3 bucket: {src_bucket}, prefix: {src_s3_prefix}")

    bucket_object_list = []
    result = s3_client.list_objects(Bucket=src_bucket, Prefix=src_s3_prefix, Delimiter='/')
    if result is not None and result.get('CommonPrefixes') is not None:
        for o in result.get('CommonPrefixes'):
            if o is not None:
                bucket_object_list.append(o.get('Prefix'))
    return bucket_object_list


def list_all_buckets():
    """Lists all buckets"""
    responses = s3_client.list_buckets()['Buckets']
    bucket_names = []
    for rsp in responses:
        bucket_names.append(rsp['Name'])
    return bucket_names


def find_public_buckets(bucket_names):
    """Finds all public buckets"""
    public_buckets = []
    for bucket in bucket_names:
        isPublic = False
        try:
            rsp = s3_client.get_bucket_policy_status(Bucket=bucket)
            isPublic = rsp['PolicyStatus']['IsPublic']
        except:
            pass

        if not isPublic:
            try:
                rsp = s3_client.get_public_access_block(Bucket=bucket)
                isPublic = not (rsp['PublicAccessBlockConfiguration']['BlockPublicAcls'] \
                                  and rsp['PublicAccessBlockConfiguration']['BlockPublicPolicy'])
            except:
                pass

        # TODO: this case seems to be complicated, ignored for now!
        # if not isPublic:
        #     try:
        #         rsp = s3_client.get_bucket_acl(Bucket=bucket)
        #         # print(rsp)
        #         grants = rsp['Grants']
        #         for grant in grants:
        #             print(grant['Grantee']['Type'])
        #     except:
        #         pass

        if isPublic:
            public_buckets.append(bucket)
    return public_buckets


def get_groups_by_username(iam_client, username):
    """Gets the groups of user"""
    groups_json = iam_client.list_groups_for_user(UserName=username)['Groups']
    group_names = []
    for group in groups_json:
        group_names.append(group['GroupName'])
    return group_names


def get_group_policies(iam_client, user_groups):
    """Gets the group policies"""
    user_policies = []
    for group in user_groups:
        # This is for AWS managed policies and returns both the policy ARN and name
        attached_group_policies = (iam_client.list_attached_group_policies(GroupName=group)['AttachedPolicies'])
        for policy in attached_group_policies:
            user_policies.append(policy['PolicyName'])
        # This is for inline policies and returns only the policy name
        group_policies = (iam_client.list_group_policies(GroupName=group)['PolicyNames'])
        for policy in group_policies:
            user_policies.append(policy)
    return user_policies


def get_user_policies(username):
    """Gets the user policies"""
    iam_client = boto3.client('iam')
    group_names = get_groups_by_username(iam_client, username)
    user_policies = get_group_policies(iam_client, group_names)

    # This is for AWS managed policies and returns both the policy ARN and name
    attached_user_policies = (iam_client.list_attached_user_policies(UserName=username)['AttachedPolicies'])
    for policy in attached_user_policies:
        user_policies.append(policy['PolicyName'])
    # This is for inline policies and returns only the policy name
    _user_policies = (iam_client.list_user_policies(UserName=username)['PolicyNames'])
    for policy in _user_policies:
        user_policies.append(policy)
    return user_policies

