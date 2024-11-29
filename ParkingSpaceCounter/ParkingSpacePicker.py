import cv2 as cv
import pickle

width, height = 107, 48

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    print("No existing positions found. Starting fresh.")
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv.EVENT_LBUTTONDOWN:
        posList.append((x, y))
        print(f"Added position: {x}, {y}")
    
    if events == cv.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                print(f"Removed position: {x1}, {y1}")
                posList.pop(i)
                break  # Stop after removing one rectangle
    
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


while True:
    img = cv.imread("carParkImg.png")
    if img is None:
        print("Error: Could not load image. Check the file path.")
        break

    for pos in posList:
        cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv.imshow("Image", img)
    cv.setMouseCallback("Image", mouseClick)
    
    if cv.waitKey(1) & 0xFF == ord('q'):  # Exit loop when 'q' is pressed
        print("Exiting...")
        break
