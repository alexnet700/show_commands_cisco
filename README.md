# Cisco Switch Show Command Collector

Run a show command on Cisco switches and save each switch's output and status to a timestamped text file.

How to use:

1. Clone the repository:

```bash
git clone https://github.com/alexnet700/show_commands_cisco.git
```

2. Go to the project folder:

```bash
cd show_commands_cisco
```

3. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

If `venv` is not installed on Ubuntu/Debian, install the matching package for your Python version. For example:

```bash
sudo apt install python3.12-venv
```

4. Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

5. Create a `.env` file in the project folder with your device credentials:

```dotenv
USER_NAME=your_username
PASSWORD=your_password
```

6. Add one switch IP address or hostname per line in `switches.txt`.

7. Run the script and enter the show command when prompted:

```bash
python show_command.py
```

For example, enter `show version` or `show ip int br | i Vlan`. The script runs against up to five switches at a time. It writes results to a filename based on the command and run time, such as `show_version_20260926_011000_123456.txt`. Each device has a section showing its status (`OK`, `AUTHENTICATION FAILED`, `CONNECTION TIMEOUT`, or `FAILED`) and command output or error details. Progress and failures are also logged in the terminal.
