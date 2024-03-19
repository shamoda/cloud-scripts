import boto3
import time

def create_security_group(group_name, description):
    ec2 = boto3.client('ec2', region_name='us-east-1')
    response = ec2.create_security_group(
        GroupName=group_name,
        Description=description
    )
    return response['GroupId']

def authorize_security_group_ingress(group_id, ip_protocol, from_port, to_port, cidr_ip):
    ec2 = boto3.client('ec2', region_name='us-east-1')
    ec2.authorize_security_group_ingress(
        GroupId=group_id,
        IpPermissions=[
            {
                'IpProtocol': ip_protocol,
                'FromPort': from_port,
                'ToPort': to_port,
                'IpRanges': [{'CidrIp': cidr_ip}]
            }
        ]
    )

def main():
    group_name = "AWS-SG"
    description = "AWS-SG-Description"
    ip_protocol = 'tcp'
    from_port = 80
    to_port = 80
    cidr_ip = '0.0.0.0/0'
    
    num_rules = int(input("Enter the number of security group rules to attach (1 or 3): "))
    if num_rules not in [1, 3]:
        print("Invalid input. Please enter 1 or 3.")
        return

    start_time = time.time()

    group_id = create_security_group(group_name, description)
    print("Created security group with ID:", group_id)

    for i in range(num_rules):
        authorize_security_group_ingress(group_id, ip_protocol, from_port+i, to_port+i, cidr_ip)
        print(f"Ingress rule {i+1} added to security group")

    end_time = time.time()

    duration = end_time - start_time
    print("Time taken to provision resources:", duration, "seconds")

if __name__ == "__main__":
    main()
