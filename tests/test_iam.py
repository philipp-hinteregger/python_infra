import json
import unittest

import boto3
from moto import mock_aws

from aws.iam.iam import get_policies_like, get_roles_like


class TestFetchIamRoles(unittest.TestCase):

    @mock_aws
    def test_get_roles_like(self):
        client = boto3.client("iam")

        client.create_role(RoleName="NotMyRole1", AssumeRolePolicyDocument="{}")
        client.create_role(RoleName="TestRole2", AssumeRolePolicyDocument="{}")
        client.create_role(RoleName="TestRole3", AssumeRolePolicyDocument="{}")

        roles = get_roles_like("TestRole")

        role_names = [role["RoleName"] for role in roles]
        self.assertCountEqual(role_names, ["TestRole2", "TestRole3"])

    @mock_aws
    def test_get_policies_like(self):
        client = boto3.client("iam")

        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:ListBucket",
                    "Resource": "arn:aws:s3:::example_bucket",
                }
            ],
        }

        client.create_policy(
            PolicyName="NotMyPolicy1", PolicyDocument=json.dumps(policy_document)
        )
        client.create_policy(
            PolicyName="TestPolicy2", PolicyDocument=json.dumps(policy_document)
        )
        client.create_policy(
            PolicyName="TestPolicy3", PolicyDocument=json.dumps(policy_document)
        )

        policies = get_policies_like("TestPolicy")

        policy_names = [policy["PolicyName"] for policy in policies]
        self.assertCountEqual(policy_names, ["TestPolicy2", "TestPolicy3"])


if __name__ == "__main__":
    unittest.main()
