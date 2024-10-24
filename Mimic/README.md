# MAC Address Mimic

A Python script for network pentesters to dynamically change their MAC address, either by hopping between devices on a network or by continuously randomizing the MAC address.

## Features

- **MAC Address Randomization**: Automatically randomizes your MAC address every few seconds.
- **Device Hopping**: Mimics devices found on the network by adopting their MAC addresses.
- **DHCP Lease Renewal**: Automatically renews your DHCP lease after each MAC change to prevent disconnection.
- **Gratuitous ARP Broadcast**: Sends a gratuitous ARP message after each MAC change to announce your presence to the network and avoid getting booted.
- **Interactive CLI**: Select your network interface, set network ranges, and blacklist certain MAC addresses.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/IlyVoid/ToolBox.git
    ```
2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    Make sure you have the necessary system dependencies installed (`ip`, `dhclient`).

3. Run the script with root privileges:
    ```bash
    sudo python3 mimic.py
    ```

## Usage

When you run the script, you will be prompted to select a network interface, specify a network range, and blacklist any devices you don't want to mimic. Then, choose one of the following modes:

1. **Device Hopping**: The script will scan the network for devices and continuously mimic their MAC addresses.
2. **MAC Randomization**: The script will randomize your MAC address every few seconds.

## Example

```bash
sudo python3 mimic.py
```

- Select your network interface (e.g., `eth0`).
- Enter the network range (e.g., `192.168.1.0/24`).
- Enter MAC addresses to blacklist, if any (comma-separated).
- Choose between device hopping or MAC randomization.

## Requirements

- Python 3
- `scapy`
- `netifaces`
- `rich`

## Important Notes

- **Root Access**: The script requires root privileges to change MAC addresses and manage network interfaces.
- **Network Disconnection**: Some networks may still disconnect you when you change your MAC. The script attempts to avoid this by renewing DHCP leases and sending ARP broadcasts, but no guarantees on highly secure networks.

## License

This project is licensed under the MIT License.
```
