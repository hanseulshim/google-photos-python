import os
import re

def get_possible_json_filenames(filename):
    """
    Generate possible JSON filenames based on the input filename.
    :param filename: The input filename
    :return: A list of possible JSON filenames
    """
    possible_json_filenames = []

    directory, filename_extension = os.path.split(filename)
    filename_only, file_extension = os.path.splitext(filename)

    # Check if the base filename ends with a number in parentheses
    match = re.search(r"\(\d\)$", filename_only)
    if match:
        # if it does the corresponding JSON is something like IMG.JPG(1).json
        possible_json_filename = filename_only[:match.start()] + file_extension + filename_only[match.start():] + '.json'
        # append the possible JSON filename to the list
        possible_json_filenames.append(possible_json_filename)
        
    # Check if the base filename ends with "-edited"
    if filename_only.endswith("-edited"):
        possible_json_filename = filename_only[:-7] + file_extension + '.json'
        possible_json_filenames.append(possible_json_filename)
    
    # # if the filename is longer than 46 characters, we need to truncate it
    if len(filename_extension) > 46:
        possible_json_filename = os.path.join(directory, filename_extension[:46] + '.json')
        possible_json_filenames.append(possible_json_filename)
    
    # always include the base filename with the .json extension as a possibility
    possible_json_filename = filename + '.json'
    possible_json_filenames.append(possible_json_filename)
    
    return possible_json_filenames