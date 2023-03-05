#Library # /bin/python3 -m pip install -U autopep8  : Format the python code
import boto3
from botocore.exceptions import ClientError
import re

# AWS session creation
session = boto3.Session(region_name="us-east-1")

ec2 = session.client('ec2')

response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

try:
    response = ec2.create_security_group(GroupName='SECURITY_GROUP_NAME',
                                         Description='DESCRIPTION',
                                         VpcId=vpc_id)
    security_group_id = response['GroupId']
    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0','Description': 'string'}]
            'Ipv6Ranges': [{'CidrIpv6': '::/0','Description': 'string'}]
             }
        ])
    print('Ingress Successfully Set %s' % data)
except ClientError as e:
    print(e)