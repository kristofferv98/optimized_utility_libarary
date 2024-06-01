import os
import shutil
import logging
import csv
from concurrent.futures import ThreadPoolExecutor
from time import ctime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global cache dictionary
file_cache = {}


def read_file(file_path):
    """
    Read and return the content of a file.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file, or None if an error occurs.
    """
    global file_cache

    # Check if the file content is in the cache
    if file_path in file_cache:
        logging.info(f"Using cached content for {file_path}")
        return file_cache[file_path]

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            file_cache[file_path] = content
            return content
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {str(e)}")
        return None


def write_file(file_path, content, mode='w', print_path=False):
    """
    Write content to a file. Mode 'w' for overwrite, 'a' for append.

    Args:
        file_path (str): The path to the file to write to.
        content (str): The content to write to the file.
        mode (str): The mode in which to open the file ('w' for write, 'a' for append). Defaults to 'w'.
        print_path (bool): Whether to print a success message. Defaults to False.
    """
    global file_cache
    buffer_size = 1024

    try:
        with open(file_path, mode, encoding='utf-8', buffering=buffer_size) as file:
            file.write(content)
            if print_path:
                logging.info(f"Content written to {file_path}.")
        # Invalidate the cache
        if mode == 'w':
            file_cache[file_path] = content
        elif mode == 'a':
            if file_path in file_cache:
                file_cache[file_path] += content
            else:
                file_cache[file_path] = content
    except Exception as e:
        logging.error(f"Failed to write to file {file_path}: {str(e)}")


def append_to_csv(row_list, filename, delimiter=',', quoting=csv.QUOTE_MINIMAL):
    """
    Append a row to a CSV file with customizable delimiter and quoting options.

    Args:
        row_list (list): The row data to append to the CSV file.
        filename (str): The path to the CSV file.
        delimiter (str): The delimiter to use in the CSV file. Defaults to ','.
        quoting (int): The quoting option for the CSV writer. Defaults to csv.QUOTE_MINIMAL.

    Raises:
        Exception: If there is an error appending to the CSV file.
    """
    global file_cache

    try:
        with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quoting=quoting)
            writer.writerow(row_list)
            logging.info(f"Row appended to {filename}.")
        # Invalidate the cache for the CSV file
        if filename in file_cache:
            del file_cache[filename]
    except Exception as e:
        logging.error(f"Failed to append to CSV file {filename}: {str(e)}")


def delete_file(file_path):
    """
    Delete a file.

    Args:
        file_path (str): The path to the file to be deleted.

    Raises:
        Exception: If there is an error deleting the file.
    """
    global file_cache

    try:
        os.remove(file_path)
        logging.info(f"File {file_path} deleted successfully.")
        # Invalidate the cache
        if file_path in file_cache:
            del file_cache[file_path]
    except Exception as e:
        logging.error(f"Failed to delete file {file_path}: {str(e)}")


def clear_file(file_path):
    """
    Clear the content of a text file.

    Args:
        file_path (str): The path to the file to be cleared.

    Returns:
        bool: True if the file was cleared successfully, False otherwise.

    Raises:
        Exception: If there is an error clearing the file.
    """
    global file_cache

    try:
        if os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write('')
            logging.info(f"File {file_path} cleared.")
            # Invalidate the cache
            file_cache[file_path] = ''
            return True
        else:
            logging.error(f"The file {file_path} does not exist.")
            return False
    except Exception as e:
        logging.error(f"Failed to clear file {file_path}: {str(e)}")
        return False


def copy_file(source, destination):
    """
    Copy a file from source to destination.

    Args:
        source (str): The path to the source file.
        destination (str): The path to the destination file.

    Raises:
        Exception: If there is an error copying the file.
    """
    global file_cache

    try:
        shutil.copy(source, destination)
        logging.info(f"File copied from {source} to {destination}.")
        # Invalidate the cache
        if destination in file_cache:
            del file_cache[destination]
    except Exception as e:
        logging.error(f"Failed to copy file from {source} to {destination}: {str(e)}")


def move_file(source, destination):
    """
    Move a file from source to destination.

    Args:
        source (str): The path to the source file.
        destination (str): The path to the destination file.

    Raises:
        Exception: If there is an error moving the file.
    """
    global file_cache

    try:
        shutil.move(source, destination)
        logging.info(f"File moved from {source} to {destination}.")
        # Invalidate the cache
        if source in file_cache:
            del file_cache[source]
        if destination in file_cache:
            del file_cache[destination]
    except Exception as e:
        logging.error(f"Failed to move file from {source} to {destination}: {str(e)}")


def file_properties(file_path):
    """
    Return file size, creation, and modification times.

    Args:
        file_path (str): The path to the file to retrieve properties for.

    Returns:
        dict: A dictionary with file size, creation time, and modification time, or None if an error occurs.

    Raises:
        Exception: If there is an error retrieving the file properties.
    """
    global file_cache

    # Check if the file properties are in the cache
    if file_path in file_cache:
        logging.info(f"Using cached properties for {file_path}")
        return file_cache[file_path]

    try:
        file_stats = os.stat(file_path)
        properties = {
            'size': file_stats.st_size,
            'creation_time': ctime(file_stats.st_ctime),
            'modification_time': ctime(file_stats.st_mtime)
        }
        # Update the cache
        file_cache[file_path] = properties
        return properties
    except Exception as e:
        logging.error(f"Error getting properties for {file_path}: {str(e)}")
        return None


def get_file_size(file_path):
    """
    Return the size of a file in bytes.

    Args:
        file_path (str): The path to the file to retrieve the size for.

    Returns:
        int: The size of the file in bytes, or -1 if an error occurs.

    Raises:
        Exception: If there is an error retrieving the file size.
    """
    global file_cache

    # Check if the file size is in the cache
    if file_path in file_cache and 'size' in file_cache[file_path]:
        logging.info(f"Using cached size for {file_path}")
        return file_cache[file_path]['size']

    try:
        size = os.path.getsize(file_path)
        # Update the cache
        if file_path in file_cache:
            file_cache[file_path]['size'] = size
        else:
            file_cache[file_path] = {'size': size}
        return size
    except Exception as e:
        logging.error(f"Failed to get size of file {file_path}: {str(e)}")
        return -1


def parallel_process_files(file_list, process_func, max_workers=4):
    """
    Process a list of files in parallel by submitting the processing function for each file to a ThreadPoolExecutor.

    Args:
        file_list (list): The list of files to process.
        process_func (callable): The function to process each file. Must take the file path as its only parameter.
        max_workers (int): The maximum number of worker threads in the thread pool. Defaults to 4.

    Raises:
        Exception: If there is an error during the processing of a file.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_func, file) for file in file_list]
        for future in futures:
            future.result()


__all__ = ['read_file', 'write_file', 'append_to_csv', 'delete_file', 'clear_file', 'copy_file', 'move_file',
           'file_properties', 'get_file_size', 'parallel_process_files']
