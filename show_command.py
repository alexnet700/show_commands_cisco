from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)

import os
from dotenv import load_dotenv

DEVICE_TYPE = "cisco_ios"
SWITCH_FILE = "switches.txt"
OUTPUT_FILE = "output.txt"

load_dotenv()

# Credentials username and password which are saved in .env
username = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')

if not username or not password:
    raise ValueError("USER_NAME or PASSWORD is missing from .env")

# Create the list of IP addresses and return it
def read_switches(filename):
    '''Read switch IP addressses from a file'''

    switches = []

    with open(filename, "r") as file:
        for line in file:
            ip = line.strip()

            if ip:
                switches.append(ip)

    return switches

def create_device(ip, username, password):
    '''Create netmiko dictionary'''

    return {
        'device_type': DEVICE_TYPE,
        'host': ip,
        'username': username,
        'password': password,
    }

# Read the list of IP addresses in switches.txt

def run_show_command(switches, command, username, password, output_filename):
    '''Run a show command on all switches'''

    print("Start script, please wait...")

    with open(output_filename, "w") as output_file:

        for ip in switches:

            try:
                print(f"Connecting to {ip}...")

                device = create_device(ip, username, password)

                with ConnectHandler(**device) as connection:
                    output = connection.send_command(command)

                output_file.write(f"\n{'=' * 60}\n")
                output_file.write(f"DEVICE: {ip}\n")
                output_file.write(f"{'=' * 60}\n")
                output_file.write(output)
                output_file.write("\n")

                print(f"{ip}: DONE")

            except NetmikoAuthenticationException as error:
                print(f"{ip}: AUTHENTICATION FAILED - {error}")

            except NetmikoTimeoutException as error:
                print(f"{ip}: CONNECTION TIMEOUT - {error}")

            except Exception as error:
                print(f"{ip}: FAILED - {error}")

def main():
    switches = read_switches(SWITCH_FILE)

    print(f"Read {len(switches)} IP addresses from file")

    run_show_command(
                switches,
                "show version",
                username,
                password,
                OUTPUT_FILE,
                )

if __name__ == "__main__":
    main()