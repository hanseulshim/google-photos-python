from PIL import Image, UnidentifiedImageError
import os

def check_file_extension(filename):
    """
    Check the file extension of the given filename and compare it with the actual file type.

    Args:
        filename (str): The path to the file.

    Returns:
        str or None: The file type if it doesn't match the file extension, otherwise None.
    """
    try:
        with Image.open(filename) as img:
            file_type = img.format.lower()
    except UnidentifiedImageError:
        return None
    file_extension = os.path.splitext(filename)[1][1:]
    return None if file_type == file_extension else file_type
