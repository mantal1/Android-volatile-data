# Android Volatile Data Collection

This script collects volatile data from connected Android devices, including logcat and dumpsys logs, zips them, and generates an MD5 hash for the zip file. The collected logs are saved in a specified output directory and zipped for easy transfer and storage.

## Prerequisites

- Python 3.x
- Android Debug Bridge (ADB) installed and added to your system's PATH

## Installation

1. Clone the repository:
    
git clone https://github.com/mantal1/Android-volatile-data.git
cd Android-volatile-data
    
2. Install required Python packages (if any):

pip install -r requirements.txt
    

## Usage

1. Connect your Android device to your computer via USB and ensure USB debugging is enabled.

2. Run the script:
    
python Android_volatile_data.py


3. Follow the prompts to enter the case number and output directory.

4. Select the connected device from the list.

5. The script will capture logcat and dumpsys logs, zip the collected logs, and generate an MD5 hash.

6. The process will complete, and you can exit the script by pressing `Ctrl + C`.

## Script Details

### Functions

- `write_log(log_file, message)`: Logs messages to the console and a specified log file.
- `log_error(log_file, message)`: Logs error messages to a specified log file.
- `run_subprocess(command, output_file, log_file)`: Runs a subprocess command and saves the output to a file.

### Steps

1. Detect connected Android devices.
2. Capture logcat logs.
3. Capture dumpsys logs.
4. Zip collected logs.
5. Generate MD5 hash for the zipped logs.

### Example


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb)
- [Python](https://www.python.org/)
