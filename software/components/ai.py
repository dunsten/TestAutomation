import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

"""class AISystemMock:
    def __init__(self, threshold=155):
        self.threshold = threshold
    def predict(self, image):
        image_array = np.array(image)
        print("Max Value of Image Array", np.max(image_array))
        defect_present = np.any(image_array > self.threshold)
        return defect_present"""

class AISystemMock:
    def preprocess_image(self, image):
        
        """Apply adaptive preprocessing steps to the image to reduce noise and enhance features."""
        # Save the image to a temporary file
        image_path = "temp_img.png"
        image.save(image_path)

        # Read the image using OpenCV
        img = cv2.imread(image_path,1)

        # Creating a Kernel mask
        kernel = np.ones((3,3),np.float32)/9
        filt_2d = cv2.filter2D(img, -1, kernel)
        blur = cv2.blur(img, (3,3))

        # Using Gauss Blur
        gauss_blur = cv2.GaussianBlur(img, (9,9), 0)

        dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

        # Remove the temporary image file
        cv2.imwrite(image_path, gauss_blur)
        
        return image_path
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def detect_defect(self, image_path):
        """Detect the defect in the preprocessed image using Canny edge detection."""
        # Read the preprocessed image using OpenCV
        preprocessed_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        # Apply Canny edge detection
        edges = cv2.Canny(preprocessed_image, 30, 150)

        # Shows the Edges with 10x10 patch
        cv2.imshow("edges",edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Find contours in the edge-detected image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate through the contours to find a 10x10 patch
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if 8 <= w <= 12 and 8 <= h <= 12 and abs(w - h) <= 2:
                return True
        
        return False
    
    def predict(self, image):
        """Predict whether the image contains a defect."""
        # Preprocess the image adaptively
        image_path = self.preprocess_image(image)
        
        # Detect the defect in the preprocessed image using Canny edge detection
        defect_present = self.detect_defect(image_path)
        
        # Return the prediction
        return defect_present
