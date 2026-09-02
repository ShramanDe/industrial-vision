import cv2
import numpy as np
import math

# Load the good reference image
image = cv2.imread("good_cap.jpeg")

if image is None:
    print("Could not load good_cap.jpeg")
    exit()

# Detected circle from our good sample
x = 417
y = 697
radius = 209

defective = image.copy()

# --------------------------------------------------
# Simulate a missing section of the outer rim
# --------------------------------------------------

start_angle = 20
end_angle = 140

# Use a wide annular region around the expected rim
for angle in range(start_angle, end_angle):

    theta = math.radians(angle)

    for r in range(radius - 12, radius + 13):

        px = int(x + r * math.cos(theta))
        py = int(y + r * math.sin(theta))

        if (
            0 <= py < defective.shape[0]
            and 0 <= px < defective.shape[1]
        ):
            # Approximate the surrounding background
            # using a nearby point outside the cap.
            bg_r = radius + 30

            bg_x = int(x + bg_r * math.cos(theta))
            bg_y = int(y + bg_r * math.sin(theta))

            if (
                0 <= bg_y < defective.shape[0]
                and 0 <= bg_x < defective.shape[1]
            ):
                defective[py, px] = defective[bg_y, bg_x]

# Save defective image
cv2.imwrite("defective_cap.jpg", defective)

print("Defective image created successfully.")