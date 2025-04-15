![screenshots](https://github.com/LegitCoconut/TEED-TS/blob/main/screenshot/teeds.png)
# 🚪 Touchless Entry-Exit Data Tracking System (TEED-TS)

## 📖 Overview
The **Touchless Entry-Exit Data Tracking System (TEED-TS)** is a hygienic, non-contact solution designed to monitor entry and exit movements. It uses **Infrared (IR) sensors**, the **ESP8266 microcontroller**, and **IoT technologies** to provide real-time data tracking while reducing physical contact.

Collected data is visualized through dynamic graphs and stored in CSV format, making it suitable for environments requiring reliable monitoring, such as:
- 🏥 Hospitals  
- 🏢 Offices  
- 🛒 Retail Spaces  
- 🛡️ Security Zones  

---

## ✨ Features
- **Touchless Monitoring**: Tracks entry/exit movements using IR sensors.
- **Real-Time Visualization**: Displays real-time entry/exit counts via animated bar graphs.
- **Data Logging**: Saves timestamped data in CSV format for analysis.
- **Hygienic and Efficient**: Reduces human contact and contamination risk.
- **Scalable**: Can integrate with larger networks or more complex setups.

---

## 🛠️ Components

### 🔩 Hardware
| Component      | Quantity | Description                              |
|----------------|----------|------------------------------------------|
| **IR Sensors** | 4        | Detect interruptions in infrared beams.  |
| **ESP8266**    | 1        | Microcontroller for data processing.     |
| **Breadboard** | 1        | For prototyping the circuit.             |
| **Jumper Wires** | Set     | Connect components to the circuit.       |

### 💻 Software
1. **Arduino IDE**: For programming the ESP8266 microcontroller.
2. **Python**: For data processing and visualization.
   - Libraries used:
     - `csv`: Handles data logging.
     - `time` & `datetime`: For timestamps.
     - `matplotlib`: For creating animated bar graphs.
     - `serial`: For serial communication with the ESP8266.

---

## 🚀 How It Works

1. **Initialization**:  
   - The ESP8266 connects to Wi-Fi to sync the current time from an NTP server.

2. **Detection**:  
   - IR sensors monitor movements by detecting interruptions in their beams.

3. **Data Processing**:  
   - The ESP8266 categorizes events as **entry** or **exit** and sends the data to a laptop.
   - Timestamped data is logged in a CSV file.

4. **Visualization**:  
   - Real-time bar graphs show ongoing entry/exit counts.
   - Interval-based graphs provide insights every 5 minutes.

---

## 📊 Results

| **Metric**               | **Performance**                  |
|---------------------------|-----------------------------------|
| **Accuracy**              | ~95% in controlled environments. |
| **Sensor Response Time**  | 0.5 seconds (average).           |
| **Uptime**                | 100% (during testing).           |
| **Test Period Data**      | 98 entries, 96 exits (24 hours). |

---

## 🔧 Setup Instructions

### Hardware
1. Connect IR sensors to the ESP8266 microcontroller.
2. Use jumper wires and a breadboard for prototyping.
3. Power the ESP8266 and ensure proper wiring.

### Software
1. Install **Arduino IDE** and upload the provided client-side code to the ESP8266.
2. Install Python (3.x) and required libraries using:  
   ```bash
   pip install matplotlib pyserial
    ```
A practical, precise, and scalable solution for monitoring movements in real-time. This system prioritizes hygiene, efficiency, and data visualization, making it suitable for a variety of environments, including healthcare, retail, and public spaces.

## 🛠️ Future Improvements

- **Replace wired communication with Wi-Fi-based communication**: Enhance connectivity and reduce dependency on physical wiring.
- **Integrate AI analytics**: Analyze movement trends and predict patterns for smarter decision-making.
- **Improve sensor calibration**: Mitigate interference caused by environmental factors to enhance accuracy.

## 🏆 Key Benefits

- **Hygienic**: Reduces contact in sensitive environments.
- **Real-Time Insights**: Provides live tracking for better monitoring.
- **Scalable**: Adaptable to various use cases, including large-scale deployments.

## 🖼️ Visualization Example

*Include your data visualization example here (e.g., graphs, charts, or images demonstrating real-time tracking).*

## 📚 References

- [Arduino People Counter](#)
- [Assessing the ESP8266 Wi-Fi Module](#)
- [A Smart Bidirectional Visitor Counter](#)

## 💡 Conclusion

The **Touchless Entry-Exit Data Tracking System (TEED-TS)** is designed for environments where hygiene, precision, and efficiency are paramount. Its features and future enhancements ensure adaptability for applications in various sectors, including:

- Healthcare
- Retail
- Public spaces

---

### 🚀 How to Run the Python Script

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Python script to process and visualize data:
   ```bash
   python script_name.py
   ```

---

### 🔧 System Requirements
- Python 3.7+
- Arduino IDE (for microcontroller programming)
- ESP8266 Wi-Fi Module or equivalent
- Sensor hardware

---

Feel free to contribute by submitting pull requests or issues!

## Screenshots

![screenshots](https://github.com/LegitCoconut/TEED-TS/blob/main/screenshot/block_diagran.jpg).

![screenshots](https://github.com/LegitCoconut/TEED-TS/blob/main/screenshot/out_csv.jpg)

![screenshots](https://github.com/LegitCoconut/TEED-TS/blob/main/screenshot/out_graph.jpg)

![screenshots](https://github.com/LegitCoconut/TEED-TS/blob/main/screenshot/project.jpg)


## Support

For support, email err@titansec.team .

