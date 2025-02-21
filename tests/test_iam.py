import unittest

import boto3
from moto.iam import mock_iam

from aws.load_balancer.load_balancer import get_policies_like, get_roles_like


class TestFetchIamRoles(unittest.TestCase):

    @mock_iam
    def test_get_roles_like(self):
        client = boto3.client("iam")

        client.create_role(RoleName="NotMyRole1", AssumeRolePolicyDocument="{}")
        client.create_role(RoleName="TestRole2", AssumeRolePolicyDocument="{}")
        client.create_role(RoleName="TestRole3", AssumeRolePolicyDocument="{}")

        roles = get_roles_like("TestRole")

        role_names = [role["RoleName"] for role in roles]
        self.assertEqual(role_names, ["TestRole2", "TestRole3"])

    @mock_iam
    def test_get_policies_like(self):
        client = boto3.client("iam")

        client.create_policy(PolicyName="NotMyPolicy1", PolicyDocument="{}")
        client.create_policy(PolicyName="TestPolicy2", PolicyDocument="{}")
        client.create_policy(PolicyName="TestPolicy3", PolicyDocument="{}")

        policies = get_policies_like("TestPolicy")

        policy_names = [policy["PolicyName"] for policy in policies]
        self.assertEqual(policy_names, ["TestPolicy2", "TestPolicy3"])


if __name__ == "__main__":
    unittest.main()
