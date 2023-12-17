import requests
import json


test_data_path ="/Users/rileydrake/Desktop/geoLeads/management/test_data.json"

# Endpoint URL
url = 'http://localhost:5001/search'  # Replace with your actual Flask URL

# Read the JSON file
with open(test_data_path, 'r') as file:
    data = json.load(file)

# Send POST request
response = requests.post(url, json=data)

# Print response
print("Status Code:", response.status_code)
print("Response Body:", response.json())