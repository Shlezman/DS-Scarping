import subprocess
import time
import platform
import os

def renew_ip_address():
    """
    Detect the operating system and renew the IP address using the appropriate method.
    Requires administrator/root privileges to run.
    """
    # Detect the operating system
    operating_system = platform.system()
    print(f"Detected operating system: {operating_system}")

    if operating_system == "Windows":
        renew_ip_windows()
    elif operating_system == "Darwin":  # macOS
        renew_ip_macos()
    elif operating_system == "Linux":
        renew_ip_linux()
    else:
        print(f"Unsupported operating system: {operating_system}")
        return False

    return True


def renew_ip_windows():
    """Renew IP address on Windows systems using ipconfig."""
    # Check for admin privileges
    if not is_admin_windows():
        print("This function requires administrator privileges. Please run as administrator.")
        return False

    # Release the current IP address
    print("Releasing IP address...")
    subprocess.run("ipconfig /release", shell=True)

    # Wait a moment before requesting a new one
    time.sleep(2)

    # Request a new IP address
    print("Requesting new IP address...")
    subprocess.run("ipconfig /renew", shell=True)

    # Display the new IP configuration
    print("New IP configuration:")
    subprocess.run("ipconfig", shell=True)
    return True


def renew_ip_macos():
    """Renew IP address on macOS systems by toggling network interfaces."""
    # Check for admin privileges
    if not is_admin_unix():
        print("This function requires administrator privileges. Please run with sudo.")
        return False

    # First, identify the network interface
    result = subprocess.run("networksetup -listallnetworkservices", shell=True, capture_output=True, text=True)
    services = result.stdout.strip().split('\n')[1:]  # Skip the first line which is a header

    print(f"Available network services: {services}")

    # Usually Wi-Fi or Ethernet are the main services
    service = next((s for s in services if s in ['Wi-Fi', 'Ethernet']), services[0])

    print(f"Using network service: {service}")

    # Turn off the interface
    print(f"Turning off {service}...")
    subprocess.run(f"networksetup -setnetworkserviceenabled '{service}' off", shell=True)

    time.sleep(2)

    # Turn on the interface
    print(f"Turning on {service}...")
    subprocess.run(f"networksetup -setnetworkserviceenabled '{service}' on", shell=True)

    # Wait for the connection to be established
    print("Waiting for new IP assignment...")
    time.sleep(5)

    # Display the new IP
    print("New IP configuration:")
    subprocess.run("ifconfig", shell=True)
    return True


def renew_ip_linux():
    """Renew IP address on Linux systems by restarting network interfaces and DHCP client."""
    # Check for admin privileges
    if not is_admin_unix():
        print("This function requires root privileges. Please run with sudo.")
        return False

    # First, identify the network interface
    result = subprocess.run("ip link show | grep -v 'lo:' | grep 'state UP'",
                            shell=True, capture_output=True, text=True)

    # Parse the interface name from the output
    if not result.stdout:
        print("No active network interface found.")
        return False

    interface_line = result.stdout.strip().split('\n')[0]
    interface = interface_line.split(':')[1].strip()

    print(f"Using interface: {interface}")

    # Restart the interface to renew IP
    print("Releasing IP address...")
    subprocess.run(f"sudo ip link set {interface} down", shell=True)

    time.sleep(2)

    print("Requesting new IP address...")
    subprocess.run(f"sudo ip link set {interface} up", shell=True)

    # For DHCP specifically, you might need to restart the client
    print("Restarting DHCP client...")

    # Try different DHCP client commands (varies by distribution)
    try:
        # For distributions using dhclient
        subprocess.run(f"sudo dhclient -r {interface} && sudo dhclient {interface}", shell=True)
    except Exception as e:
        try:
            # For distributions using dhcpcd
            subprocess.run(f"sudo systemctl restart dhcpcd", shell=True)
        except Exception as e:
            print("Could not identify DHCP client. You may need to restart it manually.")

    # Wait for the connection to be established
    print("Waiting for new IP assignment...")
    time.sleep(5)

    # Display the new IP
    print("New IP configuration:")
    subprocess.run("ip addr show", shell=True)
    return True


def is_admin_windows():
    """Check if the script is running with administrator privileges on Windows."""
    try:
        return subprocess.run("net session", shell=True, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL).returncode == 0
    except:
        return False


def is_admin_unix():
    """Check if the script is running with root privileges on Unix-like systems."""
    return os.geteuid() == 0 if hasattr(os, 'geteuid') else False