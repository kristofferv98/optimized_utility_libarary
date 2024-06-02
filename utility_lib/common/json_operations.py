import logging
import ujson
import time
from collections import OrderedDict

# Configure the logger for the library
logger = logging.getLogger('utility_lib')
logger.setLevel(logging.WARNING)

# Add a default NullHandler to prevent "No handler found" warnings
logger.addHandler(logging.NullHandler())

class LRUCache:
    def __init__(self, capacity: int = 128, ttl: int = 60):
        self.capacity = capacity
        self.ttl = ttl
        self.cache = OrderedDict()
        self.timestamps = {}

    def get(self, key):
        if key in self.cache:
            if time.time() - self.timestamps[key] > self.ttl:
                # Cache expired
                self.cache.pop(key)
                self.timestamps.pop(key)
                return None
            self.cache.move_to_end(key)  # Mark as recently used
            return self.cache[key]
        return None

    def set(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        self.timestamps[key] = time.time()
        if len(self.cache) > self.capacity:
            oldest_key = next(iter(self.cache))
            self.cache.pop(oldest_key)
            self.timestamps.pop(oldest_key)

# Global cache instance
json_cache = LRUCache(capacity=128, ttl=60)

def load_json(json_path):
    """
    Load JSON data from a file using ujson.

    Args:
        json_path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data, or None if an error occurs.
    """
    cached_data = json_cache.get(json_path)
    if cached_data is not None:
        logger.debug(f"Using cached JSON data for {json_path}")
        return cached_data

    try:
        with open(json_path, 'r') as file:
            json_data = ujson.load(file)
            logger.debug(f"JSON data loaded from {json_path}")

            # Update the cache
            json_cache.set(json_path, json_data)
            return json_data
    except Exception as e:
        logger.error(f"Failed to load JSON from {json_path}: {str(e)}")
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
    try:
        with open(json_path, 'w') as file:
            ujson.dump(json_data, file)
            logger.debug(f"JSON data saved to {json_path}")

            # Update the cache
            json_cache.set(json_path, json_data)
            return True
    except Exception as e:
        logger.error(f"Failed to save JSON to {json_path}: {str(e)}")
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
        logger.error(f"Failed to get key '{key}' from JSON data: {str(e)}")
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
        logger.error(f"Invalid key type: {type(key)}. Error: {str(te)}")
        return False
    except Exception as e:
        logger.error(f"Failed to update key '{key}' in JSON data: {str(e)}")
        return False

__all__ = ["load_json", "save_json", "get_json_key", "update_json_key"]
