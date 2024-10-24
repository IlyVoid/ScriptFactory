import subprocess
import time
import random
import os
import shutil
import signal
import logging
from scapy.all import ARP, Ether, srp
from rich.console import Console
from rich.prompt import Prompt
import netifaces

# Initialize console and logger
console = Console()
logging.basicConfig(filename='mimic.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Store original MAC to revert later
original_mac = None

def clear_terminal():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def log_event(message, level="info"):
    """Log an event."""
    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)
    console.print(message)

def get_mac(interface):
    """Get the current MAC address of the specified interface."""
    output = subprocess.run(["ip", "link", "show", interface], capture_output=True, text=True)
    for line in output.stdout.splitlines():
        if "link/ether" in line:
            return line.split()[1]
    return None

def change_mac(interface, new_mac):
    """Change the MAC address of the specified interface and handle network reconnection."""
    global original_mac
    try:
        if not original_mac:
            original_mac = get_mac(interface)

        log_event(f"[yellow]Changing MAC address of {interface} to {new_mac}...[/yellow]")
        subprocess.run(["ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["ip", "link", "set", interface, "address", new_mac], check=True)
        subprocess.run(["ip", "link", "set", interface, "up"], check=True)
        
        log_event("[green]MAC address changed successfully![/green]")
        
        # Renew DHCP and announce new MAC with gratuitous ARP
        renew_dhcp(interface)
        send_gratuitous_arp(interface)

    except subprocess.CalledProcessError:
        log_event("[red]Failed to change MAC address![/red]", level="error")

def revert_mac(interface):
    """Revert to the original MAC address."""
    if original_mac:
        log_event(f"[yellow]Reverting MAC address to {original_mac}...[/yellow]")
        change_mac(interface, original_mac)

def is_connected(interface):
    """Check if the network interface is connected."""
    output = subprocess.run(["ip", "addr", "show", interface], capture_output=True, text=True)
    return "state UP" in output.stdout

def reconnect(interface):
    """Reconnect the network interface."""
    log_event(f"[yellow]Reconnecting {interface}...[/yellow]")
    try:
        subprocess.run(["ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["ip", "link", "set", interface, "up"], check=True)
        subprocess.run(["dhclient", interface], check=True)
        log_event(f"[green]{interface} reconnected successfully![/green]")
    except subprocess.CalledProcessError:
        log_event(f"[red]Failed to reconnect {interface}. Check your network setup![/red]", level="error")

def ping_device(ip):
    """Ping a device to check if it's alive."""
    try:
        subprocess.run(["ping", "-c", "1", "-W", "2", ip], check=True, stdout=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def discover_devices(network_range):
    """Discover devices on the specified network range."""
    arp = ARP(pdst=network_range)
    ether = Ether(dst='ff:ff:ff:ff:ff:ff')
    packet = ether / arp

    log_event("[green]Scanning for devices...[/green]")
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return devices

def random_mac():
    """Generate a random MAC address."""
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(5))

def mac_randomization_mode(interface):
    """Randomize the MAC address continuously."""
    while True:
        new_mac = random_mac()
        log_event(f"[yellow]Randomizing MAC to {new_mac}...[/yellow]")
        change_mac(interface, new_mac)
        time.sleep(random.randint(10, 30))

def hop_device(interface, network_range, blacklist):
    """Continuously hop between devices on the network."""
    log_event("[blue]Starting device hop...[/blue]")
    while True:
        if not is_connected(interface):
            reconnect(interface)
            time.sleep(5)  # Wait a bit before checking again

        devices = discover_devices(network_range)
        if not devices:
            log_event("[red]No devices found. Retrying...[/red]")
            time.sleep(5)
            continue

        for device in devices:
            if device['mac'] in blacklist:
                log_event(f"[yellow]Skipping blacklisted device {device['ip']}...[/yellow]")
                continue

            if not is_connected(interface):
                reconnect(interface)
                time.sleep(5)

            if ping_device(device['ip']):
                change_mac(interface, device['mac'])
                log_event(f"[cyan]Now mimicking {device['ip']} with MAC {device['mac']}[/cyan]")
                time.sleep(random.randint(10, 30))
            else:
                log_event(f"[red]Device {device['ip']} is not responding. Skipping...[/red]")

def validate_commands():
    """Validate necessary system commands are available."""
    if shutil.which('ip') is None:
        log_event("[red]The 'ip' command is required but not found![/red]", level="error")
        exit(1)
    if shutil.which('dhclient') is None:
        log_event("[red]The 'dhclient' command is required but not found![/red]", level="error")
        exit(1)

def check_root():
    """Check if the script is being run with root privileges."""
    if os.geteuid() != 0:
        log_event("[red]This script requires root privileges. Run as root![/red]", level="error")
        exit(1)

def list_interfaces():
    """List available network interfaces."""
    return netifaces.interfaces()

def handle_sigint(signal_received, frame):
    """Handle SIGINT (Ctrl+C) to gracefully exit."""
    log_event("[yellow]SIGINT received. Reverting MAC address and exiting...[/yellow]")
    revert_mac(interface)
    exit(0)

def renew_dchp(interface):
    """Renew DHCP lease after changing MAC address."""
    log_event(f"[yellow]Renewing DHCP lease for {interface}...[/yellow]")
    try:
        subprocess.run(["dhclient", "-r", interface], check=True)  # Release current DHCP lease
        subprocess.run(["dhclient", interface], check=True)  # Request new DHCP lease
        log_event(f"[green]DHCP lease renewed successfully for {interface}![/green]")
    except subprocess.CalledProcessError:
        log_event(f"[red]Failed to renew DHCP lease on {interface}.[/red]", level="error")

def send_gratuitous_arp(interface):
    """Send gratuitous ARP to announce the new MAC address."""
    try:
        mac_addr = get_mac(interface)
        ip_addr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
        log_event(f"[yellow]Sending gratuitous ARP for IP {ip_addr} with MAC {mac_addr}...[/yellow]")
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=2, psrc=ip_addr, hwsrc=mac_addr, pdst=ip_addr, hwdst="ff:ff:ff:ff:ff:ff")
        srp(packet, timeout=1, verbose=0)
        log_event(f"[green]Gratuitous ARP sent successfully![/green]")
    except KeyError:
        log_event(f"[red]Failed to obtain IP address for interface {interface}.[/red]", level="error")

def main():
    clear_terminal()
    validate_commands()
    check_root()

    signal.signal(signal.SIGINT, handle_sigint)

    # Interactive menu
    interfaces = list_interfaces()
    interface = Prompt.ask(f"Select your network interface", choices=interfaces)

    network_range = Prompt.ask("Enter the network range (e.g., 192.168.1.0/24)", default="192.168.1.0/24")

    blacklist = Prompt.ask("Enter any MAC addresses to blacklist (comma-separated)", default="").split(",")

    mode = Prompt.ask("Choose mode: 1) Device Hopping 2) MAC Randomization", choices=["1", "2"])

    if mode == "1":
        hop_device(interface, network_range, blacklist)
    else:
        mac_randomization_mode(interface)

if __name__ == "__main__":
    main()
