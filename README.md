# Touchless Entry-Exit Data Tracking System (TEED-TS)

## Overview
The **Touchless Entry-Exit Data Tracking System (TEED-TS)** is a hygienic, non-contact solution designed to monitor entry and exit movements. It uses **Infrared (IR) sensors**, the **ESP8266 microcontroller**, and **IoT technologies** to ensure accurate, real-time tracking while reducing physical contact. 

Collected data is visualized through real-time graphs and stored in CSV format for further analysis. The system is ideal for environments requiring reliable monitoring, such as hospitals, offices, and public spaces.

---

## Features
- **Touchless Monitoring**: Tracks entry and exit movements using IR sensors.
- **Real-Time Data Visualization**: Displays real-time entry/exit counts via dynamic bar graphs.
- **Data Logging**: Stores movement data with timestamps in CSV format for analysis.
- **Hygienic and Efficient**: Ensures safety and reduces the risk of contamination.
- **Scalable and Adaptable**: Can integrate with larger networks or more complex setups.

---

## Components

### Hardware
1. **IR Sensors** (4 units): Detect interruptions in the infrared beam.
2. **ESP8266 Microcontroller**: Processes sensor data and communicates with a laptop.
3. **Breadboard**: Used for prototyping the circuit.
4. **Jumper Wires**: For connecting the components.

### Software
1. **Arduino IDE**: Used to program the ESP8266 microcontroller.
2. **Python**: For data processing and visualization.
   - Libraries used:
     - `csv`: Read/write CSV files.
     - `time` & `datetime`: For tracking and formatting timestamps.
     - `matplotlib`: For creating and animating bar graphs.
     - `serial`: For serial communication with the ESP8266.

---

## Setup Instructions

### Hardware
1. Connect the IR sensors to the ESP8266 microcontroller as per the circuit diagram.
2. Use jumper wires and a breadboard for easy prototyping.
3. Power the ESP8266 and establish its connection with the sensors.

### Software
1. Install the Arduino IDE and upload the client-side code to the ESP8266 microcontroller.
2. Install Python (3.x) on your system and set up the required libraries (`pip install matplotlib pyserial`).
3. Use the provided Python script to handle data processing, storage, and visualization.

---

## How It Works

1. **Initialization**: 
   - The ESP8266 connects to a Wi-Fi network to sync the current time from an NTP server.
2. **Detection**: 
   - IR sensors monitor movement by detecting interruptions in their infrared beam.
3. **Data Processing**:
   - The ESP8266 identifies events (entry or exit) and transmits data to a laptop.
   - Data is logged with timestamps in a CSV file.
4. **Visualization**:
   - Real-time bar graphs display entry/exit counts.
   - Five-minute interval graphs provide additional insights.

---

## Results

- **Accuracy**: ~95% in controlled environments.
- **Response Time**: 0.5 seconds average sensor response.
- **Reliability**: 100% uptime during testing with no communication interruptions.
- **Data Collected**: Successfully tracked 98 entries and 96 exits over 24 hours.

---

## Future Improvements

1. **Wi-Fi-Based Communication**: Replace the wired setup with a completely wireless system.
2. **AI Integration**: Use AI to analyze traffic patterns and perform statistical analysis.
3. **Enhanced Calibration**: Address environmental interference for greater accuracy.

---

## Conclusion

The **Touchless Entry-Exit Data Tracking System (TEED-TS)** is an efficient, scalable, and hygienic solution for monitoring movement. Its real-time tracking, reliable data storage, and visualization capabilities make it suitable for diverse environments like healthcare, retail, and security.

---

## References

- [Arduino People Counter](https://www.instructables.com/Arduino-People-CounterMachine-DIY)
- [Assessing the ESP8266 Wi-Fi Module](https://ieeexplore.ieee.org/abstract/document/8502562)
- [A Smart Bidirectional Visitor Counter](https://dl.acm.org/doi/abs/10.1145/3647444.3647925)
