import os
import logging
from pathlib import Path

# Configure the logger for the library
logger = logging.getLogger('utility_lib')
logger.setLevel(logging.WARNING)

# Add a default NullHandler to prevent "No handler found" warnings
logger.addHandler(logging.NullHandler())


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
    global cache
    cache_key = (directory, pattern, recursive)

    if cache_key in cache:
        logging.info(f"Using cached file list for directory {directory}")
        return cache[cache_key]

    try:
        path = Path(directory)
        if recursive:
            files = list(path.rglob(pattern))
        else:
            files = list(path.glob(pattern))
        file_list = [str(f.relative_to(directory)) for f in files]
        cache[cache_key] = file_list
        return file_list
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


def capture_directory_state(directory):
    state = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            mtime = os.path.getmtime(file_path)
            state[file_path] = mtime
    return state


def has_directory_changed(directory):
    """
    Check if the directory has changed by comparing the current state with the previous state stored in the cache.

    Args:
        directory (str): The path to the directory to check.

    Returns:
        bool: True if the directory has changed, False otherwise.
    """
    global cache

    current_state = capture_directory_state(directory)

    if directory not in cache:
        cache[directory] = current_state
        return True

    if current_state != cache[directory]:
        cache[directory] = current_state
        return True

    return False


def get_latest_files(directory, num_files=0, file_ext=None):
    """
    Get the latest files in the directory, optionally filtering by file extension and limiting the number of results.

    Args:
        directory (str): The path to the directory to list files in.
        num_files (int): The number of latest files to return. If 0, return all files. Defaults to 0.
        file_ext (str): The file extension to filter by. If None, no filtering is applied. Defaults to None.

    Returns:
        list: A list of file paths sorted by modification time, newest first.
    """
    global cache

    # Check if the directory has changed
    if has_directory_changed(directory):
        logging.info(f"Directory '{directory}' has changed. Updating cache.")
        files = []
        for root, _, file_list in os.walk(directory):
            for file in file_list:
                file_path = os.path.join(root, file)
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
