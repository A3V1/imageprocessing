# image_processing/edge_detection.py

from PIL import Image
from PIL import ImageFilter

def find_edges(image):
   
   return image.filter(ImageFilter.FIND_EDGES)