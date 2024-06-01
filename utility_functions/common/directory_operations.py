import os
import logging
import json
from pathlib import Path
import glob

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

cache = {}

def ensure_dir(directory):
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        directory (str): The path to the directory to ensure exists.

    Raises:
        Exception: If there is an error creating the directory.
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logging.info(f"Directory '{directory}' ensured.")
    except Exception as e:
        logging.error(f"Failed to ensure directory {directory}: {str(e)}")

def list_files(directory, pattern="*", recursive=False):
    """
    List all files in a directory matching the pattern, optionally recursing through subdirectories.

    Args:
        directory (str): The path to the directory to list files in.
        pattern (str): The pattern to match files against. Defaults to "*".
        recursive (bool): Whether to list files recursively. Defaults to False.

    Returns:
        list: A list of relative file paths matching the pattern.

    Raises:
        Exception: If there is an error listing the files.
    """
    try:
        path = Path(directory)
        if recursive:
            files = list(path.rglob(pattern))
        else:
            files = list(path.glob(pattern))
        return [str(f.relative_to(directory)) for f in files]
    except Exception as e:
        logging.error(f"Error listing files in {directory}: {str(e)}")
        return []

def setup_directories(config):
    """
    Ensure all directories specified in the configuration exist.

    Args:
        config (dict): A dictionary where the values are paths to directories to ensure exist.

    Raises:
        Exception: If there is an error creating any of the directories.
    """
    try:
        for path in config.values():
            Path(path).mkdir(parents=True, exist_ok=True)
        logging.info("All directories set up successfully.")
    except Exception as e:
        logging.error(f"Failed to set up directories: {str(e)}")

def has_directory_changed(directory, state_file):
    """
    Check if the directory has changed by comparing the current state with the previous state stored in a file.
    """
    if not os.path.exists(state_file):
        return True

    with open(state_file, 'r') as file:
        previous_state = json.load(file)

    current_state = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            mtime = os.path.getmtime(file_path)
            current_state[file_path] = mtime

    if current_state != previous_state:
        with open(state_file, 'w') as file:
            json.dump(current_state, file)
        return True

    return False

def get_latest_files(directory, num_files=0, file_ext=None, state_file="directory_state.json"):
    """
    Get the latest files in the directory, optionally filtering by file extension and limiting the number of results.

    Args:
        directory (str): The path to the directory to list files in.
        num_files (int): The number of latest files to return. If 0, return all files. Defaults to 0.
        file_ext (str): The file extension to filter by. If None, no filtering is applied. Defaults to None.
        state_file (str): The path to the state file to check for directory changes.

    Returns:
        list: A list of file paths sorted by modification time, newest first.
    """
    global cache

    # Check if the directory has changed
    if has_directory_changed(directory, state_file):
        logging.info(f"Directory '{directory}' has changed. Updating cache.")
        files = []
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if not os.path.isfile(file_path):
                continue
            if file_ext is None or file.lower().endswith(file_ext):
                files.append((file_path, os.path.getmtime(file_path)))

        # Sort the files based on modification time (newest first)
        files.sort(key=lambda x: x[1], reverse=True)

        # Update the cache
        cache[directory] = files
    else:
        logging.info(f"Using cached data for directory '{directory}'.")
        files = cache[directory]

    # Limit the number of files if num_files is specified
    if num_files > 0:
        files = files[:num_files]

    return [file[0] for file in files]

__all__ = ['ensure_dir', 'list_files', 'setup_directories', 'has_directory_changed', 'get_latest_files']
