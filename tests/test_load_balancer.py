import unittest
from unittest.mock import MagicMock, patch

import boto3
from moto import mock_aws

from aws.load_balancer.load_balancer import (
    delete_load_balancers_by_arn,
    get_load_balancer_arns_with_tag,
)


class TestAWSLoadBalancerFunctions(unittest.TestCase):

    @mock_aws
    def test_get_load_balancer_arns_with_tag(self):
        region = "us-east-1"
        client = boto3.client("elbv2", region_name=region)
        ec2_client = boto3.client("ec2", region_name=region)

        vpc = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")
        subnet1 = ec2_client.create_subnet(
            CidrBlock="10.0.1.0/24", VpcId=vpc["Vpc"]["VpcId"]
        )
        subnet2 = ec2_client.create_subnet(
            CidrBlock="10.0.2.0/24", VpcId=vpc["Vpc"]["VpcId"]
        )

        response = client.create_load_balancer(
            Name="my-load-balancer",
            Subnets=[subnet1["Subnet"]["SubnetId"], subnet2["Subnet"]["SubnetId"]],
            SecurityGroups=[],
            Tags=[{"Key": "Key1", "Value": "foo"}],
            Scheme="internet-facing",
            Type="application",
            IpAddressType="ipv4",
        )

        lb_arn = response["LoadBalancers"][0]["LoadBalancerArn"]

        result = get_load_balancer_arns_with_tag(
            tag_key="Key1", tag_value="foo", region=region
        )
        self.assertEqual(result, [lb_arn])

    @patch("aws.load_balancer.load_balancer.boto3.client")
    def test_delete_load_balancers_by_arn(self, mock_boto_client):
        region = "us-east-1"
        mock_elb_client = MagicMock()
        mock_boto_client.return_value = mock_elb_client

        lb_arns = ["arn:aws:elb:region:account-id:loadbalancer/lb1"]
        mock_elb_client.get_waiter.return_value.wait.return_value = None

        delete_load_balancers_by_arn(lb_arns, region=region)
        mock_elb_client.delete_load_balancer.assert_called_with(
            LoadBalancerArn="arn:aws:elb:region:account-id:loadbalancer/lb1"
        )
        mock_elb_client.get_waiter.assert_called_with("load_balancers_deleted")
        mock_elb_client.get_waiter().wait.assert_called_with(LoadBalancerArns=lb_arns)


if __name__ == "__main__":
    unittest.main()
