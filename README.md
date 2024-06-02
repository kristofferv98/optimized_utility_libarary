# Optimized Utility Library

## Overview
The Optimized Utility Library is a Python package that provides a collection of highly efficient and easy-to-use utility functions for common tasks such as directory operations, file handling, image processing, and JSON manipulation. This library is designed to simplify and speed up the development process by offering optimized solutions for frequently encountered tasks.

## Key Features
- **Directory Operations**: Easily manage directories, including creating directories, listing files, setting up multiple directories, checking for changes, and retrieving the latest files.
- **File Operations**: Perform common file operations like reading, writing, appending to CSV files, deleting files, clearing file contents, copying files, moving files, and retrieving file properties.
- **Image Processing**: Display images, convert images to base64 and vice versa, resize images, and perform optimized image resizing for use with OpenAI's GPT-4 API.
- **JSON Handling**: Efficiently load and save JSON data, get values with default fallbacks, and update JSON keys.
- **Performance Optimizations**: The library employs various optimization techniques such as caching, multithreading, lazy evaluation, and efficient third-party libraries to enhance performance and reduce execution time.
- **Logging Support**: Built-in logging functionality allows for easy debugging and monitoring of library operations.

## Installation
You can install the Optimized Utility Library using pip:

```bash
pip install optimized-utility-library
```

## Usage Examples

### Directory Operations

#### Ensure a Directory Exists
```python
from utility_lib.common.directory_operations import ensure_dir

directory_path = "path/to/directory"
ensure_dir(directory_path)
```

#### List Files in a Directory
```python
from utility_lib.common.directory_operations import list_files

directory_path = "path/to/directory"
files = list_files(directory_path, pattern="*.txt", recursive=True)
print(files)
```

#### Setup Multiple Directories
```python
from utility_lib.common.directory_operations import setup_directories

config = {
    "dir1": "path/to/dir1",
    "dir2": "path/to/dir2"
}
setup_directories(config)
```

#### Check if a Directory Has Changed
```python
from utility_lib.common.directory_operations import has_directory_changed

directory_path = "path/to/directory"
changed = has_directory_changed(directory_path)
print(changed)
```

#### Get Latest Files from a Directory
```python
from utility_lib.common.directory_operations import get_latest_files

directory_path = "path/to/directory"
latest_files = get_latest_files(directory_path, num_files=5, file_ext=".txt")
print(latest_files)
```

### File Operations

#### Read and Write Files
```python
from utility_lib.common.file_operations import read_file, write_file

file_path = "path/to/file.txt"
content = "Hello, World!"

# Write content to a file
write_file(file_path, content)

# Read content from a file
read_content = read_file(file_path)
print(read_content)
```

#### Append to a CSV File
```python
from utility_lib.common.file_operations import append_to_csv

row = ["name", "age", "city"]
csv_file_path = "path/to/file.csv"
append_to_csv(row, csv_file_path)
```

#### Delete a File
```python
from utility_lib.common.file_operations import delete_file

file_path = "path/to/file.txt"
delete_file(file_path)
```

### Image Processing

#### Display an Image
```python
from utility_lib.common.image_operations import display_img

image_path = "path/to/image.jpg"
display_img(image_path)
```

#### Convert Image to Base64
```python
from utility_lib.common.image_operations import image_to_base64

image_path = "path/to/image.jpg"
base64_string = image_to_base64(image_path)
print(base64_string)
```

#### Resize an Image
```python
from utility_lib.common.image_operations import resize_image

image_path = "path/to/image.jpg"
output_path = "path/to/resized_image.jpg"
size = (800, 600)
resize_image(image_path, size, output_path)
```

#### Revise Image for OpenAI's GPT-4 API
```python
from utility_lib.llm.llm_image_operation import revise_image_for_llm

image_path = "path/to/image.jpg"
mode = "low"  # or "high"
revise_image_for_llm(image_path, mode)
```

#### Batch Revise Images for OpenAI's GPT-4 API
```python
from utility_lib.llm.llm_image_operation import batch_revise_images_for_llm

image_paths = ["path/to/image1.jpg", "path/to/image2.jpg"]
mode = "low"
batch_revise_images_for_llm(image_paths, mode)
```

#### Process Last N Images for OpenAI's GPT-4 API
```python
from utility_lib.llm.llm_image_operation import process_last_n_images

folder_path = "path/to/folder"
output_folder = "path/to/output_folder"
num_images = 10
quality = "high"
processed_images = process_last_n_images(folder_path, num_images, output_folder, quality)
print(processed_images)
```

### JSON Handling

#### Load and Save JSON Data
```python
from utility_lib.common.json_operations import load_json, save_json

json_path = "path/to/file.json"
data = {"key": "value"}

# Save JSON data to a file
save_json(json_path, data)

# Load JSON data from a file
loaded_data = load_json(json_path)
print(loaded_data)
```

#### Get JSON Key with Default
```python
from utility_lib.common.json_operations import get_json_key

json_data = {"key1": "value1"}
value = get_json_key(json_data, "key2", "default_value")
print(value)
```

#### Update JSON Key
```python
from utility_lib.common.json_operations import update_json_key

json_data = {"key1": "value1"}
update_json_key(json_data, "key2", "value2")
print(json_data)
```

## Performance Optimizations
The Optimized Utility Library incorporates several techniques to enhance performance:

- **Caching**: The library utilizes caching mechanisms to store and reuse previously processed data, minimizing redundant operations and improving response times.
- **Multithreading**: Resource-intensive tasks, such as file processing and image resizing, are parallelized using multithreading to leverage available system resources and speed up execution.
- **Efficient Libraries**: The library leverages optimized third-party libraries like `ujson` for faster JSON serialization and deserialization, and `PIL` (Pillow) for efficient image processing.
- **Lazy Evaluation**: Certain operations, such as directory scanning and file listing, are performed lazily, meaning they are only executed when the results are actually needed, avoiding unnecessary processing and improving overall performance.

## Logging
The Optimized Utility Library includes built-in logging functionality to help with debugging and monitoring. By default, the logging level is set to `WARNING` to prevent excessive output. However, you can easily configure the logging level to suit your needs.

To enable logging, you can configure the root logger or the specific logger for the library:

```python
import logging

# Configure the root logger
logging.basicConfig(level=logging.DEBUG)

# Or configure the specific logger for the library
logging.getLogger('utility_lib').setLevel(logging.INFO)
```

Adjust the logging level as needed:
- `DEBUG`: Detailed information for debugging purposes.
- `INFO`: Confirmation that things are working as expected.
- `WARNING`: Indication of potential issues or unexpected events.
- `ERROR`: Serious issues that caused a failure in a specific operation.
- `CRITICAL`: Very serious errors that may lead to application failure.

## Contributing
Contributions to the Optimized Utility Library are welcome! If you find any bugs, have feature requests, or want to contribute improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/kristofferv98/optimized_utility_libarary.git).

When contributing, please adhere to the following guidelines:
- Follow the existing code style and conventions used in the library.
- Provide clear and concise documentation for any new functions or modifications.
- Write unit tests to ensure the reliability and stability of the library.
- Optimize for performance and efficiency whenever possible.

## License
The Optimized Utility Library is open-source and released under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute the library in accordance with the terms of the license.

## Acknowledgements
The Optimized Utility Library was inspired by the need for a streamlined and efficient set of utility functions in Python projects. I would like to thank the open-source community for their valuable contributions and the developers of the third-party libraries used in this project.

## Contact
If you have any questions, suggestions, or feedback regarding the Optimized Utility Library, please feel free to reach out.

Happy coding with the Optimized Utility Library!
