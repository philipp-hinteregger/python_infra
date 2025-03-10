import unittest

import boto3
from moto import mock_aws

from aws.load_balancer.load_balancer import (
    delete_load_balancers_by_arn,
    get_load_balancer_arns_with_tag,
)


@mock_aws
class TestAWSLoadBalancerFunctions(unittest.TestCase):

    def setUp(self):
        self.region = "us-east-1"
        self.lb_name = "my-load-balancer"
        self.client = boto3.client("elbv2", region_name=self.region)
        ec2_client = boto3.client("ec2", region_name=self.region)

        vpc = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")
        subnet1 = ec2_client.create_subnet(
            CidrBlock="10.0.1.0/24", VpcId=vpc["Vpc"]["VpcId"]
        )
        subnet2 = ec2_client.create_subnet(
            CidrBlock="10.0.2.0/24", VpcId=vpc["Vpc"]["VpcId"]
        )

        response = self.client.create_load_balancer(
            Name=self.lb_name,
            Subnets=[subnet1["Subnet"]["SubnetId"], subnet2["Subnet"]["SubnetId"]],
            SecurityGroups=[],
            Tags=[{"Key": "Key1", "Value": "foo"}],
            Scheme="internet-facing",
            Type="application",
            IpAddressType="ipv4",
        )
        self.lb_arn = response["LoadBalancers"][0]["LoadBalancerArn"]

    def test_get_load_balancer_arns_with_tag(self):
        result = get_load_balancer_arns_with_tag(
            tag_key="Key1", tag_value="foo", region=self.region
        )
        self.assertEqual(result, [self.lb_arn])

    def test_get_load_balancer_arns_with_wrong_tag(self):
        result = get_load_balancer_arns_with_tag(
            tag_key="Key1", tag_value="foo2", region=self.region
        )
        self.assertEqual(result, [])

    def test_delete_load_balancers_by_arn(self):
        delete_load_balancers_by_arn(self.lb_arn, region=self.region)
        response = self.client.describe_load_balancers()
        lbs = [lb["LoadBalancerArn"] for lb in response["LoadBalancers"]]
        self.assertNotIn([self.lb_arn], lbs)


if __name__ == "__main__":
    unittest.main()
