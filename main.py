import argparse
from process_files_in_directory import process_files_in_directory
import directories

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description="Process some integers.")

    # Add the arguments
    parser.add_argument('input_directory', type=str, help='The input directory', nargs='?', default='.')
    parser.add_argument('output_directory', type=str, help='The output directory', nargs='?', default='.')

    # Parse the arguments
    args = parser.parse_args()

    output_directory = args.output_directory
    input_directory = args.input_directory

    directories.process_directories(output_directory)
    output_success_directory, output_error_directory = directories.get_directories(output_directory)
    process_files_in_directory(input_directory, output_success_directory, output_error_directory)
    # process_files_in_directory('./photos1')