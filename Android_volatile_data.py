import os
import subprocess
import hashlib
import shutil
import time
import zipfile
import signal
import sys

# Function to log messages and save to file
def write_log(log_file, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - {message}"
    print(log_message)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

# Function to log errors to file only
def log_error(log_file, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - {message}"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

# Function to run subprocess and save output to a file
def run_subprocess(command, output_file, log_file):
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    if result.stdout:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)
    else:
        log_error(log_file, "No output from subprocess command.")
    if result.stderr:
        log_error(log_file, result.stderr)
    return result

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    write_log(log_file, "Process interrupted. Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Get case number and output directory
case_number = input("Enter Case Number: ")
output_path = input("Enter Output Directory (e.g., C:\\Forensics\\Logs): ").strip().strip("'\"")

# Ensure output directory exists
os.makedirs(output_path, exist_ok=True)
log_file = os.path.join(output_path, f"log_case_{case_number}.log")
write_log(log_file, "Logging started")

# Step 1: Detect connected devices
write_log(log_file, "Checking for connected Android devices...")
adb_devices = run_subprocess(["adb", "devices"], log_file, log_file)
output_lines = adb_devices.stdout.strip().split("\n") if adb_devices.stdout else []
devices = [line.split("\t")[0] for line in output_lines[1:] if "device" in line]

if not devices:
    log_error(log_file, "No Android devices detected!")
    exit(1)

# Show available devices and prompt selection
write_log(log_file, "Connected Devices:")
for index, device in enumerate(devices, start=1):
    write_log(log_file, f"{index}) {device}")

device_index = int(input("Enter the number corresponding to the device: ")) - 1
if device_index < 0 or device_index >= len(devices):
    log_error(log_file, "Invalid selection. Exiting.")
    exit(1)

selected_device = devices[device_index]
write_log(log_file, f"Selected Device: {selected_device}")

# Step 2: Capture logcat logs
logcat_file = os.path.join(output_path, f"logcat_case_{case_number}_device_{selected_device}.txt")
write_log(log_file, "Capturing logcat logs...")
run_subprocess(["adb", "-s", selected_device, "logcat", "-b", "all", "-v", "UTC,usec", "-d"], logcat_file, log_file)
write_log(log_file, f"Logcat logs saved: {logcat_file}")

# Step 3: Capture dumpsys logs
dumpsys_file = os.path.join(output_path, f"dumpsys_case_{case_number}_device_{selected_device}.txt")
write_log(log_file, "Capturing dumpsys logs...")
run_subprocess(["adb", "-s", selected_device, "shell", "dumpsys"], dumpsys_file, log_file)
write_log(log_file, f"Dumpsys logs saved: {dumpsys_file}")

# Step 4: Zip collected logs
zip_file = os.path.join(output_path, f"Android_Logs_Case_{case_number}_Device_{selected_device}.zip")
write_log(log_file, "Zipping collected logs...")
with zipfile.ZipFile(zip_file, 'w') as zipf:
    zipf.write(logcat_file, os.path.basename(logcat_file))
    zipf.write(dumpsys_file, os.path.basename(dumpsys_file))
write_log(log_file, f"Logs zipped: {zip_file}")

# Step 5: Generate MD5 hash
md5_file = os.path.join(output_path, f"Android_Logs_Case_{case_number}.md5")
write_log(log_file, "Generating MD5 hash...")
hash_md5 = hashlib.md5()
with open(zip_file, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
md5_hash = hash_md5.hexdigest()
with open(md5_file, "w", encoding="utf-8") as f:
    f.write(md5_hash)
write_log(log_file, f"MD5 Hash saved: {md5_file}")

write_log(log_file, "Process completed successfully!")
write_log(log_file, "Hit Ctrl + C to exit.")

while True:
    time.sleep(5)
