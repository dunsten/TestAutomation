# test_integration.py
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
        self.db_name = "test_results.db"
        self.integration_system = IntegrationSystem(threshold=145, db_name=self.db_name)

    def tearDown(self):
        # Ensure the database connection is closed before removing the file
        self.integration_system.database.close()
        os.remove(self.db_name)

    def test_logging_results(self):
        # Capture and analyze with a defect and without a defect
        self.integration_system.capture_and_analyze(with_defect=True)
        self.integration_system.capture_and_analyze(with_defect=False)
        self.integration_system.capture_and_analyze(with_defect=True, low_lighting=True)
        self.integration_system.capture_and_analyze(with_defect=False, low_lighting=True)

        # Reopen the connection for verification
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM results")
        rows = cursor.fetchall()
        conn.close()
        
         # Assertions to check the logging results
        self.assertEqual(len(rows), 4)
        self.assertEqual(int.from_bytes(rows[0][2], "little"), 1)  # Defect present
        self.assertEqual(int.from_bytes(rows[1][2], "little"), 0)  # No defect
        self.assertEqual(int.from_bytes(rows[2][2], "little"), 1)  # Defect present with Low Lightning
        self.assertEqual(int.from_bytes(rows[3][2], "little"), 0)  # No defect present with Low Lightning

    def test_defect_detection(self):
        # Test with defect
        image_with_defect = self.integration_system.camera.capture(with_defect=True)
        self.assertTrue(self.integration_system.ai_system.predict(image_with_defect))
        
        # Test without defect
        image_without_defect = self.integration_system.camera.capture(with_defect=False)
        self.assertFalse(self.integration_system.ai_system.predict(image_without_defect))
        
        # Test with low lighting and defect
        image_low_light_with_defect = self.integration_system.camera.capture(with_defect=True, low_lighting=True)
        self.assertTrue(self.integration_system.ai_system.predict(image_low_light_with_defect))
        
        # Test with low lighting and no defect
        image_low_light_no_defect = self.integration_system.camera.capture(with_defect=False, low_lighting=True)
        self.assertFalse(self.integration_system.ai_system.predict(image_low_light_no_defect))

if __name__ == '__main__':
    unittest.main()
