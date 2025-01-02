# image_processing/colour_adjustments.py
from PIL import Image
from PIL import ImageEnhance

def brightness(image,factor = 1.0):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def contrast(image,factor = 1.0):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def saturation(image,factor = 1.0):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)


