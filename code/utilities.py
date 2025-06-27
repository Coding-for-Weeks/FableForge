import os
import platform
import subprocess
import logging

# Utility Functions
def clear_console():
    commands = {
        "Windows": "cls",
        "Linux": "clear",
        "Darwin": "clear",  # macOS
    }
    command = commands.get(platform.system(), "clear")
    subprocess.run(command, shell=True)

def exiting():
    clear_console()
    os._exit(0)

def setup_logging():
    """Configure error logging and ensure the log directory exists."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(root_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "game.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    if not os.access(log_file, os.W_OK):
        print(
            f"Warning: Cannot write to log file {log_file}. Check file permissions."
        )

