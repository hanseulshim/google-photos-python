import os
import constants


def clear_directory(directory_path):
    """
    Deletes all files in directory path
    :param directory_path: path of the directory
    :return:
    """
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"All files deleted successfully in ./{directory_path}")
    except OSError as e:
        print("Error occurred while deleting files: ", e)


def process_directories(directory=None):
    """
    1. Creates the output and error directories if they don't exist
    2. Wipes the directories if they're not empty
    :param directory: Optional base directory to combine with output and error directories
    :return:
    """
    directories = [constants.OUTPUT_DIRECTORY, constants.ERROR_DIRECTORY]
    if directory:
        directories = [os.path.join(directory, d) for d in directories]
    try:
        for directory in directories:
            if os.path.isdir(directory):
                clear_directory(directory)
            else:
                os.mkdir(directory)
    except OSError as e:
        print("Error occurred in process_directories: ", e)

def get_directories(root_path):
    """
    Creates output and error directories within the specified root path if they don't exist.
    
    Args:
        root_path (str): The root path where the directories will be created.
        
    Returns:
        tuple: A tuple containing the paths of the output and error directories.
    """
    output_directory = os.path.join(root_path, constants.OUTPUT_DIRECTORY)
    error_directory = os.path.join(root_path, constants.ERROR_DIRECTORY)
    
    return output_directory, error_directory