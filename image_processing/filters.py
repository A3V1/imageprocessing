# image_processing/filters.py
from PIL import ImageFilter
from PIL import ImageEnhance

def apply_blur(image, radius=4):
    return image.filter(ImageFilter.GaussianBlur(radius))

def apply_sharpen(image, factor=2.0):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

