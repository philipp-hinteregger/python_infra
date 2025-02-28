import boto3


def get_load_balancer_arns_with_tag(tag_key, tag_value, region):
    elb_client = boto3.client("elbv2", region_name=region)
    load_balancers = elb_client.describe_load_balancers()["LoadBalancers"]
    matching_load_balancer_arns = []

    for lb in load_balancers:
        lb_arn = lb["LoadBalancerArn"]
        tags = elb_client.describe_tags(ResourceArns=[lb_arn])["TagDescriptions"][0][
            "Tags"
        ]

        print(f"Tags for {lb_arn}:", tags)

        for tag in tags:
            if tag["Key"] == tag_key and tag["Value"] == tag_value:
                matching_load_balancer_arns.append(lb_arn)
                break
    print("Matching Load Balancer ARNs:", matching_load_balancer_arns)

    return matching_load_balancer_arns


def delete_load_balancers_by_arn(lb_arns, region):
    elb_client = boto3.client("elbv2", region_name=region)
    waiter = elb_client.get_waiter("load_balancers_deleted")

    for lb_arn in lb_arns:
        try:
            print(f"Deleting load balancer with ARN: {lb_arn}")
            elb_client.delete_load_balancer(LoadBalancerArn=lb_arn)
        except Exception as e:
            print(f"Error deleting load balancer {lb_arn}: {e}")

    try:
        waiter.wait(LoadBalancerArns=lb_arns)
        print("All specified load balancers have been deleted.")
    except Exception as e:
        print(f"Error waiting for load balancers to be deleted: {e}")
