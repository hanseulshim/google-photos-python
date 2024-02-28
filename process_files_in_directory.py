import os
import glob
import shutil
import constants
from process_file import process_file
from get_possible_json_filenames import get_possible_json_filenames
from check_for_duplicates import check_for_duplicates

# from rename_processed_files import rename_processed_files


def process_files_in_directory(input_directory, output_directory, error_directory):
    """
        Lists all files of supported types in directory path
        :param input_directory: path of the directory
        :return:
    """

    total_files = 0

    for mediaType in constants.SUPPORTED_MEDIA_FILE_TYPES:
        # destructure mediaType
        extension = mediaType['extension']
        mapToExtension = mediaType['mapToExtension']
        # grab all files with the extension (case insensitive)
        files = glob.glob(os.path.join(input_directory, '*.' + extension), recursive=True)
        files.extend(glob.glob(os.path.join(input_directory, '*.' + extension.upper()),recursive=True))
        
        files_length = len(files)
        print(f"Files with .{extension} extension: ", files_length)
        total_files += files_length
        for file in files:
            # for mp4 files, check if there are any corresponding image files. if there are then it means that we need to process the metadata with the image file instead of the mp4 file
            has_duplicates = check_for_duplicates(file) if extension == 'mp4' else False
            # if there are duplicates, then just copy the mp4 file but don't look for json because it may not exist
            if has_duplicates:
                copy_and_remap_extension(file, output_directory, mapToExtension)
                continue
            # check for corresponding json file
            possible_json_files = get_possible_json_filenames(file)
            for json_file in possible_json_files:
                if os.path.exists(json_file):
                    # copy file to output directory
                    copied_file = copy_and_remap_extension(file, output_directory, mapToExtension)
                    
                    if not has_duplicates:
                        process_file(json_file, copied_file)
                    break
            else:
                copy_and_remap_extension(file, error_directory, mapToExtension)
                print('No corresponding JSON file found: ', file, possible_json_files)
    print('Total files: ', total_files)

def copy_and_remap_extension(file, directory, new_extension):
    """
    Copy a file to a specified directory and rename it using a provided extension.
    :param file: The path of the file to copy
    :param directory: The directory to copy the file to
    :param new_extension: The new extension for the file
    :return: The path of the copied file
    """
    # Create the new filename using new_extension
    new_filename = f"{os.path.splitext(os.path.basename(file))[0]}.{new_extension}"

    # Create the full path for the new file in the directory
    new_filepath = os.path.join(directory, new_filename)

    # Copy the file to the directory with the new filename
    copied_file = shutil.copy2(file, new_filepath)

    return copied_file