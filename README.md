# BadUSB Project

## Overview

This is my BadUSB project. This repository showcases a BadUSB attack using Arduino and Python scripts. By simulating a keyboard, the Arduino executes commands to download and run a file on the target system. Please use this project responsibly and for educational purposes only. There are three main files:

1. **Arduino File**
   - File with .ino extension
   - Description: Arduino code that simulates a keyboard to open a command prompt, download and execute a file on the target system.

2. **Python File**
   - File with .py extension
   - Description: Python script that collects PC specifications and browser history. It creates a text file and an Excel files with the gathered information and sends them via email.

3. **Executable File**
   - File with .exe extension
   - Description: Executable file generated from python file. This file can be run on a Windows system to automatically collect and send PC information.

## Usage

### Arduino File
1. Upload the ino file to an Arduino board.
2. Connect the Arduino to the target system.
3. The Arduino will simulate a keyboard and execute predefined commands.

### Python File
1. Open the python script in a text editor.
2. Locate the following lines in the script:

   &num; Data for sending an email \
   sender_email = "your_email@gmail.com" \
   sender_password = "your gmail app password" \
   recipient_email = "recipient_email@example.com" \
   
4. Change the sender_email and recipient_email to your desired email addresses.
5. Save the changes.
