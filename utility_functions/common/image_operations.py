import os
import logging
from PIL import Image, UnidentifiedImageError
from matplotlib import pyplot as plt
import base64
import cv2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global cache dictionary
file_cache = {}

def display_img(filepath):
    """
    Display an image from the given file path using matplotlib.

    Args:
        filepath (str): The path to the image file.

    Raises:
        FileNotFoundError: If the image file does not exist.
        UnidentifiedImageError: If the image file cannot be identified or opened.
        Exception: For any other errors that may occur.
    """
    global file_cache

    if filepath in file_cache:
        img = file_cache[filepath]
        logging.info(f"Using cached image for {filepath}")
    else:
        if os.path.exists(filepath):
            try:
                img = Image.open(filepath)
                file_cache[filepath] = img
            except UnidentifiedImageError:
                logging.error(f"Cannot identify image file at {filepath}")
                return
            except Exception as e:
                logging.error(f"Failed to display image at {filepath}: {str(e)}")
                return
        else:
            logging.error(f"Image not found at {filepath}")
            return

    dpi = plt.rcParams['figure.dpi']
    width, height = img.size
    fig_size = width / dpi, height / dpi

    plt.figure(figsize=fig_size)
    plt.imshow(img)
    plt.axis('off')  # Hide axes
    plt.show()

def clear_plot():
    """
    Clear the current matplotlib plot.
    """
    plt.clf()
    plt.close()

def image_to_base64(filepath):
    """
    Convert an image file to a Base64 encoded string without quality loss.

    Args:
        filepath (str): The path to the image file.

    Returns:
        str: The Base64 encoded string of the image, or None if an error occurs.

    Raises:
        FileNotFoundError: If the image file does not exist.
        Exception: For any other errors that may occur.
    """
    global file_cache

    if filepath in file_cache:
        base64_string = file_cache[filepath]
        logging.info(f"Using cached Base64 string for {filepath}")
        return base64_string

    try:
        with open(filepath, "rb") as image_file:
            base64_string = base64.b64encode(image_file.read()).decode('utf-8')
            file_cache[filepath] = base64_string
            return base64_string
    except FileNotFoundError:
        logging.error(f"Image file not found at {filepath}")
    except Exception as e:
        logging.error(f"Failed to convert image to Base64 at {filepath}: {str(e)}")
    return None

def base64_to_image(base64_string, output_filepath):
    """
    Decode a Base64 string back to an image file.

    Args:
        base64_string (str): The Base64 encoded string of the image.
        output_filepath (str): The path to save the decoded image file.

    Raises:
        Exception: If there is an error decoding the Base64 string.
    """
    global file_cache

    try:
        image_data = base64.b64decode(base64_string)
        with open(output_filepath, "wb") as image_file:
            image_file.write(image_data)
        logging.info(f"Image saved to {output_filepath}")
        file_cache[output_filepath] = base64_string
    except Exception as e:
        logging.error(f"Failed to decode Base64 to image: {str(e)}")

def resize_image(image_path, size, output_path=None):
    """
    Resize an image to the specified size.

    Args:
        image_path (str): The path to the image file.
        size (tuple): The desired size as (width, height).
        output_path (str, optional): The path to save the resized image. If None, the original image is overwritten.

    Raises:
        FileNotFoundError: If the image file does not exist.
        Exception: For any other errors that may occur.
    """
    global file_cache

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at {image_path}")

    try:
        img = cv2.imread(image_path)
        resized_img = cv2.resize(img, size, interpolation=cv2.INTER_LANCZOS4)
        if output_path:
            cv2.imwrite(output_path, resized_img)
            logging.info(f"Resized image saved to {output_path}")
            file_cache[output_path] = resized_img
        else:
            cv2.imwrite(image_path, resized_img)
            logging.info(f"Resized image saved to {image_path}")
            file_cache[image_path] = resized_img
    except Exception as e:
        logging.error(f"Failed to resize image at {image_path}: {str(e)}")

__all__ = ["display_img", "clear_plot", "image_to_base64", "base64_to_image", "resize_image"]
