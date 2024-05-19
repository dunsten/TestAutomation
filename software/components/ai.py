import cv2
import numpy as np

class AISystemMock:
    def preprocess_image(self, image):
        """Apply preprocessing steps to the image to reduce noise."""
        
        image.save("img1.png")
        # Read the image using OpenCV
        img = cv2.imread('img1.png')
        # Preprocess the image (optional)
        # You can apply techniques like blurring or histogram equalization to enhance features
        # Convert PIL image to OpenCV format
        cv2.imshow('Image', img)
        cv2.waitKey(0)  # Wait for a key press to proceed
        cv2.destroyAllWindows()  # Close the image windows

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(img, (3, 3), 0)

        # Convert to grayscale
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

        # Show grayscale image
        cv2.imshow('Grayscale Image', gray)
        cv2.waitKey(0)  # Wait for a key press to proceed
        cv2.destroyAllWindows()  # Close the image windows
        
        return gray
    
    def detect_defect(self, preprocessed_image):
        """Detect the defect in the preprocessed image."""
        # Apply adaptive threshold to handle varying lighting conditions
        thresh = cv2.adaptiveThreshold(preprocessed_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Iterate through the contours to find a 10x10 patch
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if 8 <= w <= 12 and 8 <= h <= 12:
                return True
        
        return False
    
    def predict(self, image):
        """Predict whether the image contains a defect."""
        preprocessed_image = self.preprocess_image(image)
        defect_present = self.detect_defect(preprocessed_image)
        return defect_present
