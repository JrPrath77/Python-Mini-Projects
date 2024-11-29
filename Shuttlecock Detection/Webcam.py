import cv2
import numpy as np

# Function to detect shuttlecock in a frame
def detect_shuttlecock(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    
    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=28, minRadius=10, maxRadius=50)
    
    # If circles are found
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        # Draw circles on the frame
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    
    return frame

# Open webcam
cap = cv2.VideoCapture(0)  # 0 is the default camera. Use 1 or other index for external cameras.

# Check if webcam is opened
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to exit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    # Detect shuttlecock in the frame
    processed_frame = detect_shuttlecock(frame)
    
    # Show the frame
    cv2.imshow("Shuttlecock Detection", processed_frame)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()