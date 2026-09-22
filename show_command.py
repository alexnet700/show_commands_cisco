from netmiko import ConnectHandler
import os
from dotenv import load_dotenv

load_dotenv()

username = os.environ.get('USER_NAME')
passwd = os.environ.get('PASSWD')

SWACC02 = {
    'device_type': 'cisco_ios',
    'host': '192.168.100.14',
    'username': username,
    'password': passwd
}

SWDIST01 = {
    'device_type': 'cisco_ios',
    'host': '192.168.100.12',
    'username': username,
    'password': passwd
}

SWCORE01 = {
    'device_type': 'cisco_ios',
    'host': '192.168.100.11',
    'username': username,
    'password': passwd
}


for device in (SWACC02, SWDIST01, SWCORE01):
    print(f"\nConnecting {device['host']}...")
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command('show version', read_timeout = 60)
    print(output)
    print(f"\nClosing connection {device['host']}...")
    net_connect.disconnect()