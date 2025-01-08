import subprocess
from .utils import confirm_sensitive_operation


def execute_command(command):
    """Execute a terminal command in a new xterm window and return its output or error."""
    if not confirm_sensitive_operation(command):
        return "Operation canceled by the user."

    try:
        # Log in as sudo user and execute the command
        sudo_user = "rajneesh"
        sudo_password = "Rajneesh@2024"  # (Avoid using plaintext passwords like this!)

        # Command to execute as rajneesh user
        full_command = f"echo {sudo_password} | sudo -S -u {sudo_user} {command}"
        print(f"Executing: {full_command}")
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout


    except subprocess.CalledProcessError as e:
        return f"Error occurred: {e}"