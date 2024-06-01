import logging
from pathlib import Path
import ujson

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global cache dictionary
json_cache = {}

def load_json(json_path):
    """
    Load JSON data from a file using ujson.

    Args:
        json_path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data, or None if an error occurs.
    """
    global json_cache

    # Check if the JSON data is in the cache
    if json_path in json_cache:
        logging.debug(f"Using cached JSON data for {json_path}")
        return json_cache[json_path]

    try:
        with open(json_path, 'r') as file:
            json_data = ujson.load(file)
            logging.debug(f"JSON data loaded from {json_path}")

            # Update the cache
            json_cache[json_path] = json_data
            return json_data
    except Exception as e:
        logging.error(f"Failed to load JSON from {json_path}: {str(e)}")
        return None

def save_json(json_path, json_data):
    """
    Save JSON data to a file using ujson.

    Args:
        json_path (str): The path to save the JSON file.
        json_data (dict): The JSON data to save.

    Returns:
        bool: True if the JSON data is saved successfully, False otherwise.
    """
    global json_cache

    try:
        with open(json_path, 'w') as file:
            ujson.dump(json_data, file)
            logging.debug(f"JSON data saved to {json_path}")

            # Update the cache
            json_cache[json_path] = json_data
            return True
    except Exception as e:
        logging.error(f"Failed to save JSON to {json_path}: {str(e)}")
        return False

def get_json_key(json_data, key, default=None):
    """
    Get a value from a JSON object by key, with an optional default value.

    Args:
        json_data (dict): The JSON data.
        key (str): The key to retrieve.
        default (any): The default value to return if the key is not found. Defaults to None.

    Returns:
        any: The value associated with the key, or the default value if the key is not found.
    """
    try:
        return json_data.get(key, default)
    except Exception as e:
        logging.error(f"Failed to get key '{key}' from JSON data: {str(e)}")
        return default

def update_json_key(json_data, key, value):
    """
    Update a value in a JSON object by key.

    Args:
        json_data (dict): The JSON data.
        key (object): The key to update.
        value (object): The new value to set for the key.

    Returns:
        bool: True if the key is updated successfully, False otherwise.
    """
    try:
        json_data[key] = value
        return True
    except TypeError as te:
        logging.error(f"Invalid key type: {type(key)}. Error: {str(te)}")
        return False
    except Exception as e:
        logging.error(f"Failed to update key '{key}' in JSON data: {str(e)}")
        return False

__all__ = ["load_json", "save_json", "get_json_key", "update_json_key"]
