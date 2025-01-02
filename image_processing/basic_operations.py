# image_processing/basic_operations.py
from PIL import Image

def rotate_image(image, angle):
    return image.rotate(angle)
    
def resize_image(image,dimensions):
    return image.resize(dimensions)

def crop_image(image, box):
    return image.crop(box)