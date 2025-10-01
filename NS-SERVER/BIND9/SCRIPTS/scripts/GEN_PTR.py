# GEN_PTR.py
#!/usr/bin/env python3
import sys
from datetime import datetime

def gen_zone(network, domain, special_hosts=None):
    today = datetime.now().strftime("%Y%m%d%H")
    rev_zone = ".".join(reversed(network.split('.')[:-1])) + ".in-addr.arpa"

    print(f"$TTL 86400")
    print(f"@   IN  SOA ns.{domain}. noc.{domain}. (")
    print(f"        {today} ; Serial")
    print(f"        3600       ; Refresh")
    print(f"        1800       ; Retry")
    print(f"        1209600    ; Expire")
    print(f"        86400 )    ; Minimum TTL\n")
    print(f"@   IN  NS  ns.{domain}.")
    print(f"@   IN  NS  ns1.{domain}.\n")

    for i in range(1, 255):
        hostname = f"host{i}.{domain}"
        if special_hosts and i in special_hosts:
            hostname = special_hosts[i]
        print(f"{i}   IN PTR {hostname}.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: gen_ptr.py <network> <domain>")
        sys.exit(1)

    network = sys.argv[1]  # например 145.100.222.0
    domain = sys.argv[2]   # happylink.com

    # Маппинг "особых" PTR-записей
    special_hosts = {
        1: "ns.happylink.net.ua.",
        10: "www.happylink.net.ua.",
        20: "mail.happylink.net.ua."
    } if "145" in network else {
        1: "ns1.happylink.net.ua.",
        10: "api.happylink.net.ua."
    }

    gen_zone(network, domain, special_hosts)
