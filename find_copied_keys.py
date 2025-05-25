#!/usr/bin/env python3
import re
from collections import defaultdict
import sys

def analyze_ssh_connections(log_file='/var/log/auth.log'):
    """
    Analyze SSH connections to detect key reuse across multiple IPs
    Returns dict of fingerprints with their associated IPs and usernames
    Format: {fingerprint: {'ips': set(), 'usernames': set()}}
    """
    fingerprint_data = defaultdict(lambda: {'ips': set(), 'usernames': set()})
    
    # Regex pattern to match the SSH publickey acceptance lines
    ssh_pattern = re.compile(
        r'Accepted publickey for (\w+) from ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) port \d+ ssh2: (\w+) SHA256:([a-zA-Z0-9/+]+={0,2})'
    )

    try:
        with open(log_file, 'r') as f:
            for line in f:
                match = ssh_pattern.search(line)
                if match:
                    username, ip, key_type, fingerprint = match.groups()
                    fingerprint_data[fingerprint]['ips'].add(ip)
                    fingerprint_data[fingerprint]['usernames'].add(username)
    except FileNotFoundError:
        print(f"Error: Could not open {log_file}", file=sys.stderr)
        sys.exit(1)

    return fingerprint_data

def generate_report(fingerprint_data):
    """Generate a report of suspicious key reuse"""
    # Filter for fingerprints used from multiple IPs
    suspicious_keys = {
        fp: data for fp, data in fingerprint_data.items() 
        if len(data['ips']) > 1
    }

    if not suspicious_keys:
        print("No SSH key reuse detected (all keys used from single IP)")
        return

    print("SSH KEY REUSE DETECTED - POTENTIAL SECURITY ISSUE")
    print("=" * 60)
    print("The following SSH keys were used from multiple IP addresses:\n")

    for fingerprint, data in sorted(suspicious_keys.items(), 
                                 key=lambda x: len(x[1]['ips']), reverse=True):
        print(f"Fingerprint (SHA256): {fingerprint}")
        print(f"Key Type: {next(iter(data['usernames']))}")  # Get key type from first username
        print(f"Associated Usernames: {', '.join(sorted(data['usernames']))}")
        print(f"Used from {len(data['ips'])} different IP addresses:")
        for ip in sorted(data['ips']):
            print(f"  - {ip}")
        print()

if __name__ == "__main__":
    print("Analyzing SSH key usage patterns...\n")
    fingerprints = analyze_ssh_connections()
    generate_report(fingerprints)

