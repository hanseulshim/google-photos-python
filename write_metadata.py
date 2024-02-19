import os
import datetime
import constants
from exiftool import ExifToolHelper

def write_metadata(json_file, filename):
    with ExifToolHelper() as e:
        metadata = e.get_metadata(json_file)[0]
        
        # Process date
        photo_taken_time = metadata['JSON:PhotoTakenTimeTimestamp']
        dt = datetime.datetime.fromtimestamp(photo_taken_time)
        exiftool_date = dt.strftime("%Y:%m:%d %H:%M:%S")
        e.execute("-overwrite_original", f"-DateTimeOriginal={exiftool_date}", filename)
        e.execute("-overwrite_original", f"-CreateDate={exiftool_date}", filename)
        e.execute("-overwrite_original", f"-FileCreateDate={exiftool_date}", filename)
        
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


        
        # if file extension is jpg, jpeg, or heic, find the mp4 file with same name and rename it
        

        # # Rename the file using the photo_taken_time
        # new_file_name = dt.strftime(constants.FILE_FORMAT) + file_extension
        # new_file_path = os.path.join(os.path.dirname(filename), new_file_name)

        # # Check if a file with the new name already exists
        # counter = 1
        # while os.path.exists(new_file_path):
        #     new_file_name = dt.strftime(constants.FILE_FORMAT) + f'_{counter:03}' + file_extension
        #     new_file_path = os.path.join(os.path.dirname(filename), new_file_name)
        #     counter += 1

        # os.rename(filename, new_file_path)
        e.execute("-overwrite_original", f"-FileModifyDate={exiftool_date}", filename)
        # print('Renamed file: ', filename, new_file_name)