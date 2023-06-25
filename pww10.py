import subprocess
import os
import re

os.system("cls")

try:
    from tabulate import tabulate
    tabulate_available = True
except ModuleNotFoundError:
    tabulate_available = False
    print("Error: Module 'tabulate' is not installed. Please install it using 'pip3 install tabulate'.")

# Check if tabulate is available
if tabulate_available:
    # Run the 'netsh wlan show profiles' command and retrieve the output
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()

    # Find the Wi-Fi profile names from the output using regular expression
    profile_names = re.findall("All User Profile     : (.*)\r", command_output)

    # Empty list to store Wi-Fi profile information
    wifi_list = []

    # Check if any Wi-Fi profiles are found
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {}  # Create an empty dictionary to store Wi-Fi profile information
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()

            # Check if the Wi-Fi profile has a security key or not
            if re.search("Security key           : Absent", profile_info):
                continue  # Continue to the next Wi-Fi profile if it doesn't have a security key
            else:
                # Store the SSID name of the Wi-Fi profile in the wifi_profile dictionary
                wifi_profile["ssid"] = name

                # Get the complete information of the Wi-Fi profile, including the password
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()

                # Search for the password using regular expression
                password = re.search("Key Content            : (.*)\r", profile_info_pass)

                # Store the password in the wifi_profile dictionary, or None if no password is found
                if password is None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]

                # Append the wifi_profile dictionary to the wifi_list
                wifi_list.append(wifi_profile)

    # Format the retrieved Wi-Fi profile information into a table
    table_headers = ["SSID", "Password"]
    table_data = []
    for wifi_profile in wifi_list:
        ssid = wifi_profile["ssid"]
        password = wifi_profile["password"]
        table_data.append([ssid, password])

    # Print the table
    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))