import os

import pytest
from PIL import Image

from utility_functions.llm.llm_image_operation import revise_image_for_llm, batch_revise_images_for_llm, \
    process_last_n_images


def create_test_image(file_path, size=(100, 100), color=(255, 0, 0)):
    """
    Utility function to create a simple image for testing.
    """
    image = Image.new('RGB', size, color)
    image.save(file_path)


def test_revise_image_for_llm_low_mode(tmp_path):
    # Create a test image
    file_path = tmp_path / "test_image.png"
    create_test_image(file_path, size=(1200, 800), color=(0, 0, 255))

    # Output path for revised image
    output_path = tmp_path / "revised_image_low.png"

    # Run the function with 'low' mode
    revise_image_for_llm(str(file_path), 'low', str(output_path))

    # Check if the image was resized correctly
    revised_img = Image.open(output_path)
    assert revised_img.size == (512, 512)


def test_revise_image_for_llm_high_mode(tmp_path):
    # Create a test image
    file_path = tmp_path / "test_image.png"
    create_test_image(file_path, size=(1200, 800), color=(0, 0, 255))

    # Output path for revised image
    output_path = tmp_path / "revised_image_high.png"

    # Run the function with 'high' mode
    revise_image_for_llm(str(file_path), 'high', str(output_path))

    # Check if the image was resized correctly
    revised_img = Image.open(output_path)
    assert revised_img.size == (1200, 800)


def test_revise_image_for_llm_invalid_mode(tmp_path):
    # Create a test image
    file_path = tmp_path / "test_image.png"
    create_test_image(file_path, size=(1200, 800), color=(0, 0, 255))

    # Output path for revised image
    output_path = tmp_path / "revised_image_invalid.png"

    # Run the function with an invalid mode and check for ValueError
    with pytest.raises(ValueError, match="Mode should be either 'low' or 'high'."):
        revise_image_for_llm(str(file_path), 'invalid', str(output_path))


def test_revise_image_for_llm_file_not_found(tmp_path):
    # Non-existent file path
    file_path = tmp_path / "non_existent_image.png"

    # Output path for revised image
    output_path = tmp_path / "revised_image_not_found.png"

    # Run the function with a non-existent file path and check for FileNotFoundError
    with pytest.raises(FileNotFoundError):
        revise_image_for_llm(str(file_path), 'low', str(output_path))


def test_batch_revise_images_for_llm_low_mode(tmp_path):
    # Create multiple test images
    image_paths = []
    for i in range(3):
        file_path = tmp_path / f"test_image_{i}.png"
        create_test_image(file_path, size=(1200, 800), color=(0, 0, 255))
        image_paths.append(str(file_path))

    # Output paths for revised images
    output_paths = [str(tmp_path / f"revised_image_{i}_low.png") for i in range(3)]

    # Run the batch function with 'low' mode
    batch_revise_images_for_llm(image_paths, 'low', output_paths)

    # Check if all images were resized correctly
    for output_path in output_paths:
        revised_img = Image.open(output_path)
        assert revised_img.size == (512, 512)


def test_batch_revise_images_for_llm_high_mode(tmp_path):
    # Create multiple test images
    image_paths = []
    for i in range(3):
        file_path = tmp_path / f"test_image_{i}.png"
        create_test_image(file_path, size=(1200, 800), color=(0, 0, 255))
        image_paths.append(str(file_path))

    # Output paths for revised images
    output_paths = [str(tmp_path / f"revised_image_{i}_high.png") for i in range(3)]

    # Run the batch function with 'high' mode
    batch_revise_images_for_llm(image_paths, 'high', output_paths)

    # Check if all images were resized correctly
    for output_path in output_paths:
        revised_img = Image.open(output_path)
        assert revised_img.size == (1200, 800)


def test_batch_revise_images_for_llm_invalid_mode(tmp_path):
    # Create multiple test images
    image_paths = []
    for i in range(3):
        file_path = tmp_path / f"test_image_{i}.png"
        create_test_image(file_path, size=(1200, 800), color=(0, 0, 255))
        image_paths.append(str(file_path))

    # Output paths for revised images
    output_paths = [str(tmp_path / f"revised_image_{i}_invalid.png") for i in range(3)]

    # Run the batch function with an invalid mode and check for ValueError
    with pytest.raises(ValueError, match="Mode should be either 'low' or 'high'."):
        batch_revise_images_for_llm(image_paths, 'invalid', output_paths)


