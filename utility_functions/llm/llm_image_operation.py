import os
import logging
import json
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define resampling method
resampling = getattr(Image, 'Resampling', Image).LANCZOS

# Global cache dictionary
cache = {}

def has_directory_changed(directory, state_file):
    """
    Check if the directory has changed by comparing the current state with the previous state stored in a file.

    Args:
        directory (str): The path to the directory to check.
        state_file (str): The path to the state file that stores the previous directory state.

    Returns:
        bool: True if the directory has changed, False otherwise.
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
        state_file (str): The path to the state file to check for directory changes. Defaults to "directory_state.json".

    Returns:
        list: A list of file paths sorted by modification time, newest first.
    """
    global cache

    # Check if the directory has changed
    if has_directory_changed(directory, state_file):
        logging.debug(f"Directory '{directory}' has changed. Updating cache.")
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
        logging.debug(f"Using cached data for directory '{directory}'.")
        files = cache[directory]

    # Limit the number of files if num_files is specified
    if num_files > 0:
        files = files[:num_files]

    return [file[0] for file in files]

def revise_image_for_llm(image_path, mode, output_path=None):
    """
    Resize the image based on the specified mode ('low' or 'high').

    Args:
        image_path (str): The path to the image file to resize.
        mode (str): The resize mode ('low' for 512x512, 'high' for a maximum dimension of 2048).
        output_path (str, optional): The path to save the resized image. If None, the original image is overwritten.

    Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the mode is not 'low' or 'high'.
        Exception: For other errors that occur during image processing.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at {image_path}")

    if mode not in ['low', 'high']:
        raise ValueError("Mode should be either 'low' or 'high'.")

    try:
        with Image.open(image_path) as img:
            if mode == 'low':
                new_size = (512, 512)
                img = img.resize(new_size, resampling)
            else:  # mode == 'high'
                width, height = img.size
                max_size = 2048
                if width > max_size or height > max_size:
                    if width > height:
                        new_width = max_size
                        new_height = int(height * (max_size / width))
                    else:
                        new_height = max_size
                        new_width = int(width * (max_size / height))
                    img = img.resize((new_width, new_height), resampling)

            if output_path:
                img.save(output_path)
            else:
                img.save(image_path)

    except Exception as e:
        logging.error(f"Failed to revise image at {image_path}: {str(e)}")
        raise e

def batch_revise_images_for_llm(image_paths, mode, output_paths=None, max_workers=10):
    """
    Batch process images to resize them based on the specified mode.

    Args:
        image_paths (list): A list of paths to the image files to resize.
        mode (str): The resize mode ('low' or 'high').
        output_paths (list, optional): A list of paths to save the resized images. If None, the original images are overwritten.
        max_workers (int): The maximum number of worker threads to use. Defaults to 10.

    Raises:
        ValueError: If the number of image paths and output paths do not match.
    """
    if output_paths and len(image_paths) != len(output_paths):
        raise ValueError("Number of image paths and output paths must match.")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i in range(len(image_paths)):
            image_path = image_paths[i]
            output_path = output_paths[i] if output_paths else None
            futures.append(executor.submit(revise_image_for_llm, image_path, mode, output_path))

        for future in futures:
            future.result()

def process_last_n_images(folder_path, num_images, output_folder, quality, max_workers=10):
    """
    Process the last n images in the specified folder, resizing them based on the specified quality.

    Args:
        folder_path (str): The path to the folder containing the images.
        num_images (int): The number of latest images to process.
        output_folder (str): The path to the folder where resized images will be saved.
        quality (str): The quality mode for resizing ('low' or 'high').
        max_workers (int): The maximum number of worker threads to use. Defaults to 10.

    Returns:
        list: A list of paths to the resized images.
    """
    # Get the list of JPG files in the folder
    jpg_files = get_latest_files(folder_path, num_images, '.jpg')

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Process the last n JPG files
    input_paths = [os.path.join(folder_path, file) for file in jpg_files]
    output_paths = [os.path.join(output_folder, os.path.basename(file)) for file in jpg_files]
    batch_revise_images_for_llm(input_paths, quality, output_paths, max_workers)

    return output_paths

__all__ = ["revise_image_for_llm", "batch_revise_images_for_llm", "process_last_n_images"]
