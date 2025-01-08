def confirm_sensitive_operation(command):
    """Prompt user to confirm sensitive operations."""
    if any(keyword in command.lower() for keyword in ["rm", "delete", "drop"]):
        response = input(f"The command '{command}' might perform a sensitive operation. Proceed? (y/n): ").strip().lower()
        return response == 'y'
    return True
