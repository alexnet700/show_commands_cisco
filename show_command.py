from netmiko import ConnectHandler
import os
from dotenv import load_dotenv

load_dotenv()

# Credentials username and password which are saved in .env
username = os.environ.get('USER_NAME')
passwd = os.environ.get('PASSWD')

def read_switches(filename):
    '''Read switch IP addressses from a file'''

    switches = []

    with open(filename, "r") as file:
        for line in file:
            ip = line.strip()

            if ip:
                switches.append(ip)

    return switches

def create_device(ip, username, passwd):
    '''Create netmiko dictionary'''

    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': passwd,
    }

    return device

# Read the list of IP addresses in switches.txt

def run_show_command(switches, command):
    '''Run a show command on all switches'''

    print("Start script, please wait...")

    with open("output.txt", "w") as output_file:

        for ip in switches:
            print(f"Connecting to {ip}...")

            device = create_device(ip, username, passwd)

            connection = ConnectHandler(**device)

            output = connection.send_command(command)

            output_file.write(f"\n{'=' * 60}\n")
            output_file.write(f"DEVICE: {ip}\n")
            output_file.write(f"{'=' * 60}\n")
            output_file.write(output)
            output_file.write("\n")

            connection.disconnect()

            print(f"{ip}: DONE")

switches = read_switches("switches.txt")
print(f"Read {len(switches)} IP addresses from file")

run_show_command(switches, "show version")