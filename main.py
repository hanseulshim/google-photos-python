import os
import argparse
from process_files_in_directory import process_files_in_directory
import directories

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description="Process some integers.")

    # Add the arguments
    parser.add_argument('input_directory', type=str, help='The input directory', nargs='?', default='.')
    parser.add_argument('output_directory', type=str, help='The output directory', nargs='?', default='.')
    parser.add_argument('final_directory', type=str, help='The final destination directory', nargs='?', default='.')

    # Parse the arguments
    args = parser.parse_args()

    input_directory = os.path.expanduser(args.input_directory)
    output_directory = os.path.expanduser(args.output_directory)
    final_directory = os.path.expanduser(args.final_directory)

    directories.process_directories(output_directory)
    output_success_directory, output_error_directory = directories.get_directories(output_directory)
    process_files_in_directory(input_directory, output_success_directory, output_error_directory, final_directory)
    # process_files_in_directory('./photos1')
    
    #TODO:
    # - After processing the files, move output directory to final directory if there are no errors
        # - Error directory needs to be empty
        # - Files count needs to match up
    # - If there are mismatch files, then throw an error