import os
import logging
import ujson as json  # Use ujson for faster JSON operations
from pathlib import Path

# Configure the logger for the library
logger = logging.getLogger('utility_lib')
logger.setLevel(logging.WARNING)
logger.addHandler(logging.NullHandler())

# Global cache dictionary
cache = {}

# Static directory to store state files
STATEFILES_DIR = Path(__file__).parent / "statefiles"
STATEFILES_DIR.mkdir(parents=True, exist_ok=True)

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
            ensure_dir(path)
        logger.info("All directories set up successfully.")
    except Exception as e:
        logger.error(f"Failed to set up directories: {str(e)}")
        raise

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
    except Exception as e:
        logger.error(f"Failed to ensure directory {directory}: {str(e)}")
        raise

def capture_directory_state(directory):
    """
    Capture the current state of a directory by storing file paths and modification times in a dictionary.

    Args:
        directory (str): The path to the directory to capture the state of.

    Returns:
        dict: A dictionary containing file paths as keys and modification times as values.
    """
    state = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            mtime = os.path.getmtime(file_path)
            state[file_path] = mtime
    return state

def get_state_file_path(directory):
    """
    Generate a state file path based on the monitored directory.

    Args:
        directory (str): The path to the directory to generate the state file path for.

    Returns:
        Path: The path to the state file.
    """
    directory_name = directory.replace("/", "_").replace("\\", "_").strip("_")
    return STATEFILES_DIR / f"{directory_name}_state.json"

def has_directory_changed(directory):
    """
    Check if a directory has changed by comparing the current state with the cached state.

    Args:
        directory (str): The path to the directory to check.

    Returns:
        bool: True if the directory has changed, False otherwise.
    """
    state_file = get_state_file_path(directory)

    if not state_file.exists():
        state_file.touch()
        with state_file.open('w') as file:
            json.dump({}, file)
        return False  # Assume no change for a new state file

    with state_file.open('r') as file:
        previous_state = json.load(file)

    current_state = capture_directory_state(directory)

    if current_state != previous_state:
        with state_file.open('w') as file:
            json.dump(current_state, file)
        return True

    return False

def list_files(directory, pattern="*", recursive=False):
    """
    List all files in a directory matching the pattern, optionally recursing through subdirectories.

    Args:
        directory (str): The path to the directory to list files in.
        pattern (str): The pattern to match files against. Defaults to "*".
        recursive (bool): Whether to list files recursively. Defaults to False.

    Returns:
        dict: A dictionary containing file paths as keys and modification times as values.

    Raises:
        Exception: If there is an error listing the files.
    """
    global cache
    cache_key = (directory, pattern, recursive)

    if cache_key in cache:
        return cache[cache_key]

    try:
        path = Path(directory)
        if recursive:
            files = path.rglob(pattern)
        else:
            files = path.glob(pattern)

        file_dict = {str(f.absolute()): os.path.getmtime(f) for f in files if f.is_file()}
        cache[cache_key] = file_dict
        return file_dict
    except Exception as e:
        logger.error(f"Error listing files in {directory}: {str(e)}")
        raise

def get_latest_files(directory, num_files=0, file_ext=None):
    """
    Get the latest files in the directory, optionally filtering by file extension and limiting the number of results.

    Args:
        directory (str): The path to the directory to list files in.
        num_files (int): The number of latest files to return. If 0, return all files. Defaults to 0.
        file_ext (str, optional): The file extension to filter by. If None, no filtering is applied. Defaults to None.

    Returns:
        list: A list of file paths sorted by modification time, newest first.
    """
    global cache

    # Check if the directory has changed
    directory_changed = has_directory_changed(directory)

    if directory_changed or directory not in cache:
        files = list_files(directory)
        cache[directory] = files
    else:
        files = cache[directory]

    # Filter files by the specified extension using str.endswith()
    if file_ext:
        filtered_files = {file: mtime for file, mtime in files.items() if file.lower().endswith(file_ext.lower())}
    else:
        filtered_files = files

    # Sort the filtered files based on modification time (newest first)
    sorted_files = sorted(filtered_files.items(), key=lambda x: x[1], reverse=True)

    # Limit the number of files if num_files is specified
    if num_files > 0:
        sorted_files = sorted_files[:num_files]

    # Extract only the file paths from the sorted files
    latest_files = [file for file, _ in sorted_files]

    # Update the cache with the latest files and their modification times
    cache[(directory, '*', False)] = {file: mtime for file, mtime in sorted_files}

    return latest_files

def clear_cache():
    """
    Clear the global cache.

    This function is primarily used for testing purposes to ensure the cache is reset.
    """
    global cache
    cache.clear()


__all__ = ['ensure_dir', 'list_files', 'setup_directories', 'has_directory_changed', 'get_latest_files', 'clear_cache']
