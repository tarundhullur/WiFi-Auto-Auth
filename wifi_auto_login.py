import os
import requests
from xml.etree import ElementTree as ET

# Login URL
login_url = "http://192.168.100.1:8090/login.xml"

# Get credentials securely from environment variables
username = os.getenv("WIFI_USERNAME")
password = os.getenv("WIFI_PASSWORD")

# Ensure credentials are provided
if not username or not password:
    print("Error: Username or Password not found in environment variables.")
    exit()

# Login payload
payload = {
    "username": username,
    "password": password,
    "mode": "191",  # Optional: Adjust if your portal requires it
}

try:
    # Send the POST request to log in
    response = requests.post(login_url, data=payload)

    # Parse the XML response
    if response.status_code == 200:
        xml_response = ET.fromstring(response.text)

        # Extract key details from the XML response
        status = xml_response.find("status").text if xml_response.find("status") is not None else "UNKNOWN"
        message = xml_response.find("message").text if xml_response.find("message") is not None else ""
        
        if "LIVE" in status:
            print(f"Already signed in. Message: {message}")
        elif "logged in" in message.lower():
            print("Login successful!")
        else:
            print(f"Login failed. Message: {message}")
    else:
        print(f"Error: Received status code {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")
