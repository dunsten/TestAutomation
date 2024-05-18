# Embedded Systems Automation Testing Take-Home Test

## Overview

This take-home test is designed to evaluate candidates' skills in embedded systems, automation testing, and continuous integration workflows. The task involves creating a mock for a Data Acquisition (DAQ) device using the NI-DAQmx Python library, simulating digital pins being toggled on and off at a specific rate, and writing tests to verify this behavior. The final step will involve setting up a CI/CD pipeline using GitHub Actions to automate the testing process.

## Objectives

- **Create a Mock DAQ Device:** Implement a mock a DAQ device `NI USB-6001` that can simulate digital input/output operations. You can use as base the NI-DAQmx Python library.
- **Simulate Pin Toggling:** Simulate toggling a digital pin on and off at a rate of once every second with some tolerance.
- **Write Tests:** Develop tests in Python to check the correctness of the pin toggling simulation.
- **CI/CD Integration:** Setup a GitHub Actions workflow to automatically run tests on each push or pull request.

## Requirements

- **Python:** Knowledge of Python programming.
- **Embedded devices:** Familiarity with Embedded devices and interfacing with DAQ devices.
- **Testing Frameworks:** Experience with Python testing frameworks like `unittest` or `pytest`.
- **GitHub Actions:** Understanding of GitHub Actions for CI/CD pipelines.

## Task Breakdown

### 1. Create a Mock DAQ Device

Create a Python class that mocks the functionalities of a DAQ device. This class should include methods to:
- Initialize the device.
- Configure digital channels for input and output.
- Read from and write to digital pins.
There is no need to implement other functionalities like analog I/O.

### 2. Simulate Pin Toggling

Implement a function in your mock that toggles a digital **input** pin on and off every second. Ensure there is a mechanism to verify the timing aspect, allowing for a small degree of tolerance (e.g., ±10 milliseconds).

You can imagine that your DAQ device would be recieving the digital signal from an external signal generator. In a real deployment both the DAQ mock and this pin toggling function would be replaced by real hardware.

### 3. Write Tests

Develop a suite of tests using a Python testing framework to ensure the mock behaves as expected. This should include:
- Testing the toggle rate of the digital pin.
- Validating the accuracy of the timing mechanism.
- Checking the state of the digital pin after each toggle.

Additionaly write some logic that would toggle ON another digital **output** pin indicating if any of the tests have failed.

### 4. CI/CD Integration

Setup a GitHub Actions workflow to automate the execution of your tests. The workflow should:
- Be triggered on every push to the `main` branch and pull requests.
- Run the entire suite of tests.
- Provide feedback on the success or failure of the tests.

## Evaluation Criteria

- **Code Quality:** Readability, use of proper abstractions, and adherence to Pythonic practices.
- **Functionality:** Accuracy of the simulation and thoroughness of the tests.
- **CI/CD Setup:** Correct configuration and efficiency of the GitHub Actions workflow.

## Resources

- [NI-DAQmx Python Library Documentation](https://nidaqmx-python.readthedocs.io/en/latest/)
- [NI-USB-6001 hardware Documentation](https://www.ni.com/docs/en-US/bundle/usb-6001-specs/resource/374369a.pdf)

Good luck!
