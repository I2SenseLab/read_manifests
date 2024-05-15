import json
import os
import sublist3r
import requests
import dns.resolver

def get_dns_records(url):
    dns_records = {}

    # List of DNS record types to query
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR']

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(url, record_type)
            dns_records[record_type] = [answer.to_text() for answer in answers]
        except dns.resolver.NoAnswer:
            dns_records[record_type] = []
        except dns.resolver.NXDOMAIN:
            dns_records[record_type] = []
        except dns.resolver.NoNameservers:
            dns_records[record_type] = []
        except dns.resolver.Timeout:
            dns_records[record_type] = []
        except Exception as e:
            dns_records[record_type] = [f"Error retrieving {record_type} record: {e}"]

    return dns_records

def enumerate_and_get_dns_records(domain):
    # Use Sublist3r to find subdomains
    subdomains = sublist3r.main(domain, 40, savefile=None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
    
    records_complete = {}
    for subdomain in subdomains:
        print(f"Retrieving DNS records for {subdomain}")
        records = get_dns_records(subdomain)
        if any(records.values()):
            print(f"Found records for {subdomain}: {records}")
            records_complete[subdomain] = records



    return records_complete

def load_manifest_data(dns_records):
    manifest_data = {}
    for subdomain, _ in dns_records.items():
        # Attempt to load the manifest file at the root of the subdomain
        manifest_file_url = f"https://{subdomain}/manifest.json"
        try:
            response = requests.get(manifest_file_url)
            if response.status_code == 200:
                manifest_data[subdomain] = response.json()
            else:
                manifest_data[subdomain] = f"Failed to load manifest file for {subdomain}. Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            manifest_data[subdomain] = f"Error retrieving manifest file for {subdomain}: {e}"

    return manifest_data


if __name__ == '__main__':
    domain = 'fl2f.ca'
    dns_records = enumerate_and_get_dns_records(domain)
    print(dns_records)