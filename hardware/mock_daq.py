import time
import threading
from collections import defaultdict

class MockDAQDevice:
    def __init__(self):
        # Dictionary to store the state of each channel
        self.digital_pins = defaultdict(lambda: {'direction': None, 'value': False})
        self._stop_toggle = threading.Event()
        self._toggle_thread = None

    def configure_digital_channel(self, channel, direction):
        """
        Configure a digital channel as either 'input' or 'output'.
        Args:
            channel (str): The name of the channel.
            direction (str): The direction of the channel ('input' or 'output').
        """
        if direction not in ['input', 'output']:
            raise ValueError("Direction must be either 'input' or 'output'")
        self.digital_pins[channel]['direction'] = direction

    def write_digital(self, channel, value):
        """
        Write a digital value to an output channel.
        Args:
            channel (str): The name of the channel.
            value (bool): The value to write (True or False).
        """
        if self.digital_pins[channel]['direction'] == 'output':
            self.digital_pins[channel]['value'] = value
        else:
            raise ValueError("Cannot write to an input channel")

    def read_digital(self, channel):
        """
        Read the digital value from an input channel.
        Args:
            channel (str): The name of the channel.
        Returns:
            bool: The current value of the channel, or None if not an input.
        """
        if self.digital_pins[channel]['direction'] == 'input':
            return self.digital_pins[channel]['value']
        else:
            raise ValueError("Cannot read from an output channel")

    def start_toggle(self, input_channel, output_channel, interval=1.0, tolerance=0.01):
        """
        Start toggling a digital input channel at a specified interval.
        Args:
            input_channel (str): The name of the input channel.
            output_channel (str): The name of the output channel.
            interval (float): The interval between toggles in seconds.
            tolerance (float): The allowed tolerance in seconds.
        """
        if self.digital_pins[input_channel]['direction'] != 'input':
            raise ValueError("Cannot toggle a non-input channel")
        if self.digital_pins[output_channel]['direction'] != 'output':
            raise ValueError("Cannot toggle a non-output channel")
        self._stop_toggle.clear()
        self._toggle_thread = threading.Thread(target=self._toggle_pin, args=(input_channel, output_channel, interval, tolerance))
        self._toggle_thread.start()

    def stop_toggle(self):
        """
        Stop toggling the digital input channel.
        """
        if self._toggle_thread:
            self._stop_toggle.set()
            self._toggle_thread.join()

    def _toggle_pin(self, input_channel, output_channel, interval, tolerance):
        """
        Internal method to toggle the digital input channel.
        Args:
            input_channel (str): The name of the input channel.
            output_channel (str): The name of the output channel.
            interval (float): The interval between toggles in seconds.
            tolerance (float): The allowed tolerance in seconds.
        """
        next_toggle_time = time.time() + interval
        while not self._stop_toggle.is_set():
            current_time = time.time()
            if abs(current_time - next_toggle_time) <= tolerance:
                current_value = self.digital_pins[input_channel]['value']
                new_value = not current_value
                self.digital_pins[input_channel]['value'] = new_value
                self.digital_pins[output_channel]['value'] = not new_value
                next_toggle_time += interval
            time.sleep(tolerance)  # Check in small intervals for more accurate toggling

    def set_failure_pin(self, pin, value):
        """
        Set the failure indicator pin.
        Args:
            pin (str): The name of the pin.
            value (bool): The value to set (True or False).
        """
        self.write_digital(pin, value)