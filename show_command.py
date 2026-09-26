import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from dotenv import load_dotenv
from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)

DEVICE_TYPE = "cisco_ios"
SWITCH_FILE = "switches.txt"
# Keep this modest: each worker opens its own SSH session to a switch.
MAX_WORKERS = 5

logger = logging.getLogger(__name__)


def read_switches(filename):
    """Read non-empty switch addresses from a file."""
    with open(filename, "r", encoding="utf-8") as switch_file:
        return [line.strip() for line in switch_file if line.strip()]


def create_device(ip, username, password):
    """Create the Netmiko connection parameters for a switch."""
    return {
        "device_type": DEVICE_TYPE,
        "host": ip,
        "username": username,
        "password": password,
    }


def create_output_filename(command):
    """Create a filesystem-safe output name with a unique timestamp."""
    command_name = re.sub(r"[^a-zA-Z0-9._-]+", "_", command.strip()).strip("._-")
    command_name = command_name[:80] or "show_command"
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{command_name.lower()}_{current_time}.txt"


def _run_on_switch(ip, command, username, password):
    """Return (status, output) for one switch, converting errors to results."""
    try:
        with ConnectHandler(**create_device(ip, username, password)) as connection:
            return "OK", connection.send_command(command)
    except NetmikoAuthenticationException as error:
        return "AUTHENTICATION FAILED", str(error)
    except NetmikoTimeoutException as error:
        return "CONNECTION TIMEOUT", str(error)
    except Exception as error:
        logger.exception("Unexpected failure while connecting to %s", ip)
        return "FAILED", str(error)


def run_show_command(switches, command, username, password, output_filename):
    """Run a show command concurrently and save every device result."""
    logger.info("Starting command on %d switch(es)", len(switches))
    if not switches:
        with open(output_filename, "w", encoding="utf-8"):
            pass
        return

    results = {}
    worker_count = min(MAX_WORKERS, len(switches))

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            executor.submit(_run_on_switch, ip, command, username, password): ip
            for ip in switches
        }
        for future in as_completed(futures):
            ip = futures[future]
            results[ip] = future.result()
            logger.info("%s: %s", ip, results[ip][0])

    # Write in input order even though connections finish at different times.
    with open(output_filename, "w", encoding="utf-8") as output_file:
        for ip in switches:
            status, output = results[ip]
            output_file.write(f"\n{'=' * 60}\nDEVICE: {ip}\nSTATUS: {status}\n{'=' * 60}\n")
            output_file.write(output)
            output_file.write("\n")


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    load_dotenv()
    username = os.getenv("USER_NAME")
    password = os.getenv("PASSWORD")
    if not username or not password:
        raise ValueError("USER_NAME or PASSWORD is missing from .env")

    try:
        switches = read_switches(SWITCH_FILE)
    except OSError as error:
        raise SystemExit(f"Could not read {SWITCH_FILE}: {error}") from error
    if not switches:
        raise SystemExit(f"No switch addresses found in {SWITCH_FILE}")

    logger.info("Read %d switch address(es) from %s", len(switches), SWITCH_FILE)
    command = input("Enter the command to run on all switches: ").strip()
    if not command:
        logger.info("No command entered. Exiting.")
        return

    output_filename = create_output_filename(command)
    logger.info("Command: %s", command)
    logger.info("Output file: %s", output_filename)
    run_show_command(switches, command, username, password, output_filename)


if __name__ == "__main__":
    main()
