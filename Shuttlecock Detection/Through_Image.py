import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to detect shuttlecock
def detect_shuttlecock(img):
    # Read the image
    img = cv2.imread(img)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    
    # Detect circles using HoughCircles (for circular shape of shuttlecock)
    # circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=50)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=28, minRadius=10, maxRadius=50)


    # If circles are found
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        # Draw the circles on the original image
        for (x, y, r) in circles:
            cv2.circle(img, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # Show the result with detected shuttlecock
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.axis('off')  # Hide axis
        plt.show()
    else:
        print("No shuttlecock detected in the image.")

# Input image path
image_path = "s1.jpg"  # Replace with your image file path

# Detect shuttlecock in the image
detect_shuttlecock(image_path)