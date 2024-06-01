import pytest
from PIL import Image
from utility_functions.common.image_operations import resize_image

def create_test_image(file_path, size=(100, 100), color=(255, 0, 0)):
    """
    Utility function to create a simple image for testing.
    """
    image = Image.new('RGB', size, color)
    image.save(file_path)

def test_resize_image(tmp_path):
    file_path = tmp_path / "test_image.png"
    output_path = tmp_path / "resized_image.png"
    create_test_image(file_path, size=(1200, 600), color="blue")
    resize_image(str(file_path), (512, 512), str(output_path))
    resized_img = Image.open(output_path)
    assert resized_img.size == (512, 512)

def test_resize_image_no_output_path(tmp_path):
    file_path = tmp_path / "test_image.png"
    create_test_image(file_path, size=(1200, 600), color="blue")
    resize_image(str(file_path), (512, 512))
    resized_img = Image.open(file_path)
    assert resized_img.size == (512, 512)