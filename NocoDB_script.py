import os, json
import requests
from dotenv import *

# Load the enviroment variable
load_dotenv()

# This small part of code read all the json files in the directory specified
path_to_json = './json/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
data = []

# Try to read all the JSON obj in all the JSON files 
try:
    for f in json_files:
        with open (path_to_json + f, 'r', encoding = "utf-8") as file:
            read = json.load(file)
            data.append(read)

except FileNotFoundError:
    print ("Error: The file was not found")

header = json.loads(os.getenv("headers"))

#---------------------------------------------------------------------------------------------

# Upload the JSON obj in the areas table
# Building the POST variables
areas = data [0]

# Insert the values inside the table
api_url_area = f"{os.getenv('url_areas')}"
upload_response = requests.post(api_url_area, headers = header, json = areas)

# Return value
if upload_response.status_code != 200:
    print ("Upload failed:", upload_response.text)
else:
    print ("Upload completed")

#-------------------------------------------------------------------------------------

# Upload the JSON obj to the departments table
# Build the POST variables
departments = data [1]

# Insert the values inside the table
api_url_departments = f"{os.getenv('url_departments')}"
upload_response = requests.post(api_url_departments, headers = header,  json = departments)

# Return value
if upload_response.status_code != 200:
    print ("Upload failed:", upload_response.text)
else:
    print ("Upload completed")

#------------------------------------------------------------------------------------------------------------------------

# Upload the JSON obj to the users table
# Building the POST variables
users = data [2]

# Change exit date from "" to null
for u in users:
    if u["Exit Date"] == "":
        u["Exit Date"] = None

# Insert the values inside the table
api_url_users = f"{os.getenv('url_users')}"
upload_response = requests.post(api_url_users, headers = header, json = users)

# Return value
if upload_response.status_code != 200:
    print ("Upload failed:", upload_response.text)
else:
    print ("Upload completed")

#--------------------------------------------------------------------------------------------------------------

# Linking the table departments to the table users
# Get the department ID
get_response = requests.get(api_url_departments, headers=header)

if get_response.status_code != 200:
    print ("Get request failed:", get_response.text)
else:
    print ("Get request completed")

departments = get_response.json()["list"]

# Get the user ID
get_response = requests.get(api_url_users, headers=header)

if get_response.status_code != 200:
    print ("Get request failed:", get_response.text)
else:
    print ("Get request completed")

users = get_response.json()["list"]

# Make a control to extract the IDs for the link
user_ID = []
department_ID = []

for u in users:
    for d in departments:
        if (u["Department"] == d["Name"]):
            user_ID.append(u["Id"])
            department_ID.append(d["Id"])

# Uploading the link between users and departments
i = 0 
for ID in user_ID:
    # Url for the user link records
    url_string = os.getenv("BASE_URL") + os.getenv("LINK_URL_DEPARTMENT") + str(ID)
    url_users = f"{url_string}"       
    payload = {"Id": department_ID[i]}
    upload_response = requests.post(url_users, headers=header, json=payload)     
    i += 1
    if upload_response.status_code != 201:
        print ("Upload failed:", upload_response.text)
        exit
    else:
        print ("Upload for user: ", ID, " completed")

#--------------------------------------------------------------------------------------------------

# Linking the table departments to the table users
# Get the areas ID
get_response = requests.get(api_url_area, headers=header)

if get_response.status_code != 200:
    print ("Get request failed:", get_response.text)
else:
    print ("Get request completed")

areas = get_response.json()["list"]

user_ID.clear()
areas_ID = []

# Make a control to extract the IDs for the link
for u in users:
    for a in areas:
        user_area = u["Area"].split()
        tag = user_area[0]
        if (tag == a["Tag"]):
            user_ID.append(u["Id"])
            areas_ID.append(a["Id"])

# Uploading the link between users and areas
i = 0 
for ID in user_ID:
    url_string = os.getenv("BASE_URL") + os.getenv("LINK_URL_AREA") + str(ID)    
    url_users = f"{url_string}"     
    payload = {"Id": areas_ID[i]}
    upload_response = requests.post(url_users, headers=header, json=payload)     
    i += 1
    if upload_response.status_code != 201:
        print ("Upload failed:", upload_response.text)
        exit
    else:
        print ("Upload for user: ", ID, " completed")
