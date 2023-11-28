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
   recipient_email = "recipient_email@example.com"
4. Change the sender_email and recipient_email to your desired email addresses.
5. Save the changes.

### Setting up Gmail App Password
1. Go to your Google Account settings.
2. Navigate to "Security" and find the "App Passwords" section.
3. Generate an App Password for the application (choose "Mail" as the app).
4. Replace the email_password variable in pc_info.py with the generated App Password.

### Setting up Executable File (Using auto-py-to-exe)
1. Install auto-py-to-exe using the following command: \
pip install auto-py-to-exe
2. Open auto-py-to-exe.
3. Load the python script.
4. Configure the desired settings, including the output directory and file name.
5. Click on "Convert .py to .exe."
6. The tool will generate an executable file in the specified output directory.

