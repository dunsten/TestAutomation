# integrate_system.py
import time
import random
from ai import AISystemMock
from camera import CameraMock
from database import Database

class IntegrationSystem:
    def __init__(self, threshold=145, db_name='test_results.db'):
        self.ai_system = AISystemMock()
        self.camera = CameraMock()
        self.database = Database(db_name)
        self.image_id = 0

    def capture_and_analyze(self, with_defect=True, low_lighting=False):
        
        #Randomize 'with defect', 'without defect', and 'low lighting' conditions
        #with_defect = random.choice([True, False])
        #low_lighting = random.choice([True, False])
        
        # Capture an image
        image = self.camera.capture(with_defect=with_defect, low_lighting=low_lighting)

        # Predict the presence of defects
        defect_present = self.ai_system.predict(image)

        # Log the result in the database
        self.database.log_result(self.image_id, defect_present)

        print(f"Image ID {self.image_id}: Defect present: {defect_present}")
        self.image_id += 1

    def run(self, capture_interval=1, capture_count=10):
        for _ in range(capture_count):
            self.capture_and_analyze()
            time.sleep(capture_interval)
        self.database.close()

if __name__ == "__main__":
    system = IntegrationSystem()
    system.run()