def test_batch_revise_images_for_llm_path_mismatch(tmp_path):
    # Create multiple test images
    image_paths = []
    for i in range(3):
        file_path = tmp_path / f"test_image_{i}.png"
        create_test_image(file_path, size=(1200, 800), color=(0, 0, 255))
        image_paths.append(str(file_path))

    # Output paths for revised images (mismatched length)
    output_paths = [str(tmp_path / f"revised_image_{i}_low.png") for i in range(2)]

    # Run the batch function with mismatched path lengths and check for ValueError
    with pytest.raises(ValueError, match="Number of image paths and output paths must match."):
        batch_revise_images_for_llm(image_paths, 'low', output_paths)


def test_process_last_n_images(tmp_path):
    # Create a temporary folder for testing
    folder_path = tmp_path / "test_folder"
    folder_path.mkdir()

    # Create test images in the folder
    for i in range(5):
        file_path = folder_path / f"image_{i}.jpg"
        create_test_image(file_path, size=(1200, 800), color=(0, 0, 255))

    # Create an output folder
    output_folder = tmp_path / "output_folder"

    # Process the last 3 images with 'low' quality
    num_images = 3
    quality = 'low'
    output_paths = process_last_n_images(str(folder_path), num_images, str(output_folder), quality)

    # Check if the correct number of images were processed
    assert len(output_paths) == num_images

    # Check if the processed images exist in the output folder
    for output_path in output_paths:
        assert os.path.exists(output_path)

    # Check if the processed images have the correct size
    for output_path in output_paths:
        revised_img = Image.open(output_path)
        assert revised_img.size == (512, 512)


def test_process_last_n_images_high_quality(tmp_path):
    # Create a temporary folder for testing
    folder_path = tmp_path / "test_folder"
    folder_path.mkdir()

    # Create test images in the folder
    for i in range(5):
        file_path = folder_path / f"image_{i}.jpg"
        create_test_image(file_path, size=(1200, 800), color=(0, 0, 255))

    # Create an output folder
    output_folder = tmp_path / "output_folder"

    # Process the last 3 images with 'high' quality
    num_images = 3
    quality = 'high'
    output_paths = process_last_n_images(str(folder_path), num_images, str(output_folder), quality)

    # Check if the correct number of images were processed
    assert len(output_paths) == num_images

    # Check if the processed images exist in the output folder
    for output_path in output_paths:
        assert os.path.exists(output_path)

    # Check if the processed images have the correct size
    for output_path in output_paths:
        revised_img = Image.open(output_path)
        assert revised_img.size == (1200, 800)


def test_process_last_n_images_invalid_quality(tmp_path):
    # Create a temporary folder for testing
    folder_path = tmp_path / "test_folder"
    folder_path.mkdir()

    # Create test images in the folder
    for i in range(5):
        file_path = folder_path / f"image_{i}.jpg"
        create_test_image(file_path, size=(1200, 800), color=(0, 0, 255))

    # Create an output folder
    output_folder = tmp_path / "output_folder"

    # Process the last 3 images with an invalid quality
    num_images = 3
    quality = 'invalid'

    # Check if ValueError is raised for invalid quality
    with pytest.raises(ValueError, match="Mode should be either 'low' or 'high'."):
        process_last_n_images(str(folder_path), num_images, str(output_folder), quality)


def test_process_last_n_images_folder_not_found(tmp_path):
    # Non-existent folder path
    folder_path = tmp_path / "non_existent_folder"

    # Create an output folder
    output_folder = tmp_path / "output_folder"

    # Process the last 3 images from a non-existent folder
    num_images = 3
    quality = 'low'

    # Check if FileNotFoundError is raised for non-existent folder
    with pytest.raises(FileNotFoundError):
        process_last_n_images(str(folder_path), num_images, str(output_folder), quality)


def test_process_last_n_images_no_jpg_files(tmp_path):
    # Create a temporary folder for testing
    folder_path = tmp_path / "test_folder"
    folder_path.mkdir()

    # Create non-JPG files in the folder
    for i in range(5):
        file_path = folder_path / f"file_{i}.txt"
        with open(file_path, 'w') as file:
            file.write("Test file")

    # Create an output folder
    output_folder = tmp_path / "output_folder"

    # Process the last 3 images from a folder with no JPG files
    num_images = 3
    quality = 'low'
    output_paths = process_last_n_images(str(folder_path), num_images, str(output_folder), quality)

    # Check if an empty list is returned when no JPG files are found
    assert len(output_paths) == 0
