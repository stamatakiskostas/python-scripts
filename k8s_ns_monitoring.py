import subprocess
import time
from datetime import datetime

# Define namespace and log file
namespace = "namespace"  # Replace with your namespace
log_file = "k8s_monitoring_log.txt"

# Commands and their intervals
commands = [
    {
        "cmd": ["kubectl", "-n", namespace, "get", "pods", "-o", "wide"],
        "interval": 180
    },
    {
        "cmd": ["helm3", "list", "--all", "-n", namespace],
        "interval": 180
    },
    {
        "cmd": ["kubectl", "-n", namespace, "get", "events", "--sort-by=.metadata.creationTimestamp"],
        "interval": 600
    },
    {
        "cmd": ["kubectl", "get", "resourcequotas", "-n", namespace],
        "interval": 120
    }
]

# tracking execution time of each command
last_executed = {cmd["cmd"][0]: 0 for cmd in commands}


def log_command_output(cmd_name, output):
    """Logs the output of a command with a name and timestamps to the file."""
    with open(log_file, "a") as f:
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n--- Command Start: {cmd_name} at {start_time} ---\n")
        try:
            f.write(output)
        except subprocess.CalledProcessError as e:
            f.write(f"Error executing command {cmd_name}: {e.output}\n")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"--- Command End: {cmd_name} at {end_time} ---\n")


while True:
    current_time = time.time()
    for command in commands:
        if current_time - last_executed[command["cmd"][0]] >= command["interval"]:
            output = subprocess.check_output(command["cmd"], stderr=subprocess.STDOUT, universal_newlines=True)
            log_command_output(command["cmd"][0], output)  # Pass command name and output
            last_executed[command["cmd"][0]] = current_time
    time.sleep(1)
