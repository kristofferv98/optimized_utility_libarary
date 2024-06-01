import os
import time
import shutil
import tempfile
import pytest

from utility_lib.common.directory_operations import has_directory_changed, get_latest_files


@pytest.fixture
def temp_directory():
    directory = tempfile.mkdtemp()
    yield directory
    shutil.rmtree(directory)


def create_file(directory, filename):
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as file:
        file.write("Test file")
    return file_path


def capture_directory_state(directory):
    state = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            mtime = os.path.getmtime(file_path)
            state[file_path] = mtime
    return state


def test_has_directory_changed(temp_directory):
    # Test when state file doesn't exist
    assert has_directory_changed(temp_directory)

    # Capture the initial state and update state file
    current_state = capture_directory_state(temp_directory)

    # Test when no changes in directory
    assert not has_directory_changed(temp_directory)

    # Test when a new file is added
    create_file(temp_directory, "file1.txt")
    assert has_directory_changed(temp_directory)

    # Capture the state again and update state file
    current_state = capture_directory_state(temp_directory)

    # Test when no further changes in directory
    assert not has_directory_changed(temp_directory)

    # Test when an existing file is modified
    time.sleep(1)  # Ensure modification time is different
    create_file(temp_directory, "file1.txt")
    assert has_directory_changed(temp_directory)


def test_get_latest_files(temp_directory):
    # Test when directory is empty
    assert get_latest_files(temp_directory) == []

    # Create test files
    file1 = create_file(temp_directory, "file1.txt")
    time.sleep(1)  # Ensure modification times are different
    file2 = create_file(temp_directory, "file2.txt")
    time.sleep(1)
    file3 = create_file(temp_directory, "file3.txt")
    time.sleep(1)
    file4 = create_file(temp_directory, "file4.jpg")

    # Test getting all files
    latest_files = get_latest_files(temp_directory)
    assert latest_files == [file4, file3, file2, file1]

    # Test getting limited number of files
    latest_files = get_latest_files(temp_directory, num_files=2)
    assert latest_files == [file4, file3]

    # Test getting files with specific extension
    latest_files = get_latest_files(temp_directory, file_ext=".txt")
    assert latest_files == [file3, file2, file1]

    # Test getting limited number of files with specific extension
    latest_files = get_latest_files(temp_directory, num_files=2, file_ext=".txt")
    assert latest_files == [file3, file2]
