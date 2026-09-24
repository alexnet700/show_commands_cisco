from netmiko import ConnectHandler
import os
from dotenv import load_dotenv
import sys

load_dotenv()

# Credentials username and password which are saved in .env
username = os.environ.get('USER_NAME')
passwd = os.environ.get('PASSWD')

data = open("switches.txt", "r")
list_of_data = []

def get_device_info(list_of_data, username, passwd):
    devices = {
        'device_type': 'cisco_ios',
        'ip': 'list_of_data',
        'username': username,
        'password': passwd,
    }

    return devices

# Read the list of IP addresses in switches.txt

def func_switch_list(delete_empty_lines=False):
    print('Reading IP addresses from file')
    with open('switches.txt', 'r') as file:
        for line in file:
            if delete_empty_lines and not line.strip():
                continue
            ip = line.strip()
            list_of_data.append(ip)
    print(f'Read {len(list_of_data)} IP addresses from file.')

def func_show_command():
    devices = get_device_info(list_of_data, username, passwd)
    print('\x1b[1;31;47m' + "Start script, please do nothing" + '\x1b[0m')
    for ip in list_of_data:
        devices['ip'] = (ip)
        ssh_connect = ConnectHandler(**devices)

        output = ssh_connect.send_command('show version')

        original_stdout = sys.stdout
        with open('func_show command.txt', 'a+') as f:
            sys.stdout = f
            print(output)
            sys.stdout = original_stdout

        print('\x1b[6;30;42m' + " DONE " + '\x1b[0m')
        ssh_connect.disconnect()
func_switch_list(delete_empty_lines=True)
func_show_command()