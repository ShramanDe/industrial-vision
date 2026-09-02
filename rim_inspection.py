import cv2
import numpy as np
import math

# ==========================================================
# 1. LOAD IMAGES
# ==========================================================

reference = cv2.imread("good_cap.jpeg")
image = cv2.imread("defective_cap.jpg")

if reference is None:
    print("Could not load good_cap.jpeg")
    exit()

if image is None:
    print("Could not load defective_cap.jpg")
    exit()

print("Reference and test images loaded successfully.")


# ==========================================================
# 2. FUNCTION TO DETECT CAP RIM
# ==========================================================

def detect_rim(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(
        gray,
        (9, 9),
        2
    )

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
        return None

    circles = np.round(circles[0]).astype(int)

    # Select the largest circle
    circle = max(circles, key=lambda c: c[2])

    return tuple(circle)


# ==========================================================
# 3. DETECT RIM IN BOTH IMAGES
# ==========================================================

ref_circle = detect_rim(reference)
test_circle = detect_rim(image)

if ref_circle is None:
    print("Could not detect reference cap rim.")
    exit()

if test_circle is None:
    print("Could not detect test cap rim.")
    exit()

rx, ry, rr = ref_circle
x, y, radius = test_circle

print(f"Reference rim: ({rx}, {ry}), radius: {rr}")
print(f"Test rim: ({x}, {y}), radius: {radius}")


# ==========================================================
# 4. CREATE EDGE IMAGES
# ==========================================================

def create_edges(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Reduce noise
    blurred = cv2.GaussianBlur(
        gray,
        (7, 7),
        1.5
    )

    edges = cv2.Canny(
        blurred,
        40,
        120
    )

    return edges


ref_edges = create_edges(reference)
test_edges = create_edges(image)


# ==========================================================
# 5. MEASURE RIM EDGE STRENGTH
# ==========================================================

number_of_angles = 360

reference_strength = []
test_strength = []

radial_range = range(-5, 6)

for angle in range(number_of_angles):

    theta = math.radians(angle)

    ref_values = []
    test_values = []

    for offset in radial_range:

        # Reference coordinates
        r = rr + offset

        px = int(rx + r * math.cos(theta))
        py = int(ry + r * math.sin(theta))

        if (
            0 <= py < ref_edges.shape[0]
            and 0 <= px < ref_edges.shape[1]
        ):
            window = ref_edges[
                max(0, py - 2):py + 3,
                max(0, px - 2):px + 3
            ]

            ref_values.append(np.count_nonzero(window))

        # Test coordinates
        r = radius + offset

        px = int(x + r * math.cos(theta))
        py = int(y + r * math.sin(theta))

        if (
            0 <= py < test_edges.shape[0]
            and 0 <= px < test_edges.shape[1]
        ):
            window = test_edges[
                max(0, py - 2):py + 3,
                max(0, px - 2):px + 3
            ]

            test_values.append(np.count_nonzero(window))

    reference_strength.append(
        max(ref_values) if ref_values else 0
    )

    test_strength.append(
        max(test_values) if test_values else 0
    )


# ==========================================================
# 6. DETECT SIGNIFICANT EDGE LOSS
# ==========================================================

failed_angles = []

for angle in range(number_of_angles):

    ref_value = reference_strength[angle]
    test_value = test_strength[angle]

    # Ignore areas where reference itself has no useful edge
    if ref_value < 3:
        continue

    # Test rim is significantly weaker than good rim
    if test_value < ref_value * 0.35:
        failed_angles.append(angle)


# ==========================================================
# 7. REMOVE ISOLATED NOISE
# ==========================================================

def group_angles(angles):

    if not angles:
        return []

    angles = sorted(angles)

    groups = []
    current = [angles[0]]

    for angle in angles[1:]:

        if angle - current[-1] <= 3:
            current.append(angle)
        else:
            groups.append(current)
            current = [angle]

    groups.append(current)

    # Merge 0° and 359° regions
    if len(groups) > 1:

        if (
            groups[0][0] <= 2
            and groups[-1][-1] >= 357
        ):

            merged = groups[-1] + groups[0]

            groups = [merged] + groups[1:-1]

    return groups


groups = group_angles(failed_angles)


# ==========================================================
# 8. FILTER VERY SMALL DEFECTS
# ==========================================================

defect_groups = []

for group in groups:

    # Require at least 4 consecutive degrees
    if len(group) >= 4:
        defect_groups.append(group)


# ==========================================================
# 9. FINAL DECISION
# ==========================================================

defect_angles = sum(
    len(group)
    for group in defect_groups
)

defect_percentage = (
    defect_angles / number_of_angles
) * 100


# Defect if meaningful rim section is missing
if defect_percentage >= 1.0:
    result = "FAIL"
else:
    result = "PASS"


print(f"Defect angles detected: {defect_angles}")
print(f"Defect percentage: {defect_percentage:.2f}%")
print(f"Defect regions detected: {len(defect_groups)}")
print(f"Inspection result: {result}")


# ==========================================================
# 10. DRAW RESULT
# ==========================================================

output = image.copy()

# Draw detected rim
cv2.circle(
    output,
    (x, y),
    radius,
    (0, 255, 0),
    3
)


# ==========================================================
# 11. HIGHLIGHT DEFECT REGIONS
# ==========================================================

for group in defect_groups:

    for angle in group:

        theta = math.radians(angle)

        px = int(
            x + radius * math.cos(theta)
        )

        py = int(
            y + radius * math.sin(theta)
        )

        cv2.circle(
            output,
            (px, py),
            5,
            (0, 0, 255),
            -1
        )

    # Draw red arc
    start_angle = group[0]
    end_angle = group[-1]

    # Handle wrap-around
    if start_angle > end_angle:
        end_angle += 360

    cv2.ellipse(
        output,
        (x, y),
        (radius, radius),
        0,
        start_angle,
        end_angle,
        (0, 0, 255),
        7
    )


# ==========================================================
# 12. DISPLAY RESULT
# ==========================================================

text_color = (
    (0, 255, 0)
    if result == "PASS"
    else
    (0, 0, 255)
)

cv2.putText(
    output,
    f"Result: {result}",
    (30, 70),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.8,
    text_color,
    4
)

cv2.putText(
    output,
    f"Defect regions: {len(defect_groups)}",
    (30, 120),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.9,
    (255, 255, 255),
    2
)

cv2.putText(
    output,
    f"Defect: {defect_percentage:.2f}%",
    (30, 160),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.9,
    (255, 255, 255),
    2
)


# ==========================================================
# 13. SAVE RESULT
# ==========================================================

cv2.imwrite(
    "inspection_result.jpg",
    output
)

print(
    "Inspection image saved as inspection_result.jpg"
)