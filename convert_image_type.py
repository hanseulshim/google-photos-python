import os
from PIL import Image

def covert_image_type(original_path, output_path, new_extension):    
    img = Image.open(original_path)
    rgb_img = img.convert('RGB')
    rgb_img.save(output_path, new_extension)

    # Delete the original file after converting
    os.remove(original_path)