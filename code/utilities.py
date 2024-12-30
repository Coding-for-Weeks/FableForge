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
    log_file = "game.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    if not os.access(log_file, os.W_OK):
        print(f"Warning: Cannot write to log file {log_file}. Check file permissions.")

setup_logging()