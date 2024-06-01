#!/bin/bash

# Run the tests
echo "Running the tests..."
pytest tests/test_directory_operations.py
pytest tests/test_file_operations.py
pytest tests/test_image_operations.py
pytest tests/test_json_operations.py
pytest tests/test_llm_image_operations.py

# Final check
echo "All commands executed. Check above for any errors or issues."

