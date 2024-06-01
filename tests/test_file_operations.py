from pathlib import Path

from utility_functions.common.file_operations import (
    read_file, write_file, append_to_csv,
    delete_file, clear_file, copy_file,
    move_file, file_properties, get_file_size,
    parallel_process_files
)


def test_read_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    content = "Hello, World!"
    file_path.write_text(content)
    assert read_file(str(file_path)) == content


def test_write_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    content = "Hello, World!"
    write_file(str(file_path), content)
    assert file_path.read_text() == content


def test_append_to_csv(tmp_path):
    file_path = tmp_path / "test_file.csv"
    row = ["a", "b", "c"]
    append_to_csv(row, str(file_path))
    assert file_path.read_text().strip() == "a,b,c"


def test_append_multiple_to_csv(tmp_path):
    file_path = tmp_path / "test_file.csv"
    row1 = ["a", "b", "c"]
    row2 = ["d", "e", "f"]
    append_to_csv(row1, str(file_path))
    append_to_csv(row2, str(file_path))
    assert file_path.read_text().strip() == "a,b,c\nd,e,f"


def test_delete_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.touch()
    delete_file(str(file_path))
    assert not file_path.exists()


def test_clear_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("content")
    clear_file(str(file_path))
    assert file_path.read_text() == ""


def test_copy_file(tmp_path):
    src_path = tmp_path / "test_file.txt"
    dest_path = tmp_path / "copy_file.txt"
    src_path.write_text("content")
    copy_file(str(src_path), str(dest_path))
    assert dest_path.read_text() == "content"


def test_move_file(tmp_path):
    src_path = tmp_path / "test_file.txt"
    dest_path = tmp_path / "moved_file.txt"
    src_path.write_text("content")
    move_file(str(src_path), str(dest_path))
    assert dest_path.read_text() == "content"
    assert not src_path.exists()


def test_file_properties(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("content")
    properties = file_properties(str(file_path))
    assert properties is not None
    assert properties['size'] == len("content")


def test_get_file_size(tmp_path):
    file_path = tmp_path / "test_file.txt"
    content = "content"
    file_path.write_text(content)
    assert get_file_size(str(file_path)) == len(content)


def test_parallel_process_files(tmp_path):
    # Setup a sample processing function
    def test_process_func(file_path):
        content = read_file(file_path)
        write_file(file_path, content[::-1])

    # Create sample files
    file_list = []
    content = "Hello, World!"
    for i in range(4):
        file_path = tmp_path / f"file{i}.txt"
        file_path.write_text(content)
        file_list.append(str(file_path))

    # Process files in parallel
    parallel_process_files(file_list, test_process_func, max_workers=2)

    # Check if each file has been processed correctly
    for file_path in file_list:
        assert Path(file_path).read_text() == content[::-1]
