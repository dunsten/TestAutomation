import unittest
import os
from ai import AISystemMock
from camera import CameraMock
from database import Database
from integrate_system import IntegrationSystem
import sqlite3
from PIL import Image

class TestIntegrationSystem(unittest.TestCase):
    def setUp(self):
        """Set up the test environment before each test."""
        print("\nSetting up the test environment...")
        self.db_name = "test_results.db"
        self.integration_system = IntegrationSystem(threshold=145, db_name=self.db_name)
        print("Test environment set up complete.\n")

    def tearDown(self):
        """Tear down the test environment after each test."""
        print("Tearing down the test environment...")
        # Close the database connection before removing the file
        self.integration_system.database.close()
        # Remove the database file
        os.remove(self.db_name)
        print("Test environment torn down.\n")

    def test_logging_results(self):
        """Test that the system correctly logs results in the database."""
        print("Starting test for logging results...\n")

        # Capture and analyze with different conditions
        print("Capturing and analyzing image with defect, normal lighting...")
        self.integration_system.capture_and_analyze(with_defect=True, low_lighting=False)

        print("Capturing and analyzing image without defect, normal lighting...")
        self.integration_system.capture_and_analyze(with_defect=False, low_lighting=False)

        print("Capturing and analyzing image with defect, low lighting...")
        self.integration_system.capture_and_analyze(with_defect=True, low_lighting=True)

        print("Capturing and analyzing image without defect, low lighting...")
        self.integration_system.capture_and_analyze(with_defect=False, low_lighting=True)

        print("Reopening the database to verify results...")
        # Reopen the connection for verification
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM results")
        rows = cursor.fetchall()
        conn.close()

        print(f"Total results logged: {len(rows)}")
        for row in rows:
            print(f"Image ID: {row[1]}, Defect Detected: {row[2]}")

        # Assertions to check the logging results
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0][2], 1)  # Defect present
        self.assertEqual(rows[1][2], 0)  # No defect
        self.assertEqual(rows[2][2], 1)  # Defect present with Low Lighting
        self.assertEqual(rows[3][2], 0)  # No defect present with Low Lighting

        print("Test for logging results completed.\n")

    def test_defect_detection(self):
        """Test the AI system's ability to detect defects."""
        print("Starting test for defect detection...\n")

        print("Capturing image with defect, normal lighting...")
        image_with_defect = self.integration_system.camera.capture(with_defect=True, low_lighting=False)
        print("Predicting defect presence in image with defect, normal lighting...")
        self.assertTrue(self.integration_system.ai_system.predict(image_with_defect))

        print("Capturing image without defect, normal lighting...")
        image_without_defect = self.integration_system.camera.capture(with_defect=False, low_lighting=False)
        print("Predicting defect absence in image without defect, normal lighting...")
        self.assertFalse(self.integration_system.ai_system.predict(image_without_defect))

        print("Capturing image with defect, low lighting...")
        image_low_light_with_defect = self.integration_system.camera.capture(with_defect=True, low_lighting=True)
        print("Predicting defect presence in image with defect, low lighting...")
        self.assertTrue(self.integration_system.ai_system.predict(image_low_light_with_defect))

        print("Capturing image without defect, low lighting...")
        image_low_light_no_defect = self.integration_system.camera.capture(with_defect=False, low_lighting=True)
        print("Predicting defect absence in image without defect, low lighting...")
        self.assertFalse(self.integration_system.ai_system.predict(image_low_light_no_defect))

        print("Test for defect detection completed.\n")

if __name__ == '__main__':
    unittest.main()
