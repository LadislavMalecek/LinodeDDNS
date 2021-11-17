
import re
import requests
import json

def get_public_ip():
    """
    Get the public IP address.
    """
    response = requests.get('https://ipinfo.io/ip')
    htmlIP = response.text

    is_valid = re.match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$", htmlIP)
    if not is_valid:
        print("Invalid IP address")
        exit()
    return htmlIP

def call_linode_api_to_change_domain_record_ip(token, domainId, recordId, newIP):
    """
    Call the Linode API to change the IP address of a domain record.
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    url = f"https://api.linode.com/v4/domains/{domainId}/records/{recordId}"
    data = {
        "target": newIP
    }
    # call the api endpoint
    response = requests.put(url, headers=headers, data=json.dumps(data))
    return response.json()

if __name__ == "__main__":
    # read args from command line
    import argparse
    parser = argparse.ArgumentParser(description='Change IP address of domain')
    parser.add_argument('-d', '--domain-id', help='domain id', required=True)
    parser.add_argument('-r', '--record-id', help='record id', required=True)
    parser.add_argument('-t', '--token', help='linode api token', required=True)
    args = parser.parse_args()

    # call linode api to change ip address of domain
    newIP = get_public_ip()
    print(f"Public IP address: {newIP}")
    print(call_linode_api_to_change_domain_record_ip(
        args.token,
        args.domain_id,
        args.record_id,
        newIP))