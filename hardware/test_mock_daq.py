import unittest
import time
from mock_daq import MockDAQDevice

class TestMockDAQDevice(unittest.TestCase):

    def setUp(self):
        self.daq_device = MockDAQDevice()
        self.daq_device.configure_digital_channel('pin1', 'input')
        self.daq_device.configure_digital_channel('pin2', 'output')

    def test_initial_state(self):
        # Test initial state of the pins
        self.assertFalse(self.daq_device.read_digital('pin1'))
        self.assertFalse(self.daq_device.digital_pins['pin2']['value'])

    def test_write_digital(self):
        # Test writing to the output pin
        self.daq_device.write_digital('pin2', True)
        self.assertTrue(self.daq_device.digital_pins['pin2']['value'])

    def test_toggle_pins(self):
        # Start toggling pin1 and pin2
        self.daq_device.start_toggle('pin1', 'pin2', 1.0, tolerance=0.01)
        time.sleep(2.1)  # Wait for a little more than 2 seconds to observe two toggles

        # Check the state after the first toggle
        pin1_value_first = self.daq_device.read_digital('pin1')
        pin2_value_first = self.daq_device.digital_pins['pin2']['value']
        self.assertNotEqual(pin1_value_first, pin2_value_first)

        time.sleep(1.1)  # Wait for a little more than 1 second to observe another toggle

        # Check the state after the second toggle
        pin1_value_second = self.daq_device.read_digital('pin1')
        pin2_value_second = self.daq_device.digital_pins['pin2']['value']
        self.assertNotEqual(pin1_value_second, pin2_value_second)

        # Verify that pin1 has toggled
        self.assertNotEqual(pin1_value_first, pin1_value_second)
        # Verify that pin2 has also toggled to be the opposite of pin1
        self.assertEqual(pin1_value_second, not pin2_value_second)

        # Stop toggling
        self.daq_device.stop_toggle()

    def test_invalid_operations(self):
        # Test invalid write operation on input pin
        with self.assertRaises(ValueError):
            self.daq_device.write_digital('pin1', True)
        
        # Test invalid read operation on output pin
        with self.assertRaises(ValueError):
            self.daq_device.read_digital('pin2')

if __name__ == '__main__':
    unittest.main()
