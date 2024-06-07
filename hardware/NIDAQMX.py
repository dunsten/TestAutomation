import time
import nidaqmx
from nidaqmx.constants import LineGrouping
import keyboard

def read_digital_input(pin_name):
    try:
        # Create a task to read digital input
        with nidaqmx.Task() as task:
            # Add the digital input channel
            task.di_channels.add_di_chan(pin_name, line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
            
            # Infinite loop for continuous reading
            while True:
                # Record the start time of the read operation
                read_start_time = time.time()
                # Read the digital input
                data = task.read()
                # Record the end time of the read operation
                read_end_time = time.time()

                # Calculate the actual read duration
                read_duration = read_end_time - read_start_time
                # Calculate the expected read duration (time.sleep(0.1))
                expected_duration = 0.1
                # Calculate the tolerance threshold
                tolerance = 0.01  # 10 milliseconds tolerance

                # Print the acquired data and the actual read duration
                print(f"Acquired data: {data}, Read Duration: {read_duration:.4f}s")

                # Check if the actual read duration is within the tolerance range of the expected duration
                if abs(read_duration - expected_duration) > tolerance:
                    print("Warning: Read duration deviates from expected duration!")

                # Wait for a short duration before reading again
                time.sleep(0.1)

                # Check for key press to exit the loop
                if keyboard.is_pressed('q'):
                    break
    except nidaqmx.errors.DaqError as e:
        print(f"DAQmx Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def write_digital_output(pin_name, value):
    try:
        # Create a task to write digital output
        with nidaqmx.Task() as task:
            # Add the digital output channel
            task.do_channels.add_do_chan(pin_name, line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
            # Start the task
            task.start()
            # Write the digital value
            task.write(value)
    except nidaqmx.errors.DaqError as e:
        print(f"DAQmx Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Specify the digital input pin name
    pin_name = "Dev1/port0"  # Change this to the appropriate pin name
    # Specify the duration for reading (in seconds)
    duration = 10

    # Call the function to read the digital input pin
    read_digital_input(pin_name)

    # Specify the digital output pin name for failure pin
    failure_pin_name = "Dev1/port1"  # Change this to the appropriate failure pin name
    # Specify the value to be written (True or False)
    failure_pin_value = True

    # Call the function to write to the digital output pin
    write_digital_output(failure_pin_name, failure_pin_value)
