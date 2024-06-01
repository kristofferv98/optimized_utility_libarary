import json
import math
import time

import pytest
import ujson

from utility_lib.common.json_operations import (
    get_json_key,
    load_json,
    save_json,
    update_json_key,
)

@pytest.fixture
def json_test_file(tmp_path):
    file_path = tmp_path / "test.json"
    content = {"key": "value"}
    save_json(str(file_path), content)
    return str(file_path)


def test_load_json(tmp_path):
    file_path = tmp_path / "test.json"
    content = {"key": "value"}
    file_path.write_text(json.dumps(content))
    loaded_content = load_json(str(file_path))
    assert loaded_content == content

def test_load_invalid_json(tmp_path):
    file_path = tmp_path / "test.json"
    file_path.write_text("{invalid json}")
    loaded_content = load_json(str(file_path))
    assert loaded_content is None

def test_save_json(tmp_path):
    file_path = tmp_path / "test.json"
    content = {"key": "value"}
    assert save_json(str(file_path), content)
    loaded_content = json.loads(file_path.read_text())
    assert loaded_content == content

def test_save_invalid_json(tmp_path):
    file_path = tmp_path / "test.json"
    content = {"key": float("nan")}
    save_json(str(file_path), content)
    loaded_content = ujson.load(file_path.open())
    assert math.isnan(loaded_content["key"])

def test_get_json_key():
    json_data = {"key1": "value1", "key2": "value2"}
    assert get_json_key(json_data, "key1") == "value1"
    assert get_json_key(json_data, "key3", "default") == "default"

def test_get_json_key_with_default():
    json_data = {"key1": "value1"}
    assert get_json_key(json_data, "key2", "default") == "default"

def test_update_json_key():
    json_data = {"key1":"value1", "key2": "value2"}
    assert update_json_key(json_data, "key1", "new_value")
    assert json_data["key1"] == "new_value"

def test_update_json_key_new_key():
    json_data = {"key1": "value1"}
    assert update_json_key(json_data, "key2", "value2")
    assert json_data["key2"] == "value2"

def test_update_json_key_invalid_key():
    json_data = {"key1": "value1"}
    result = update_json_key(json_data, "key2", "value2")
    assert result == True
    assert "key2" in json_data

    # Test with integer key
    result = update_json_key(json_data, 1, "int value")
    assert result == True
    assert 1 in json_data

    # Test with boolean key
    result = update_json_key(json_data, True, "bool value")
    assert result == True
    assert True in json_data

    # Test with invalid key type (e.g., list)
    result = update_json_key(json_data, ["list_key"], "value")
    assert result == False


def test_load_json_performance(json_test_file):
    iterations = 100000  # Increase iterations to reduce measurement noise

    # Measure time without caching
    start_time = time.time()
    for _ in range(iterations):
        load_json(json_test_file)
    no_cache_duration = time.time() - start_time

    # Clear cache to measure time with caching
    global json_cache
    json_cache = {}

    # Measure time with caching
    start_time = time.time()
    for _ in range(iterations):
        load_json(json_test_file)
    cache_duration = time.time() - start_time

    print(f"No cache duration: {no_cache_duration:.4f} seconds")
    print(f"Cache duration: {cache_duration:.4f} seconds")

    assert cache_duration < no_cache_duration