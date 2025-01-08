
from .executer import execute_command

def run_command(command):
    """Run a command and return its result."""
    result = execute_command(command)
    return result
