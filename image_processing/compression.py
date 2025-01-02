from PIL import Image
import io

def compress_image(image, quality=85):
    
    # Create a buffer to temporarily store the image
    buffer = io.BytesIO()
    
    # Convert image to RGB if it's in RGBA mode
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    # Save to buffer with JPEG compression
    image.save(buffer, format='JPEG', quality=quality)
    
    # Load the compressed image from buffer
    buffer.seek(0)
    compressed_image = Image.open(buffer)
    
    return compressed_image

def compress_image_size(image, max_size_kb=500):
   
    quality_min = 5
    quality_max = 95
    target_size = max_size_kb * 1024  # Convert to bytes
    
    while quality_min < quality_max:
        quality = (quality_min + quality_max) // 2
        buffer = io.BytesIO()
        
        if image.mode == 'RGBA':
            image = image.convert('RGB')
            
        image.save(buffer, format='JPEG', quality=quality)
        size = buffer.tell()
        
        if size <= target_size:
            quality_min = quality + 1
        else:
            quality_max = quality - 1
    
    return compress_image(image, quality_min)
