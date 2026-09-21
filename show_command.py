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

net_connect = ConnectHandler(**SWACC02)
print(f"Connecting {SWACC02['host']}...")
output = net_connect.send_command('show version', read_timeout = 60)
print(output)

print("Closing connection...")
net_connect.disconnect()