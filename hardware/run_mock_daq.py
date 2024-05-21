import time
import matplotlib.pyplot as plt
from mock_daq import MockDAQDevice

def main():
    # Initialize the mock DAQ device
    daq_device = MockDAQDevice()
    
    # Configure channels
    daq_device.configure_digital_channel('pin1', 'input')
    daq_device.configure_digital_channel('pin2', 'output')
    
    # Write to an output channel
    daq_device.write_digital('pin2', True)
    print("pin2 set to True")

    # Start toggling the input pin and the output pin
    daq_device.start_toggle('pin1', 'pin2', 1.0, tolerance=0.01)

    # Set up the plot
    plt.ion()
    fig, ax = plt.subplots()
    times = []
    pin1_values = []
    pin2_values = []

    start_time = time.time()
    while time.time() - start_time < 10:
        current_time = time.time() - start_time
        pin1_value = daq_device.read_digital('pin1')
        pin2_value = daq_device.digital_pins['pin2']['value']
        times.append(current_time)
        pin1_values.append(pin1_value)
        pin2_values.append(pin2_value)

        ax.clear()
        ax.plot(times, pin1_values, label='pin1')
        ax.plot(times, pin2_values, label='pin2', linestyle='--')
        ax.set_ylim(-0.1, 1.1)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Value')
        ax.legend()
        plt.draw()
        plt.pause(0.01)  # Pause to update the plot

    #Stop toggling the pin
    daq_device.stop_toggle()

    # Show the final plot
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()
