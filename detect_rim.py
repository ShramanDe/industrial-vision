import cv2
import numpy as np

# Load the image
image = cv2.imread("good_cap.jpeg")

if image is None:
    print("Could not load good_cap.jpeg")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Smooth the image
blurred = cv2.GaussianBlur(gray, (9, 9), 2)

# Detect circles
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=100,
    param1=100,
    param2=40,
    minRadius=150,
    maxRadius=400
)

if circles is None:
    print("No circles detected.")
    exit()

# Convert circle values to integers
circles = np.round(circles[0]).astype(int)

print("Circles detected:", len(circles))

# Draw detected circles
output = image.copy()

for x, y, r in circles:
    cv2.circle(output, (x, y), r, (0, 255, 0), 3)
    cv2.circle(output, (x, y), 3, (0, 0, 255), -1)

    print(f"Circle center: ({x}, {y}), radius: {r}")

# Save result
cv2.imwrite("detected_rim.jpg", output)

print("Result saved as detected_rim.jpg")