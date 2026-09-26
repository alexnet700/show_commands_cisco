Script that captures the output of any show command from the cisco switches and save it in a text file.

How to use:

1. In your local folder on your pc, clone the github repo

```git clone https://github.com/alexnet700/show_commands_cisco.git```

2. Go to the folder created after cloning

```cd show_commands_cisco```

3. Create a python virtual env

```python3 -m venv venv```

If you don't have venv installed run this first:

```sudo apt install python3.12-venv -y```

4. Activate the python virtual env

```source venv/bin/activate```

5. Install the requirements

```pip3 install -r requirements.txt```

6. Create the .env for your credentials

```nano .env```

Enter the username and password of the devices:

USER_NAME=your_username
PASSWORD=your_password

7. Add you switches IP addresses in switches.txt file

8. Run the script:

```python3 show_command.py```

Then at the prompt 
Enter the command to run on all switches: ```show version```

Example: show version, show ip int br | i Vlan ..etc

Command is run on all the switches and the file is saved this format:

show_version_092626_0110am.txt