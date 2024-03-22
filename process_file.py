import os
import datetime
import constants
from exiftool import ExifToolHelper, exceptions
from convert_image_type import covert_image_type
from check_file_extension import check_file_extension

def process_file(json_file, filename):
    print('Processing file: ', filename)
    file_extension = os.path.splitext(filename)[1]
    file_directory = os.path.dirname(filename)
    
    correct_file_extension = check_file_extension(filename)
    if correct_file_extension != None:
        # File type and file extension are not equal, convert the file to the correct format
        new_file_extension = '.' + correct_file_extension
        new_filename = os.path.splitext(filename)[0] + new_file_extension
        covert_image_type(filename, new_filename, correct_file_extension)
        filename = new_filename
        file_extension = new_file_extension
        
    
    if file_extension in ['.png']:
        file_extension = '.jpg'
        jpg_filename = os.path.splitext(filename)[0] + file_extension
        covert_image_type(filename, jpg_filename, 'JPEG')
        filename = jpg_filename
    
    new_filename = get_new_file_name(json_file, file_directory, file_extension)
    new_filename_full = os.path.join(file_directory, new_filename + file_extension)
    
    os.rename(filename, new_filename_full)
    write_metadata(json_file, new_filename_full)
        
    if file_extension not in ['.mp4']:
        mp4_filename = os.path.splitext(filename)[0] + '.mp4'
        if os.path.exists(mp4_filename):
            new_mp4_filename = os.path.join(file_directory, new_filename + '.mp4')
            os.rename(mp4_filename, new_mp4_filename)
            write_metadata(json_file, new_mp4_filename)
            
def get_new_file_name(json_file, file_directory, file_extension):
    """
    Generates a new file name based on the photo taken time from the metadata of a JSON file.

    Args:
        json_file (str): The path to the JSON file containing the metadata.
        file_directory (str): The directory of the file.

    Returns:
        str: The new file name.

    Raises:
        None
    """
    with ExifToolHelper() as e:    
        metadata = e.get_metadata(json_file)[0]
        
        # Process date
        photo_taken_time = metadata['JSON:PhotoTakenTimeTimestamp']
        dt = datetime.datetime.fromtimestamp(photo_taken_time)
        # Rename the file using the photo_taken_time
        new_file_name = dt.strftime(constants.FILE_FORMAT)
        new_file_path = os.path.join(file_directory, new_file_name + file_extension)

        # Check if a file with the new name already exists
        counter = 1
        while os.path.exists(new_file_path):
            new_file_name = dt.strftime(constants.FILE_FORMAT) + f'_{counter:03}'
            new_file_path = os.path.join(file_directory, new_file_name + file_extension)
            counter += 1

        return new_file_name
    
def write_metadata(json_file, filename):
    """
    Writes metadata to a file using the ExifTool library.
    
    Args:
        json_file (str): The path of the JSON file containing the metadata.
        filename (str): The path of the file to write the metadata to.
    """
    with ExifToolHelper() as e:
        metadata = e.get_metadata(json_file)[0]
        
        # Get the geoData
        latitude = metadata['JSON:GeoDataLatitude']
        longitude =  metadata['JSON:GeoDataLongitude']
        altitude =  metadata['JSON:GeoDataAltitude']
        if latitude and longitude and latitude != 0.0 and longitude != 0.0:
            # Convert latitude and longitude to the format expected by ExifTool
            latitude_ref = "N" if latitude >= 0 else "S"
            longitude_ref = "E" if longitude >= 0 else "W"
            latitude = abs(latitude)
            longitude = abs(longitude)

            # Update the GPSLatitude, GPSLongitude, and GPSAltitude metadata
            e.execute("-overwrite_original", f"-GPSLatitude={latitude}", f"-GPSLatitudeRef={latitude_ref}", filename)
            e.execute("-overwrite_original", f"-GPSLongitude={longitude}", f"-GPSLongitudeRef={longitude_ref}", filename)
            if altitude and altitude != 0.0:
                e.execute("-overwrite_original", f"-GPSAltitude={altitude}", filename)
                
        # Process date
        photo_taken_time = metadata['JSON:PhotoTakenTimeTimestamp']
        dt = datetime.datetime.fromtimestamp(photo_taken_time)
        exiftool_date = dt.strftime("%Y:%m:%d %H:%M:%S")
        try:
            e.execute("-overwrite_original", f"-DateTimeOriginal={exiftool_date}", filename)
            e.execute("-overwrite_original", f"-CreateDate={exiftool_date}", filename)
            e.execute("-overwrite_original", f"-FileCreateDate={exiftool_date}", filename)
            e.execute("-overwrite_original", f"-FileModifyDate={exiftool_date}", filename)
        except exceptions.ExifToolExecuteError as error:
            print(f"Error executing ExifTool command: {error}")