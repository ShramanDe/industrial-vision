import cv2

# Load the image
image = cv2.imread("test.jpeg")

if image is None:
    print("Image could not be loaded.")
    exit()

print("Image loaded successfully!")
print("Image dimensions:", image.shape)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply binary threshold
_, thresholded = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# Save the thresholded image
cv2.imwrite("thresholded.jpg", thresholded)

print("Thresholded image saved as thresholded.jpg")