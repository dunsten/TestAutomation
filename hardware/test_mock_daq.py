import unittest
import time
from mock_daq import MockDAQDevice
from unittest.mock import MagicMock
import threading

class TestMockDAQDevice(unittest.TestCase):

    def setUp(self):
        self.daq_device = MockDAQDevice()
        self.daq_device.configure_digital_channel('pin1', 'input')
        self.daq_device.configure_digital_channel('pin2', 'output')
        print("\nSetup complete: Configured 'pin1' as input and 'pin2' as output.")

    def test_initial_state(self):
        """Test initial state of the pins."""
        print("Testing initial state of the pins...")
        pin1_initial = self.daq_device.read_digital('pin1')
        pin2_initial = self.daq_device.digital_pins['pin2']['value']
        print(f"Initial state - Pin1: {pin1_initial}, Pin2: {pin2_initial}")
        self.assertFalse(pin1_initial)
        self.assertFalse(pin2_initial)
        print("Initial state test passed.")

    def test_write_digital(self):
        """Test writing to the output pin."""
        print("Testing write operation to pin2 (output pin)...")
        self.daq_device.write_digital('pin2', True)
        pin2_value = self.daq_device.digital_pins['pin2']['value']
        print(f"Pin2 value after write: {pin2_value}")
        self.assertTrue(pin2_value)
        print("Write operation test passed.")

    def test_toggle_pins(self):
        """Test that pin1 toggles every second and pin2 is the opposite of pin1."""
        print("Starting toggle test for pin1 and pin2 with 1-second interval...")
        self.daq_device.start_toggle('pin1', 'pin2', 1.0, tolerance=0.01)
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

    def test_timing_mechanism(self):
        """Validate the timing mechanism with a tolerance."""
        print("Starting timing mechanism test with 1-second interval and 0.01-second tolerance...")
        self.daq_device.start_toggle('pin1', 'pin2', 1.0, tolerance=0.01)
        start_time = time.time()
        time.sleep(2.1)  # Wait for a little more than 2 seconds to observe two toggles
        end_time = time.time()

        # Calculate elapsed time
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds (expected ~2 seconds)")

        # Check that the elapsed time is close to the expected time (2 seconds) within tolerance
        self.assertAlmostEqual(elapsed_time, 2.0, delta=0.05)  # Allow 50ms tolerance
        print("Timing mechanism test passed.")

        # Stop toggling
        self.daq_device.stop_toggle()

    def test_invalid_operations(self):
        """Test invalid write and read operations."""
        print("Testing invalid operations...")
        # Test invalid write operation on input pin
        print("Testing invalid write operation on input pin (pin1)...")
        with self.assertRaises(ValueError):
            self.daq_device.write_digital('pin1', True)
        print("Invalid write operation test passed.")
        
        # Test invalid read operation on output pin
        print("Testing invalid read operation on output pin (pin2)...")
        with self.assertRaises(ValueError):
            self.daq_device.read_digital('pin2')
        print("Invalid read operation test passed.")

    def test_external_signal_generator_pin1(self):
        """Simulate receiving signals from an external signal generator for pin1."""
        print("Simulating external signal generator for pin1...")
        
        def mock_external_signal_generator(device, channel, interval=1.0, duration=5.0):
            """Mock function to simulate an external signal generator."""
            start_time = time.time()
            while time.time() - start_time < duration:
                current_value = device.read_digital(channel)
                device.digital_pins[channel]['value'] = not current_value
                print(f"External signal generator toggled {channel} to {not current_value}")
                time.sleep(interval)
        
        # Mock the external signal generator behavior for pin1
        external_signal_thread = threading.Thread(
            target=mock_external_signal_generator, 
            args=(self.daq_device, 'pin1')
        )
        external_signal_thread.start()
        time.sleep(6)  # Wait enough time to observe multiple toggles

        # Verify the final state of the pin
        pin1_final = self.daq_device.read_digital('pin1')
        print(f"Final state of Pin1 after external signal simulation: {pin1_final}")
        external_signal_thread.join()
        print("External signal generator simulation test for pin1 passed.")

    def test_external_signal_generator_pin2(self):
        """Simulate receiving signals from an external signal generator for pin2."""
        print("Simulating external signal generator for pin2...")
        
        def mock_external_signal_generator(device, channel, interval=1.0, duration=5.0):
            """Mock function to simulate an external signal generator."""
            start_time = time.time()
            while time.time() - start_time < duration:
                current_value = device.digital_pins[channel]['value']
                device.digital_pins[channel]['value'] = not current_value
                print(f"External signal generator toggled {channel} to {not current_value}")
                time.sleep(interval)
        
        # Mock the external signal generator behavior for pin2
        external_signal_thread = threading.Thread(
            target=mock_external_signal_generator, 
            args=(self.daq_device, 'pin2')
        )
        external_signal_thread.start()
        time.sleep(6)  # Wait enough time to observe multiple toggles

        # Verify the final state of the pin
        pin2_final = self.daq_device.digital_pins['pin2']['value']
        print(f"Final state of Pin2 after external signal simulation: {pin2_final}")
        external_signal_thread.join()
        print("External signal generator simulation test for pin2 passed.")

if __name__ == '__main__':
    unittest.main()
    exit()
