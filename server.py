import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import datetime
import re

# Configure your serial port and baud rate here
serial_port = 'COM5'  # Update with your port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux)
baud_rate = 115200
output_file = "serial_data.csv"
threshold = 1000  # Customizable threshold for total count

# Initialize serial connection
ser = serial.Serial(serial_port, baud_rate)

# Initialize data storage
entry_count = 0
exit_count = 0
total_count = 0
time_stamps = []

# Set up CSV file for data storage
with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Timestamp', 'Type', 'Count'])  # Write header row

# Set up matplotlib figure and axis
fig, ax = plt.subplots()
bars = ax.bar(['Entry', 'Exit'], [entry_count, exit_count], color=['green', 'red'])

# Set integer tick marks for y-axis
ax.yaxis.get_major_locator().set_params(integer=True)
total_count_annotation = ax.text(0.5, max(entry_count, exit_count), '', 
                                 ha='center', va='bottom', fontsize=12, color='blue')

# Function to parse the time from the serial message
def parse_time_from_message(message):
    match = re.search(r"(\d+) hr : (\d+) min : (\d+) sec", message)
    if match:
        hours, minutes, seconds = map(int, match.groups())
        return datetime.datetime.now().replace(hour=hours, minute=minutes, second=seconds)
    return None

# Function to print current counts
def print_counts():
    print(f"\nSummary:")
    print(f"  Total Entries: {entry_count}")
    print(f"  Total Exits: {exit_count}")
    print(f"  Current Count: {total_count}")

# Function to update bar graph
def update(frame):
    global entry_count, exit_count, total_count

    if ser.in_waiting > 0:
        # Read a line from the serial port with error handling for decoding
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        timestamp = None
        label = None

        # Check for entry or exit in the message
        if "Entry detected at" in line:
            entry_count += 1
            total_count += 1
            timestamp = parse_time_from_message(line)
            time_stamps.append((timestamp, "Entry", entry_count))
            bars[0].set_height(entry_count)  # Update entry bar height
            label = 'Entry'
        
        elif "Exit detected at" in line:
            exit_count += 1
            total_count -= 1
            timestamp = parse_time_from_message(line)
            time_stamps.append((timestamp, "Exit", exit_count))
            bars[1].set_height(exit_count)  # Update exit bar height
            label = 'Exit'

        # Update total count annotation
        total_count_annotation.set_text(f"Total Count: {total_count}")
        total_count_annotation.set_position((0.5, max(entry_count, exit_count) + 1))

        # Save data to CSV
        if timestamp:
            with open(output_file, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([timestamp.strftime("%Y-%m-%d %H:%M:%S"), label, entry_count if label == 'Entry' else exit_count])

        # Console output
        if timestamp:
            print(f"{label} at {timestamp.strftime('%H:%M:%S')}")
        else:
            print(f"{label} detected, but timestamp unavailable.")
        
        # Print summary counts
        print_counts()

        # Check for threshold warning
        if total_count > threshold:
            print("WARNING: Total count has exceeded the threshold!")

    return bars

# Set up real-time animation with cache_frame_data=False
ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)

# Display the bar graph with labels and title
plt.xlabel("Event Type")
plt.ylabel("Count")
plt.title("Real-Time Entry and Exit Count")
plt.show()

# Close the serial connection when done
ser.close()
