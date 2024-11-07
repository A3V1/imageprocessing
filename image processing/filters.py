# image_processing/filters.py
from PIL import ImageFilter

def apply_blur(image, radius=2):
    return image.filter(ImageFilter.GaussianBlur(radius))
