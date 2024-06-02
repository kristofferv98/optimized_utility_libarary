
# Optimized Utility Library

## Overview
This library provides optimized utility functions for directory operations, file operations, image processing, and JSON handling. It is designed to be highly efficient and easy to use, making common tasks simpler and faster.

## Installation
You can install the library using pip:

```bash
pip install optimized-utility-library
```

## Usage
Below are examples of how to use the various functionalities provided by the library.

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
state_file = "path/to/state.json"
changed = has_directory_changed(directory_path, state_file)
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

### Image Operations
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

### JSON Operations
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

#### Update JSON Key
```python
from utility_lib.common.json_operations import update_json_key

json_data = {"key1": "value1"}
update_json_key(json_data, "key2", "value2")
print(json_data)
```

#### Get JSON Key with Default
```python
from utility_lib.common.json_operations import get_json_key

json_data = {"key1": "value1"}
value = get_json_key(json_data, "key2", "default_value")
print(value)
```

### LLM Image Operations
#### Revise Image for LLM
```python
from utility_lib.common.llm_image_operations import revise_image_for_llm

image_path = "path/to/image.jpg"
mode = "low"  # or "high"
revise_image_for_llm(image_path, mode)
```

#### Batch Revise Images for LLM
```python
from utility_lib.common.llm_image_operations import batch_revise_images_for_llm

image_paths = ["path/to/image1.jpg", "path/to/image2.jpg"]
mode = "low"
batch_revise_images_for_llm(image_paths, mode)
```

#### Process Last N Images
```python
from utility_lib.common.llm_image_operations import process_last_n_images

folder_path = "path/to/folder"
output_folder = "path/to/output_folder"
num_images = 10
quality = "high"
processed_images = process_last_n_images(folder_path, num_images, output_folder, quality)
print(processed_images)
```


### Logging Configuration

By default, logging is set to use a WARNING to prevent logging from producing any output unless configured by the user.
Here’s an example of how to configure logging specific to the library.
```python
import logging

# Configure root logger or specific logger
logging.basicConfig(level=logging.DEBUG)

# or configure the specific logger for your module
logging.getLogger('utility_lib').setLevel(logging.INFO)

# Now when you use the library, you will see debug logs
from utility_lib.common.json_operations import load_json, save_json

# Use the functions as usual
json_path = "path/to/file.json"
data = {"key": "value"}

save_json(json_path, data)
loaded_data = load_json(json_path)
print(loaded_data)

```
