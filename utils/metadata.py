from PIL import Image
import os

def get_image_metadata(image):
    
    if image is None:
        return {}

    metadata = {
        "format": image.format,
        "mode": image.mode,
        "size": image.size,
    }
    return metadata

def save_metadata(image, file_path):
    
    metadata = get_image_metadata(image)
    metadata_file_path = os.path.splitext(file_path)[0] + "_metadata.txt"
    
    with open(metadata_file_path, 'w') as f:
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")
