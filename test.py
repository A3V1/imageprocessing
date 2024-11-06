import cv2

# Load an image (replace 'image.jpg' with the path to your image)
image = cv2.imread('image.jpg')

# Check if the image was loaded properly
if image is None:
    print("Error: Image not found.")
else:
    # Display the image in a window
    cv2.imshow('Test Image', image)

    # Wait for a key press indefinitely or for a specified amount of time (in ms)
    cv2.waitKey(0)

    # Close all OpenCV windows
    cv2.destroyAllWindows()