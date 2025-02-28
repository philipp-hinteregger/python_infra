import boto3


def get_roles_like(role_name_part):
    iam_client = boto3.client("iam")
    paginator = iam_client.get_paginator("list_roles")
    matching_roles = []

    for page in paginator.paginate():
        for role in page["Roles"]:
            if role_name_part in role["RoleName"]:
                matching_roles.append(role)

    return matching_roles


def get_policies_like(policy_name_part):
    iam_client = boto3.client("iam")
    paginator = iam_client.get_paginator("list_policies")
    matching_policies = []

    for page in paginator.paginate():
        for policy in page["Policies"]:
            if policy_name_part in policy["PolicyName"]:
                matching_policies.append(policy)

    return matching_policies
