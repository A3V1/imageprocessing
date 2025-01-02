# image_processing/basic_operations.py
from PIL import Image, ImageDraw

def rotate_image(image, angle):
    return image.rotate(angle)
    
def resize_image(image, dimensions):
    return image.resize(dimensions)

def crop_image(image, box):
    
    width, height = image.size
    left, top, right, bottom = box
    
    left = max(0, min(left, width))
    top = max(0, min(top, height))
    right = max(0, min(right, width))
    bottom = max(0, min(bottom, height))
    
    # Ensure right > left and bottom > top
    if right <= left or bottom <= top:
        return image
        
    return image.crop((left, top, right, bottom))