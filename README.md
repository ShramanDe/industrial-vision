# Industrial Vision – Bottle Cap Rim Defect Inspection

A computer vision-based industrial inspection system developed using **Python and OpenCV** to automatically detect defects in the rim of bottle caps.

The system compares a test bottle-cap image against a reference (good) cap and identifies areas where the rim edge is significantly weaker or missing.

## Project Overview

In industrial manufacturing, automated visual inspection can be used to identify defective components without relying on manual inspection.

This project implements a simple machine-vision inspection pipeline for bottle caps:

**Input Image → Preprocessing → Rim Detection → Edge Analysis → Defect Detection → PASS/FAIL**

The system uses a good bottle cap as a reference and compares the detected rim characteristics of the test image against it.

## Features

- Automatic bottle-cap rim detection
- Reference vs. test image comparison
- Gaussian blur and Canny edge detection
- Circular rim detection using Hough Circle Transform
- 360-degree rim analysis
- Detection of significant edge loss
- Defect-region grouping
- PASS/FAIL inspection decision
- Visual highlighting of detected defect regions
- Inspection result image generation

## Technologies Used

- **Python**
- **OpenCV**
- **NumPy**
- **Math / Trigonometry**
- **Computer Vision**
- **Image Processing**

## Inspection Pipeline

### 1. Image Acquisition

The system loads:

- A reference image of a good bottle cap
- A test image that may contain a defect

Example:

```text
good_cap.jpeg
defective_cap.jpg
