## Software Project Documentation

## Overview:

1. **AI.py**: Implements a mock AI system for defect detection, including image preprocessing and defect prediction.

2. **camera.py**: Simulates a camera by generating images with random noise, optionally containing defects, and varying lighting conditions.

3. **database.py**: Manages a SQLite database for logging test results, including creating tables and logging test outcomes.

4. **integrate_system.py**: Integrates the AI system, camera simulation, and database management to capture images, analyze them for defects, and log results.

5. **test_integration.py**: Contains unit tests to validate the functionality of the integrated system, including logging test results and defect detection accuracy.

## Project Structure:

1. AI.py:
   - Contains the `AISystemMock` class responsible for simulating an AI system for defect detection.
   - Implements methods for preprocessing images (`preprocess_image`), to detect defects `detect_defect`and predicting defects (`predict`) to an input image.

2. camera.py:
   - Defines the `CameraMock` class simulating a camera system.
   - Provides a method `capture` to generate images with random noise, optionally containing defects, and varying lighting conditions.

3. database.py:
   - Implements the `Database` class for managing a SQLite database.
   - Contains methods for creating tables (`create_table`), logging test results (`log_result`), and closing the database connection (`close`).

4. integrate_system.py:
   - Combines the `AI system`, `camera simulation`, and `database management` to create the integration system.
   - Defines the `IntegrationSystem` class responsible for capturing images, analyzing them for defects, and logging results and .

5. test_integration.py:
   - Contains unit tests for validating the functionality of the integrated system.
   - Consists of methods to Test the logging functionality by capturing images with and without defects, and verifying the logged results in the database, and Validates the defect detection capability by capturing images with and without defects, and ensuring the AI system predicts the presence or absence of defects accurately

Overall, the project follows a modular structure where each script encapsulates specific functionalities related to AI, camera simulation, database management, system integration, and testing.

## Instructions

# Installation
1. Clone the Mock_DAQ repository from GitHub - https://github.com/dunsten/TestAutomation.git
2. Ensure Python 3.x is installed on your system.
3. Install the necessary dependencies using `pip install -r requirements.txt`.
4. Run the integration system by executing the `integrate_system.py` script in the `TestAutomation/software/components`.
5. After running the integration system, you can view the test results in the SQLite database, by opening the `DB Browser`
6. Run the unit tests, execute the `test_integration.py` script
7. After running the tests, review the output in the terminal to ensure all tests pass successfully.

Class: MockDAQDevice
## Methods

# AI.py
# Class: `AISystemMock`
- **`preprocess_image(self, image)`**:
  - Saves the provided PIL image to a temporary file.
  - Reads the image using OpenCV.
  - Applies different filters and denoising techniques to preprocess the image.
  - Saves the preprocessed image and returns the path to the preprocessed image.

- **`detect_defect(self, image_path)`**:
  - Reads the preprocessed image in grayscale.
  - Applies Canny edge detection to find edges in the image.
  - Searches for contours in the edge-detected image.
  - Checks if any contour forms a patch that resembles a defect and returns `True` if a defect is detected, otherwise `False`.

- **`predict(self, image)`**:
  - Combines the preprocessing and defect detection steps.
  - Takes a PIL image, preprocesses it, and detects defects.
  - Returns whether a defect is present in the image.

# camera.py
# Class: `CameraMock`
- **`capture(self, with_defect=False, low_lighting=True)`**:
  - Generates an image with random noise.
  - Optionally introduces a defect in the image.
  - Adjusts noise levels based on lighting conditions.
  - Converts the generated numpy array to a PIL image and returns it.

# database.py
# Class: `Database`
- **`__init__(self, db_name="test_results.db")`**:
  - Initializes a connection to the SQLite database.
  - Calls `create_table` method to ensure the results table exists.

- **`create_table(self)`**:
  - Creates a table named `results` in the database if it does not already exist.

- **`log_result(self, image_id, defect_detected)`**:
  - Inserts a new record into the `results` table with the given image ID and defect detection result.

- **`close(self)`**:
  - Closes the connection to the database.

# integrate_system.py
# Class: `IntegrationSystem`
- **`__init__(self, threshold=145, db_name='test_results.db')`**:
  - Initializes instances of `AISystemMock`, `CameraMock`, and `Database`.
  - Sets the initial image ID to zero.

- **`capture_and_analyze(self, with_defect=True, low_lighting=True)`**:
  - Captures an image using the `CameraMock` instance.
  - Analyzes the captured image for defects using the `AISystemMock` instance.
  - Logs the result (image ID and defect detection) in the database.
  - Increments the image ID for the next capture.

