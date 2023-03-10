import subprocess
import argparse
import json
import os

DNS_FILE = "dns_servers.json"
DEFAULT_INTERFACE = "Wi-Fi"

def get_interfaces():
    interfaces_output = subprocess.check_output("netsh interface show interface")
    interfaces = interfaces_output.decode().split("\n")[3:-1]
    return [interface.split()[0] for interface in interfaces]

def set_dns(interface_name, primary_dns, secondary_dns):
    subprocess.run(f"netsh interface ip set dns name=\"{interface_name}\" static {primary_dns} primary", capture_output=True, text=True)
    subprocess.run(f"netsh interface ip add dns name=\"{interface_name}\" addr={secondary_dns} index=2", capture_output=True, text=True)

def load_dns_servers():
    if os.path.exists(DNS_FILE):
        with open(DNS_FILE) as f:
            return json.load(f)
    else:
        default_dns_servers = {
            "google": ["8.8.8.8", "8.8.4.4"],
            "cloudfare": ["1.1.1.1", "1.0.0.1"],
            "opendns": ["208.67.222.222", "208.67.220.220"],
            "quad9": ["9.9.9.9", "149.112.112.112"],
            "comodo": ["8.26.56.26", "8.20.247.20"],
            "electro": ['78.157.42.101', '78.157.42.100'],
            "electrodns": ["185.51.200.2", "185.51.200.3"],
            "shecan": ["178.22.122.100", "185.51.200.2"],
            "bertina": ["5.144.130.146", "5.144.130.147"],
            "bamilo": ["5.144.129.170", "5.144.129.171"],
            "faradns": ["5.144.129.190", "5.144.129.191"],
            "dibaj": ["31.7.62.66", "31.7.63.66"],
            "fanava": ["178.216.248.246", "185.55.225.25"],
            "datak": ["178.216.248.246", "178.22.123.155"],
            "parsonline": ["91.99.101.101", "91.99.99.99"],
            "rasanegar": ["79.175.176.2", "79.175.176.3"],
            "shatel": ["217.218.155.155", "217.218.147.147"]
        }
        with open(DNS_FILE, "w") as f:
            json.dump(default_dns_servers, f)
        return default_dns_servers

def add_dns_server(name, primary_dns, secondary_dns):
    dns_servers = load_dns_servers()
    dns_servers[name] = [primary_dns, secondary_dns]
    with open(DNS_FILE, "w") as f:
        json.dump(dns_servers, f)

def main():
    parser = argparse.ArgumentParser(description="Set DNS servers for a network interface")
    parser.add_argument("interface", nargs="?", default=DEFAULT_INTERFACE, help="Name of the network interface (default: Wi-Fi)")
    parser.add_argument("--list", action="store_true", help="List available network interfaces and exit")
    parser.add_argument("--dns", metavar=("PRIMARY_DNS", "SECONDARY_DNS"), help="Set the primary and secondary DNS server addresses for the interface")
    parser.add_argument("--add", metavar=("NAME", "PRIMARY_DNS", "SECONDARY_DNS"), nargs=3, help="Add a DNS server to the available list")

    args = parser.parse_args()

    if args.list:
        interfaces = get_interfaces()
        print("Available network interfaces:")
        for interface in interfaces:
            print(f" - {interface}")
        return

    if args.add:
        name, primary_dns, secondary_dns = args.add
        add_dns_server(name, primary_dns, secondary_dns)
        print(f"{name} has been added to available DNS servers")
        return

    interface_name = args.interface
    if interface_name not in get_interfaces():
        interfaces = get_interfaces()
        print(f"{interface_name} is not a valid interface. Available network interfaces:")
        for interface in interfaces:
            print(f" - {interface}")
        return

    if args.dns:
        primary_dns, secondary_dns = args.dns
    else:
        dns_servers = load_dns_servers()
        print("Available DNS servers:")
        for name, dns in dns_servers.items():
            print(f" - {name}: primary={dns[0]}, secondary={dns[1]}")
        name = input("Select a DNS server: ")
        primary_dns, secondary_dns = dns_servers[name]

    set_dns(interface_name, primary_dns, secondary_dns)
    print(f"DNS server settings for {interface_name} have been set to primary: {primary_dns}, secondary: {secondary_dns}")

if __name__ == "__main__":
    main()
    