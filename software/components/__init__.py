import numpy as np
import cv2
from PIL import Image
import tempfile
import os

class AISystemMock:
    def __init__(self, threshold=145):
        self.threshold = threshold
    def predict(self, image):
        
        image.save("img1.png")
    # Read the image using OpenCV
        img = cv2.imread('img1.png')
        # Preprocess the image (optional)
        # You can apply techniques like blurring or histogram equalization to enhance features

        # Apply edge detection (Canny edge detector)
        edges = cv2.Canny(img, threshold1=0, threshold2=20)  # Adjust thresholds as needed

        # Find contours in the edge-detected image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on area
        min_contour_area = 10  # Adjust as needed
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

        # Iterate through the filtered contours and find the bounding box of each
        for cnt in filtered_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            patch_region = img[y:y+h, x:x+w]
    
        # Now you have the patch region, you can analyze it for the presence of defects
        # For example, you can compute statistics like mean pixel value or standard deviation
        # and compare them to predefined thresholds to detect anomalies

        # Example: Compute mean pixel value of the patch region
            mean_pixel_value = np.mean(patch_region)

        # Example: Define a threshold for defect detection
            threshold = 50  # Adjust as needed

        # Example: Check if defect is present based on mean pixel value and threshold
            defect_present = mean_pixel_value < threshold
            print(mean_pixel_value)
        return defect_present