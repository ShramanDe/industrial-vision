import cv2

# Load the reference image
image = cv2.imread("good_cap.jpeg")

if image is None:
    print("Could not load good_cap.jpeg")
    exit()

print("Image loaded successfully!")
print("Image dimensions:", image.shape)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Reduce small image noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Detect edges
edges = cv2.Canny(blurred, 50, 150)

# Save intermediate results
cv2.imwrite("gray_cap.jpg", gray)
cv2.imwrite("edges_cap.jpg", edges)

print("Grayscale image saved.")
print("Edge image saved.")