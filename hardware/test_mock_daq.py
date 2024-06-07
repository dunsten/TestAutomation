import unittest
import time
from mock_daq import MockDAQDevice
import threading

class TestMockDAQDevice(unittest.TestCase):  #To Use the assertion methods and test management features from unit test

    def setUp(self):
        print("\nRunning setUp...")
        self.daq_device = MockDAQDevice()
        self.daq_device.configure_digital_channel('pin1', 'input')
        self.daq_device.configure_digital_channel('pin2', 'output')
        self.daq_device.configure_digital_channel('failure_pin', 'output')  # New failure indicator pin
        self.daq_device.write_digital('failure_pin', False)  # Ensure the failure pin starts from FALSE State
        self.daq_device.digital_pins['pin1']['value'] = False # Ensure the Initial States of the pin starts from FALSE State, in reality this shud come from the hardware
        self.daq_device.digital_pins['pin2']['value'] = False # Ensure the Initial States of the pin starts from FALSE State 
        self.pin_statuses = []  # List to track pin statuses
        print("\nSetup complete: Configured 'pin1' as input, 'pin2' as output, and 'failure_pin' as output.")
        self.threads = []
        self.addCleanup(self.cleanup)  # Register cleanup method

    def cleanup(self):
        print("\nRunning cleanup...")
        self.daq_device.stop_toggle()
        for thread in self.threads:
            if thread.is_alive():
                thread.join()
        print("Cleanup complete: Stopped any ongoing toggling and joined all threads.")

    def tearDown(self):
        print("\nRunning tearDown...")
        # Run cleanup
        self.cleanup()

        # Check if there were any failures or errors in the test result
        result = self._outcome.result
        if any(error for (test, error) in result.errors) or any(failure for (test, failure) in result.failures):
            self.daq_device.write_digital('failure_pin', True)
            print("Failure detected: Toggling failure_pin ON")
        # Append the latest pin statuses to the list
        current_status = self.get_pin_status()
        self.pin_statuses.append(current_status)
        # Print the latest pin status
        self.print_latest_pin_status()

    def get_pin_status(self):
        """Get the current status of all pins."""
        status = {}
        for pin in ['pin1', 'pin2', 'failure_pin']:
            status[pin] = self.daq_device.digital_pins[pin]['value']
        return status

    def print_pin_status(self):
        """Print the latest pin statuses."""
        print("Latest pin statuses:")
        for status in self.pin_statuses:
            for pin, value in status.items():
                print(f"{pin}: {value}")
        print("\n")

    def print_latest_pin_status(self):
        """Print the latest pin status explicitly."""
        if self.pin_statuses:
            latest_status = self.pin_statuses[-1]
            print("Latest pin statuses after test:")
            for pin, value in latest_status.items():
                print(f"{pin}: {value}")
            print("\n")
        else:
            print("No pin statuses recorded yet.\n")

    def test_initial_state(self):
        """Test initial state of the pins."""
        print("Testing initial state of the pins...")
        pin1_initial = self.daq_device.read_digital('pin1')
        pin2_initial = self.daq_device.digital_pins['pin2']['value']
        print(f"Initial state - Pin1: {pin1_initial}, Pin2: {pin2_initial}")
        self.assertFalse(pin1_initial)
        self.assertFalse(pin2_initial)
        print("Initial state test passed.")
        self.print_latest_pin_status()

    def test_write_digital(self):
        """Test writing to the output pin."""
        print("Testing write operation to pin2 (output pin)...")
        self.daq_device.write_digital('pin2', True)
        pin2_value = self.daq_device.digital_pins['pin2']['value']
        print(f"Pin2 value after write: {pin2_value}")
        self.assertTrue(pin2_value)

        print("Testing write operation to Failure Pin (output pin)...")
        self.daq_device.write_digital('failure_pin', True)
        failure_pin_value = self.daq_device.digital_pins['failure_pin']['value']
        print(f"Failure pin value after write: {failure_pin_value}")
        self.assertTrue(failure_pin_value)
        self.daq_device.write_digital('failure_pin', False)

        print("Write operation test passed.")
        self.print_latest_pin_status()

    def test_toggle_pins(self):
        """Test that pin1 toggles every second and pin2 is the opposite of pin1."""
        print("Starting toggle test for pin1 and pin2 with 1-second interval...")
        self.daq_device.start_toggle('pin1', 'pin2', 1.0, tolerance=0.01)
        self.addCleanup(self.daq_device.stop_toggle)  # Ensure toggling stops even if the test fails

        time.sleep(2.1)  # Wait for a little more than 2 seconds to observe two toggles

        # Check the state after the first toggle
        pin1_value_first = self.daq_device.read_digital('pin1')
        pin2_value_first = self.daq_device.digital_pins['pin2']['value']
        print(f"State after first toggle - Pin1: {pin1_value_first}, Pin2: {pin2_value_first}")
        self.assertNotEqual(pin1_value_first, pin2_value_first)

        time.sleep(1.1)  # Wait for a little more than 1 second to observe another toggle

        # Check the state after the second toggle
        pin1_value_second = self.daq_device.read_digital('pin1')
        pin2_value_second = self.daq_device.digital_pins['pin2']['value']
        print(f"State after second toggle - Pin1: {pin1_value_second}, Pin2: {pin2_value_second}")
        self.assertNotEqual(pin1_value_second, pin2_value_second)

        # Verify that pin1 has toggled
        self.assertNotEqual(pin1_value_first, pin1_value_second)
        # Verify that pin2 has also toggled to be the opposite of pin1
        self.assertEqual(pin1_value_second, not pin2_value_second)

        print("Toggle test passed. Stopping toggle process.")
        # Stop toggling
        self.daq_device.stop_toggle()
        self.print_latest_pin_status()

    def test_timing_mechanism(self):
        """Validate the timing mechanism with a tolerance."""
        print("Starting timing mechanism test with 1-second interval and 0.01-second tolerance...")
        self.daq_device.start_toggle('pin1', 'pin2', 1.0, tolerance=0.01)
        start_time = time.time()
        self.addCleanup(self.daq_device.stop_toggle)  # Ensure toggling stops and all the threads are joined even if the test fails
        time.sleep(2.1)  # Wait for a little more than 2 seconds to observe two toggles
        end_time = time.time()

        # Calculate elapsed time
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds (expected ~2 seconds)")

        # Check that the elapsed time is close to the expected time (2 seconds) within tolerance
        self.assertAlmostEqual(elapsed_time, 2.1, delta=0.05)  # Allow 50ms tolerance
        print("Timing mechanism test passed.")

        # Stop toggling
        self.daq_device.stop_toggle()
        self.print_latest_pin_status()

    def test_invalid_operations(self):
        """Test invalid write and read operations."""
        print("Testing invalid operations...")
        # Test invalid write operation on input pin
        print("Testing invalid write operation on input pin (pin1)...")
        with self.assertRaises(ValueError):
            self.daq_device.write_digital('pin1', True)
        print("Invalid write operation test passed.")
        self.print_latest_pin_status()
        
        # Test invalid read operation on output pin, testing for exception cases here.
        """
        try:
            self.daq_device.write_digital('pin1', True)
        except ValueError:
            print("Invalid write operation test passed.")
        else:
            self.fail("ValueError not raised")
        """
        print("Testing invalid read operation on output pin (pin2)...")
        with self.assertRaises(ValueError):
            self.daq_device.read_digital('pin2')
        print("Invalid read operation test passed.")
        self.print_latest_pin_status()

    def test_external_signal_generator_pin1(self):
        """Simulate receiving signals from an external signal generator for pin1."""
        print("Simulating external signal generator for pin1...")

        state_changes_pin1 = []


        
        def mock_external_signal_generator(device, channel, interval=1.0, duration=5.0):
            """Mock function to simulate an external signal generator."""
            start_time = time.time()
            while time.time() - start_time < duration:
                current_value = device.read_digital(channel)
                new_value = not current_value  # Toggle the current value
                device.digital_pins[channel]['value'] = new_value
                state_changes_pin1.append(new_value)  # Capture state changes
                print(f"External signal generator toggled {channel} to {new_value}")
                time.sleep(interval)

        # Read initial state of pin1
        initial_state = self.daq_device.read_digital('pin1')
        print(f"Initial state of Pin1: {initial_state}")
        
        # Mock the external signal generator behavior for pin1
        external_signal_thread = threading.Thread(
            target=mock_external_signal_generator, 
            args=(self.daq_device, 'pin1')
        )
        self.threads.append(external_signal_thread)
        external_signal_thread.start()
        #print(f"Threads list after append: {self.threads}")
        time.sleep(6)  # Wait enough time to observe multiple toggles

        # Verify the final state of the pin
        pin1_final = self.daq_device.read_digital('pin1')
        print(f"Final state of Pin1 after external signal simulation: {pin1_final}")
        external_signal_thread.join()
        print("External signal generator simulation test for pin1 passed.")
        self.print_latest_pin_status()

        # Print state changes for verification
        print(f"State changes for pin1: {state_changes_pin1}")

        # Assertions to verify expected behavior
        # In this case, let's verify that the pin1 state has changed during the test
        self.assertIn(pin1_final, [True, False])  # Ensure pin1 is a valid boolean
        self.assertNotEqual(initial_state, pin1_final, "Pin1 state did not toggle as expected.")
        self.assertGreater(len(state_changes_pin1), 0, "No state changes recorded for pin1.")
        self.assertIn(False, state_changes_pin1, "Pin1 did not toggle to False state.")
        self.assertIn(True, state_changes_pin1, "Pin1 did not toggle to True state.")

    def test_external_signal_generator_pin2(self):
        """Simulate receiving signals from an external signal generator for pin2."""
        print("Simulating external signal generator for pin2...")

        state_changes_pin2 = []
        
        def mock_external_signal_generator(device, channel, interval=1.0, duration=5.0):
            """Mock function to simulate an external signal generator."""
            start_time = time.time()
            while time.time() - start_time < duration:
                current_value = device.digital_pins[channel]['value']
                new_value = not current_value  # Toggle the current value
                device.digital_pins[channel]['value'] = new_value
                state_changes_pin2.append(new_value)  # Capture state changes
                print(f"External signal generator toggled {channel} to {new_value}")
                time.sleep(interval)

        # Read initial state of pin1
        initial_state = self.daq_device.digital_pins['pin2']['value']
        print(f"Initial state of Pin2: {initial_state}")
        
        # Mock the external signal generator behavior for pin2
        external_signal_thread = threading.Thread(
            target=mock_external_signal_generator, 
            args=(self.daq_device, 'pin2')
        )
        self.threads.append(external_signal_thread)
        external_signal_thread.start()
        #print(f"Threads list after append: {self.threads}")
        time.sleep(6)  # Wait enough time to observe multiple toggles

        # Verify the final state of the pin
        pin2_final = self.daq_device.digital_pins['pin2']['value']
        print(f"Final state of Pin2 after external signal simulation: {pin2_final}")
        external_signal_thread.join()
        print("External signal generator simulation test for pin2 passed.")
        self.print_latest_pin_status()

        # Print state changes for verification
        print(f"State changes for pin2: {state_changes_pin2}")

        # Assertions to verify expected behavior
        # In this case, let's verify that the pin2 state has changed during the test
        self.assertIn(pin2_final, [True, False])  # Ensure pin2 is a valid boolean
        self.assertNotEqual(initial_state, pin2_final, "Pin2 state did not toggle as expected.")
        self.assertGreater(len(state_changes_pin2), 0, "No state changes recorded for pin2.")
        self.assertIn(False, state_changes_pin2, "Pin1 did not toggle to False state.")
        self.assertIn(True, state_changes_pin2, "Pin1 did not toggle to True state.")
if __name__ == '__main__':
    unittest.main()
    exit()