- **`run(self, capture_interval=1, capture_count=10)`**:
  - Runs the integration system for a specified number of captures at specified intervals.
  - Calls `capture_and_analyze` repeatedly and waits for the specified interval between captures.
  - Closes the database connection after completing the captures.

# test_integration.py
# Class: `TestIntegrationSystem`
- **`setUp(self)`**:
  - Sets up the test environment by creating an instance of `IntegrationSystem` with a test database.

- **`tearDown(self)`**:
  - Cleans up the test environment by closing the database connection and removing the test database file.

- **`test_logging_results(self)`**:
  - Tests logging of results by capturing and analyzing images with different conditions (with and without defects, with and without low lighting).
  - Verifies that the results are correctly logged in the database.

- **`test_defect_detection(self)`**:
  - Tests the defect detection functionality by capturing images with and without defects and with different lighting conditions.
  - Verifies that the `AISystemMock` instance correctly detects the presence or absence of defects in the images.

### Summary:
- **AI.py**: Contains methods for preprocessing images and detecting defects.
- **camera.py**: Contains methods for capturing images with simulated defects and noise.
- **database.py**: Contains methods for managing a SQLite database to log results.
- **integrate_system.py**: Contains methods to integrate the camera, AI system, and database for capturing and analyzing images, and logging results.
- **test_integration.py**: Contains methods to set up and tear down the test environment, and tests to verify the logging and defect detection functionality of the integration system.

# New concepts that I learnt here:

1) Importance of denoising an image using `Kernels` and denosiing techniques like `Gaussian Blur`.
2) Using Canny edges and Contout detection to find the 10x10 patch when introducing noise or LowLightning=True.
3) Playing around with sqlite3.
4) I tried implementing the front-end stuff, but I was having some issues with my windows where the OS crashes when trying to install NODE.JS Unfortunately, i did not implement that part of the integration in this take-home exam. But will look into this further and work on it after the test submission.

# What are the different Test scenarios?

The `TestIntegrationSystem` class in `test_integration.py` is designed to test the functionality of the integration system that combines the camera, AI defect detection, and database logging components. Below is a detailed explanation of each test case scenario.

#### `setUp` Method
The `setUp` method is called before each test case to set up the test environment. It creates an instance of the `IntegrationSystem` and initializes the database for testing, where we set the threshold and dbname.

#### `tearDown` Method
The `tearDown` method is called after each test case to clean up the test environment. It closes the database connection and removes the test database file.

#### `test_logging_results` Method
This test case verifies that the results of the defect detection process are correctly logged into the database. It captures images under different conditions (with and without defects, with and without low lighting) and checks the database entries.

1. **Capture and Analyze Images**:
   - `with_defect=True, low_lighting=False`: An image with a defect and normal lighting.
   - `with_defect=False, low_lighting=False`: An image without a defect and normal lighting.
   - `with_defect=True, low_lighting=True`: An image with a defect and low lighting.
   - `with_defect=False, low_lighting=True`: An image without a defect and low lighting.

2. **Verify Database Entries**:
   - Reopen the database and fetch all results.
   - Check that four entries are logged.
   - Verify that the entries correspond correctly to the captured conditions.
    
#### `test_defect_detection` Method
This test case verifies the defect detection capabilities of the AI system under different conditions. It captures images with and without defects, under both normal and low lighting conditions, and checks the AI system's predictions.

1. **Test with Defect (Normal Lighting)**:
   - Capture an image with a defect and normal lighting.
   - Assert that the AI system correctly detects the defect.

2. **Test without Defect (Normal Lighting)**:
   - Capture an image without a defect and normal lighting.
   - Assert that the AI system correctly identifies the absence of a defect.

3. **Test with Defect (Low Lighting)**:
   - Capture an image with a defect and low lighting.
   - Assert that the AI system correctly detects the defect.

4. **Test without Defect (Low Lighting)**:
   - Capture an image without a defect and low lighting.
   - Assert that the AI system correctly identifies the absence of a defect.

### Summary of Test Case Scenarios
1. **Logging Results**: Ensures that the system correctly logs the results of defect detection in the database.
2. **Defect Detection**: Ensures that the AI system accurately detects defects and the absence of defects under both normal and low lighting conditions.

These test cases cover critical aspects of the integration system, ensuring that both the logging mechanism and the defect detection functionality work correctly under different scenarios.

# Images:
Added the database image screenshot in the directory `/software/components`