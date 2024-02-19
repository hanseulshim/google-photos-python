import os
import glob

def check_for_duplicates(filename):
  directory = os.path.dirname(filename)
  # Get the base name of the file (without the path and extension)
  base_name = os.path.splitext(os.path.basename(filename))[0]

  # Find all files in the directory with the same base name but different extension
  matching_files = glob.glob(os.path.join(directory, base_name + '.*'))

  # Remove the original file from the list of matching files and remove any JSON files
  matching_files = [file for file in matching_files if os.path.basename(file) != os.path.basename(filename) and not file.endswith('.json')]


  # If there are any matching files, return True. Otherwise, return False.
  return len(matching_files) > 0