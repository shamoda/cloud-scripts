from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from datetime import datetime

def create_nsg(group_name, location, resource_group_name, subscription_id):
    credentials = DefaultAzureCredential()
    network_client = NetworkManagementClient(credentials, subscription_id)
    
    nsg_params = {
        'location': location
    }

    nsg_poller = network_client.network_security_groups.begin_create_or_update(
        resource_group_name, group_name, nsg_params)
    nsg = nsg_poller.result()

    return nsg

def add_nsg_rule(group_name, resource_group_name, num_rules, subscription_id):
    credentials = DefaultAzureCredential()
    network_client = NetworkManagementClient(credentials, subscription_id)
    
    for i in range(num_rules):
        security_rule = {
            'name': f'NSG_Rule_{i+1}',
            'protocol': 'Tcp',
            'source_port_range': '*',
            'destination_port_range': str(80+i),
            'source_address_prefix': '*',
            'destination_address_prefix': '*',
            'access': 'Allow',
            'priority': 100 + i,
            'direction': 'Inbound'
        }

        rule_poller = network_client.security_rules.begin_create_or_update(
            resource_group_name, group_name, f'NSG_Rule_{i+1}', security_rule)
        rule = rule_poller.result()

def main():
    group_name = "Network Security Group"
    location = 'East US'
    resource_group_name = 'test-rg'

    num_rules = int(input("Enter the number of NSG rules to attach (1 or 3): "))
    if num_rules not in [1, 3]:
        print("Invalid input. Please enter 1 or 3.")
        return

    start_time = datetime.now()

    nsg = create_nsg(group_name, location, resource_group_name, "b690e026-1009-4d60-817d-b045c4afb00e")
    print("Created NSG:", nsg.name)

    add_nsg_rule(group_name, resource_group_name, num_rules, "b690e026-1009-4d60-817d-b045c4afb00e")

    end_time = datetime.now()

    duration = end_time - start_time
    print("Time taken to provision resources:", duration)

if __name__ == "__main__":
    main()
