# image_processing/filters.py
from PIL import ImageFilter

def apply_blur(image, radius=4):
    return image.filter(ImageFilter.GaussianBlur(radius))

def apply_sharpen(image):
    return 