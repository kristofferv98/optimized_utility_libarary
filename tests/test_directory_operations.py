import os
import pytest

from utility_functions.common.directory_operations import setup_directories, list_files, ensure_dir


def test_ensure_dir(tmp_path):
    dir_path = tmp_path / "test_dir"
    ensure_dir(str(dir_path))
    assert dir_path.exists()

def test_list_files(tmp_path):
    dir_path = tmp_path / "test_dir"
    file1 = dir_path / "file1.txt"
    file2 = dir_path / "file2.txt"
    dir_path.mkdir()
    file1.touch()
    file2.touch()
    files = list_files(str(dir_path))
    assert len(files) == 2
    assert "file1.txt" in files
    assert "file2.txt" in files

def test_list_files_with_pattern(tmp_path):
    dir_path = tmp_path / "test_dir"
    file1 = dir_path / "file1.txt"
    file2 = dir_path / "file2.log"
    dir_path.mkdir()
    file1.touch()
    file2.touch()
    files = list_files(str(dir_path), "*.txt")
    assert len(files) == 1
    assert "file1.txt" in files

def test_list_files_recursive(tmp_path):
    dir_path = tmp_path / "test_dir"
    sub_dir = dir_path / "sub_dir"
    file1 = dir_path / "file1.txt"
    file2 = sub_dir / "file2.txt"
    sub_dir.mkdir(parents=True)
    file1.touch()
    file2.touch()
    files = list_files(str(dir_path), "*.txt", True)
    assert len(files) == 2
    assert "file1.txt" in files
    assert "sub_dir/file2.txt" in files

def test_setup_directories(tmp_path):
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    config = {"path1": str(dir1), "path2": str(dir2)}
    setup_directories(config)
    assert dir1.exists()
    assert dir2.exists()