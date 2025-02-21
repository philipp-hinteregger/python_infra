import unittest
from unittest.mock import MagicMock, patch

from aws.load_balancer.load_balancer import (
    delete_load_balancers_by_arn,
    get_load_balancer_arns_with_tag,
)


class TestAWSLoadBalancerFunctions(unittest.TestCase):

    @patch("aws.load_balancer.load_balancer.boto3.client")
    def test_get_load_balancer_arns_with_tag(self, mock_boto_client):
        mock_elb_client = MagicMock()
        mock_boto_client.return_value = mock_elb_client

        mock_elb_client.describe_load_balancers.return_value = {
            "LoadBalancers": [
                {"LoadBalancerArn": "arn:aws:elb:region:account-id:loadbalancer/lb1"},
                {"LoadBalancerArn": "arn:aws:elb:region:account-id:loadbalancer/lb2"},
            ]
        }
        mock_elb_client.describe_tags.side_effect = [
            {"TagDescriptions": [{"Tags": [{"Key": "key1", "Value": "right-value"}]}]},
            {"TagDescriptions": [{"Tags": [{"Key": "key1", "Value": "wrong-value"}]}]},
        ]

        arns = get_load_balancer_arns_with_tag("key1", "right-value")
        self.assertEqual(arns, ["arn:aws:elb:region:account-id:loadbalancer/lb1"])

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
