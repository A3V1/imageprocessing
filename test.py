import cv2
import numpy as np

def display_menu():
    print("\n=== Image Processing Menu ===")
    print("1. View Original Image")
    print("2. View Grayscale Image")
    print("3. View Equalized Image")
    print("4. View Compressed Image")
    print("5. Apply Edge Detection")
    print("6. Apply DCT Compression")
    print("7. Apply Wavelet Compression")
    print("8. Apply Gaussian Blur")
    print("9. Apply Sharpening")
    print("10. Resize Image")
    print("11. Crop Image")
    print("12. Rotate Image")
    print("13. Flip Image")
    print("14. Add Text Annotation")
    print("15. Save Image")
    print("16. Add Text Watermark")
    print("17. Remove Watermark")
    print("18. Apply Color Space Conversion")
    print("19. Invert Image")
    print("20. Apply Histogram Equalization")
    print("0. Exit")
    choice = int(input("Enter your choice: "))
    return choice

def process_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray_image)
    
    # Compress the original image
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 5]
    _, buffer = cv2.imencode('.jpg', image, encode_param)
    compressed_image = cv2.imdecode(buffer, 1)

    while True:
        choice = display_menu()
        if choice == 1:
            cv2.imshow("Original Image", image)
            cv2.waitKey(0)
        elif choice == 2:
            cv2.imshow("Grayscale Image", gray_image)
            cv2.waitKey(0)
        elif choice == 3:
            cv2.imshow("Equalized Image", equalized_image)
            cv2.waitKey(0)
        elif choice == 4:
            cv2.imshow("Compressed Image", compressed_image)
            cv2.waitKey(0)
        elif choice == 5:
            apply_edge_detection(image)
        elif choice == 6:
            dct_image = apply_dct_compression(image)
            cv2.imshow("DCT Compressed Image", dct_image)
            cv2.waitKey(0)
        elif choice == 7:
            wavelet_image = apply_wavelet_compression(gray_image)
            cv2.imshow("Wavelet Compressed Image", wavelet_image)
            cv2.waitKey(0)
        elif choice == 8:
            apply_gaussian_blur(image)
        elif choice == 9:
            apply_sharpening(image)
        elif choice == 10:
            resize_image(image)
        elif choice == 11:
            crop_image(image)
        elif choice == 12:
            rotate_image(image)
        elif choice == 13:
            flip_image(image)
        elif choice == 14:
            add_text_annotation(image)
        elif choice == 15:
            save_image(image)
        elif choice == 16:
            add_text_watermark(image, "Watermark", (50, 50), 1, (255, 255, 255))
        elif choice == 17:
            remove_watermark(image, (50, 50, 100, 30))
        elif choice == 18:
            apply_color_space_conversion(image)
        elif choice == 19:
            invert_image(image)
        elif choice == 20:
            apply_histogram_equalization(image)
        elif choice == 0:
            break
        else:
            print("Invalid choice. Please try again.")

def save_image(image):
    filename = input("Enter filename to save the image (e.g., C:/imagescv/output.jpg): ")
    if cv2.imwrite(filename, image):
        print(f"Image saved successfully as {filename}")
    else:
        print("Error saving image!")

def ask_to_save_image(image):
    choice = input("Do you want to save this image? (y/n): ").lower()
    if choice == 'y':
        save_image(image)

def apply_edge_detection(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel_image = cv2.Sobel(gray_image, cv2.CV_64F, 1, 1)
    cv2.imshow("Sobel Edge Detection", sobel_image)
    cv2.waitKey(0)
    canny_image = cv2.Canny(gray_image, 100, 200)
    cv2.imshow("Canny Edge Detection", canny_image)
    cv2.waitKey(0)
    ask_to_save_image(canny_image)

def apply_dct_compression(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = np.float32(gray_image)
    dct_image = cv2.dct(gray_image)
    idct_image = cv2.idct(dct_image)
    idct_image = np.uint8(idct_image)
    return idct_image

def apply_wavelet_compression(image):
    # This is a simplified version of wavelet transform, use pywt for better results.
    return cv2.GaussianBlur(image, (5, 5), 0)

def apply_gaussian_blur(image):
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    cv2.imshow("Gaussian Blur", blurred_image)
    cv2.waitKey(0)
    ask_to_save_image(blurred_image)

def apply_sharpening(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(image, -1, kernel)
    cv2.imshow("Sharpened Image", sharpened_image)
    cv2.waitKey(0)
    ask_to_save_image(sharpened_image)

def resize_image(image):
    resized_image = cv2.resize(image, None, fx=0.5, fy=0.5)
    cv2.imshow("Resized Image", resized_image)
    cv2.waitKey(0)
    ask_to_save_image(resized_image)

def crop_image(image):
    roi = image[50:150, 50:150]
    cv2.imshow("Cropped Image", roi)
    cv2.waitKey(0)
    ask_to_save_image(roi)

def rotate_image(image):
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow("Rotated Image", rotated_image)
    cv2.waitKey(0)
    ask_to_save_image(rotated_image)

def flip_image(image):
    flipped_image = cv2.flip(image, 1)  # Horizontal flip
    cv2.imshow("Flipped Image", flipped_image)
    cv2.waitKey(0)
    ask_to_save_image(flipped_image)

def add_text_annotation(image):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, "Hello, OpenCV!", (10, 30), font, 1, (255, 255, 255), 2)
    cv2.imshow("Annotated Image", image)
    cv2.waitKey(0)
    ask_to_save_image(image)

def add_text_watermark(image, text, position, font_size, color):
    watermarked_image = image.copy()
    cv2.putText(watermarked_image, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_size, color, 2)
    cv2.imshow("Watermarked Image", watermarked_image)
    cv2.waitKey(0)
    ask_to_save_image(watermarked_image)

def remove_watermark(image, watermark_area):
    roi = image[watermark_area[1]:watermark_area[1]+watermark_area[3], watermark_area[0]:watermark_area[0]+watermark_area[2]]
    roi[:] = (0, 0, 0)  # Replace with black or desired color
    cv2.imshow("Watermark Removed", image)
    cv2.waitKey(0)
    ask_to_save_image(image)

def apply_color_space_conversion(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV Color Space", hsv_image)
    cv2.waitKey(0)
    ask_to_save_image(hsv_image)

def invert_image(image):
    inverted_image = cv2.bitwise_not(image)
    cv2.imshow("Inverted Image", inverted_image)
    cv2.waitKey(0)
    ask_to_save_image(inverted_image)

def apply_histogram_equalization(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray_image)
    cv2.imshow("Histogram Equalized Image", equalized_image)
    cv2.waitKey(0)
    ask_to_save_image(equalized_image)

if __name__ == "__main__":
    image = cv2.imread("C:/imagescv/lenna.png")
    if image is None:
        print("Could not open or find the image!")
    else:
        process_image(image)
