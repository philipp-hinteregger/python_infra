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
        client = boto3.client("elbv2", region_name="us-east-1")

        response = client.create_load_balancer(
            Name="my-load-balancer",
            Subnets=["subnet-0123456789abcdef0"],
            SecurityGroups=["sg-0123456789abcdef0"],
            Scheme="internet-facing",
            Type="application",
            IpAddressType="ipv4",
        )

        lb_arn = response["LoadBalancers"][0]["LoadBalancerArn"]
        client.add_tags(ResourceArns=[lb_arn], Tags=[{"Key": "Key1", "Value": "foo"}])

        result = get_load_balancer_arns_with_tag(tag_key="Key1", tag_value="foo")
        self.assertEqual(result, [lb_arn])

    @patch("aws.load_balancer.load_balancer.boto3.client")
    def test_delete_load_balancers_by_arn(self, mock_boto_client):
        mock_elb_client = MagicMock()
        mock_boto_client.return_value = mock_elb_client

        lb_arns = ["arn:aws:elb:region:account-id:loadbalancer/lb1"]
        mock_elb_client.get_waiter.return_value.wait.return_value = None

        delete_load_balancers_by_arn(lb_arns)
        mock_elb_client.delete_load_balancer.assert_called_with(
            LoadBalancerArn="arn:aws:elb:region:account-id:loadbalancer/lb1"
        )
        mock_elb_client.get_waiter.assert_called_with("load_balancers_deleted")
        mock_elb_client.get_waiter().wait.assert_called_with(LoadBalancerArns=lb_arns)


if __name__ == "__main__":
    unittest.main()
