# **gps2gpx**

gps2gpx is a Python library that allows you to read serial GPS data and convert it into a .gpx file format. It is designed to be lightweight, efficient, and non-blocking, using multi-threading to capture real-time GPS data without interrupting your program's main flow.

The library is mainly intended for use on Raspberry Pi, but it is also compatible with other platforms such as Linux and Windows. It supports a range of GPS devices and offers customizable data fields.

gps2gpx is open-source, allowing for community contributions and modifications. It is an ideal tool for tracking, mapping, and navigation applications where real-time GPS data is needed.

  

## Installation

You can install gps2gpx using pip:

    pip install gps2gpx

## Usage

    from gps2gpx import Gps2Gpx

  

# Initialize the GPS to GPX converter

    converter = Gps2Gpx(port='/dev/ttyS0',baudrate=9600,folder="./")

  

# Test GPS and device communication

    converter.test_gps_sensor()

  

# Start Capturing GPS data and saver to .gpx file

    converter.start_worker()

  

# Disconnect from the GPS device

    converter.stop_worker()

# Features

Real-time GPS data capture

Customizable data fields

Supports Raspberry Pi, Linux, Windows, and single-board computers

Open-source for community contributions and modifications

# Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

  

# License

gps2gpx is licensed under the MIT License. See LICENSE for more information.