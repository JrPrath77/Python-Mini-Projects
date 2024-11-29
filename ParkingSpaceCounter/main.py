import cv2 as cv
import pickle
import cvzone
import numpy as np

# Video feed:
cap = cv.VideoCapture("carPark.mp4")  # Relative path for the video

# Load parking positions:
with open('CarParkPos', 'rb') as f: 
    posList = pickle.load(f)

width, height = 107, 48

def checkParkingSpace(imgProcessed):
    spaceCounter = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgProcessed[y:y + height, x:x + width]
        count = cv.countNonZero(imgCrop)
        if count < 950:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free Spaces: {spaceCounter}/{len(posList)}', (0, 30), scale=2, thickness=2, offset=20, colorR=(0, 200, 0))

while True:
    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    if not success:
        print("Error: Could not read frame. Exiting.")
        break

    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv.medianBlur(imgThreshold, 5)
    kernal = np.ones((3, 3), np.uint8)
    imgDilate = cv.dilate(imgMedian, kernal, iterations=1)

    checkParkingSpace(imgDilate)
    cv.imshow("Image", img)
    if cv.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
