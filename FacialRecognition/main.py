#!/usr/bin/python3

# Import necessary libraries
from signal import pause                    # For signal handling
from datetime import datetime               # For handling date and time
from time import sleep                      # For time-related functions
import time                                 # For time functions
from gpiozero import Button                 # For controlling GPIO pins
import cv2                                  # OpenCV for image processing
from simple_facerec import SimpleFacerec    # Custom face recognition library
import pyautogui                            # Library to get screen resolution
import requests                             # For sending HTTP requests
from requests.auth import HTTPBasicAuth     # For HTTP authentication
import pyzbar.pyzbar as pyzbar              # For decoding barcodes
from dotenv import load_dotenv              # For loading variables from a .env file
import os                                   # For interacting with the operating system, including environmental variables
import firebase_admin
from firebase_admin import credentials, firestore, storage, db

os.environ['QT_QPA_PLATFORM'] = 'xcb'

# Load variables from .env file
load_dotenv()

# Retrieve variables from the .env file to use in HTTP Requests
username = os.getenv('USERNAME')        # Get the username from the .env file
password = os.getenv('PASSWORD')        # Get the password from the .env file
base_url = os.getenv('URL')             # Get the base URL from the .env file
firebase_bucket = os.getenv('BUCKET')   # Get the bucket ID from the .env file
firebase_URL = os.getenv('DB_URL')      # Get the DB URL from the .env file

# Firebase Setup
cred=credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': firebase_bucket,    # BUCKET ID
    'databaseURL': firebase_URL          # DB URL
})

bucket = storage.bucket()                   # Create a bucket object for the default bucket
ref = db.reference('/')                     # Create a reference to the root of the database
audittrail_ref = ref.child('audittrail')    # Create a reference to the audittrail collection
employees_ref = ref.child('employees')      # Create a reference to the employees collection

# print("Url:{} | USERNAME: {} | PASSWORD: {}".format(url, username, password)) # For Debug

# Create a session with authentication for HTTP Requests
session = requests.Session()
session.auth = HTTPBasicAuth(username, password)

# Get the screen resolution
screen_width, screen_height = pyautogui.size()

#print("screen_width: {} | screen_height: {}".format(screen_width, screen_height)) # For Debug

# Set the capture resolution (optional)
capture_width, capture_height = 960, 720  # Adjust these values as needed

#print("capture_width: {} | capture_height: {}".format(capture_width, capture_height)) # For Debug

# Calculate the position for centering the window
window_x = int((screen_width - capture_width) / 2)
window_y = int((screen_height - capture_height) / 2)

#print("window_x: {} | window_y: {}".format(window_x, window_y)) # For Debug

# Initialize face recognition from images in the 'images/' folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Load Camera
cap = cv2.VideoCapture(0)

#print("CAP_PROP_FRAME_WIDTH: {} | CAP_PROP_FRAME_HEIGHT: {}".format(cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT)) # For Debug

# Set the video size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, capture_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, capture_height)

# Create a set to store recognized names
names_set = set()

# Define buttons connected to GPIO pins
buttons = {
    Button(26): '1', # Button Colour: Red
    Button(21): '2', # Button Colour: Blue
    Button(20): '3', # Button Colour: Yellow
    Button(16): '4', # Button Colour: Green
    Button(12): '5'  # Button Colour: Black
}

# global variables 
checkQRCode=0   # Enable QR Code Check
toggle=0        # This is a global variable 
globalbtn=0     # global button value

def set_global_toggle():
    global toggle  # Declaring that we're using the global variable
    toggle=1       # Modifying the global variable inside the function

def set_global_checkQRCode():
    global checkQRCode    # Declaring that we're using the global variable
    if checkQRCode == 0:
        checkQRCode=1     # Modifying the global variable inside the function
    else:
        checkQRCode=0     # Modifying the global variable inside the function

def set_globalbtn(button):
    global globalbtn    # Declaring that we're using the global variable
    globalbtn=button    # Modifying the global variable inside the function

# Function to decode barcode from camera image
def decodeQRCode(image):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)
    print('reading...', end='\r')
    for barcode in barcodes:
        barcodeData = barcode.data.decode()
        barcodeType = barcode.type
        print("Type:{} | Data: {}".format(barcodeType, barcodeData))
        #print('globalbtn testing: ', buttons[globalbtn])   # Debug
        
        if toggle != 1:
            if name in names_set:                
                firstname, lastname = name.split() # split the name up                
                accesskey = get_accesskey(firstname, lastname) # Get the employeeID

                # print('accesskey testing: ', accesskey)  # For Debug

                # If Barcode is correct
                if barcodeData == accesskey:
                    set_global_checkQRCode()   # Modifying the global variable            

                    # if the name is in the recognized set
                    if name in names_set:                        
                        firstname, lastname = name.split() # split the name up
                        allowedDevices = get_devices(firstname, lastname) # Get Allowed Devices
                        
                        #print(allowedDevices) #Debug

                        if int(buttons[globalbtn]) in allowedDevices:                
                            toggle_device(globalbtn)  # Toggle Device
                            set_global_toggle()       # Modifying the global variable
                        else:                            
                            print(f'{int(buttons[globalbtn])} is not in allowedDevices') 
                        
                        device, image_url = setAudittrail(globalbtn, firstname, lastname)  # Set Audittrail                     
                else:
                    print("Wrong QR Code Scanned")

            if int(buttons[globalbtn]) == 3 and barcodeData == "AllAccess": 
                firstname = 'QR Code'
                lastname = 'Activation'
                toggle_device(globalbtn)    # Toggle Device
                set_global_toggle()         # Modifying the global variable 
                device, image_url = setAudittrail(globalbtn, firstname, lastname)  # Set Audittrail            
            
    return image

# Define action for button press
def toggle_device(button):
    
    # Concatenate the base URL with the specific endpoint for HTTP Requests
    endpoint = buttons[button]      # Value to be pulled from DB
    url = f"{base_url}{endpoint}"   # Concatenate the base URL with the specific endpoint for HTTP Requests
    
    #print(f"Button# {buttons[button]} on GPIO{button.pin.number} pressed") # For Debug
    
    response = session.get(url) # Send a GET request with authentication to the specified URL

    # Check the response
    if response.status_code == 200:
        print(f"Request successful! Toggled Device#{buttons[button]}")
    else:
        print(f"Request failed with status code {response.status_code}")    

# Function to perform actions based on facial recognition 
def checkForKnownFace():  

    # Check if the name is not 'Unknown' 
    if name != 'Unknown':  
        names_set.add(name)    
    else:                
        print("Access Denied")       

# Needs Facial Recognition and QR Code read
def security_type_1():
    checkForKnownFace()    
    set_global_checkQRCode()      

# Needs Facial Recognition
def security_type_2():
    checkForKnownFace() 
   
    # if the name is in the recognized set
    if name in names_set:        
        firstname, lastname = name.split() # split the name up
        allowedDevices = get_devices(firstname, lastname) # Get Allowed Devices

        # print(', '.join(allowedDevices))  # For Debug

        if int(buttons[globalbtn]) in allowedDevices:                
            toggle_device(globalbtn)  
        else:                            
            print(f'{int(buttons[globalbtn])} is not in allowedDevices') 

        device, image_url = setAudittrail(globalbtn, firstname, lastname)  # Set Audittrail


# Needs QR Code read only set to AllAccess
def security_type_3():    
    set_global_checkQRCode() 

# Needs Button Press - HTTP Request
def security_type_4():    
    checkForKnownFace() 
   
    # if the name is in the recognized set
    if name in names_set:        
        firstname, lastname = name.split() #split the name up  

        allowedDevices = get_devices(firstname, lastname) # Get the allowedDevices

        if int(buttons[globalbtn]) in allowedDevices:
            # print(f'{int(buttons[globalbtn])} is in allowedDevices') # For Debug                   
            
             # Concatenate the base URL with the specific endpoint for HTTP Requests
            endpoint = buttons[button]      # Value to be pulled from DB
            url = f"{base_url}{endpoint}"   # Concatenate the base URL with the specific endpoint for HTTP Requests
        
            #print(f"Button# {buttons[button]} on GPIO{button.pin.number} pressed")  # For Debug

            response = session.get(url) # Send a GET request with authentication to the specified URL

            # print(', '.join(allowedDevices)) # For Debug

            device, image_url = setAudittrail(globalbtn, firstname, lastname)

            # Check the response
            if response.status_code == 200:
                print(f"Request successful! Toggled Device#{buttons[button]}")
            else:
                print(f"Request failed with status code {response.status_code}")  
        else:                            
            print(f'{int(buttons[globalbtn])} is not in allowedDevices')      

def security_type_5():
    checkForKnownFace() 
    # if the name is in the recognized set
    if name in names_set:        
        firstname, lastname = name.split()  #s plit the name up
        allowedDevices = get_devices(firstname, lastname)  # Get the allowedDevices

        # print(', '.join(allowedDevices))  # For Debug

        if int(buttons[globalbtn]) in allowedDevices:
            # print(f'{int(buttons[globalbtn])} is in allowedDevices') # For Debug                   
            device, image_url = setAudittrail(globalbtn, firstname, lastname) 
       
            request_access(device, firstname, lastname, image_url) 
        else:                            
            print(f'{int(buttons[globalbtn])} is not in allowedDevices')        


def setAudittrail(button, firstname, lastname):    
    now = datetime.now()                                         # Get the current date and time  
    formatted_date_time = now.strftime("%d%m%Y_%H%M%S")          # Format the date and time
    formatted_date_time_DB = now.strftime("%d/%m/%Y %H:%M:%S")   # Format the date and time   

    image_name = f'{firstname}_{lastname}_{formatted_date_time}' # Use the formatted date and time in a file name

    cv2.imwrite(f'./images/access/{image_name}.jpg', original_frame) # Save the image

    device = buttons[button] # Setting Devive to Activate
    image_url = store_file(f'./images/access/{image_name}.jpg') # Image URL to send
    
    employeeID = get_id(firstname, lastname) # Get the employeeID
   
    print('employeeID: ', employeeID)  # Print the employeeID   
    push_db(employeeID, device, firstname, lastname, image_url, formatted_date_time_DB, f'./{image_name}.jpg') # Push to DB

    os.remove(f'./images/access/{image_name}.jpg') # Delete Local Image 
    
    return device, image_url # Return the values

# Define action for when button is press
def device_interaction(button):    
    set_globalbtn(button)# set global variable

    # print('globalbtn: ', buttons[globalbtn])   # Debug 
    
    # Set function name to call based on button value
    securityCheck = {
        1: security_type_1,
        2: security_type_2,
        3: security_type_3,
        4: security_type_4,
        5: security_type_5
    }

    # call the function associated with the button value
    securityCheck.get(int(buttons[button]) , lambda: "Invalid button")()

# Function to send HTTP request to the specified URL
# sends request to Telegram Bot asking for access
def request_access(device, firstname, lastname, image_url):
    access_point = 'telegram'                  # Value to be pulled from DB
    url_access = f"{base_url}{access_point}"   # Concatenate the base URL with the specific endpoint for HTTP Requests

    # Set the headers for the HTTP request
    headers = {
        'Content-Type': 'application/json',
    }

    # Set the parameters for the HTTP request
    params = {
        'device': device,
        'firstname': firstname,
        'lastname': lastname,
        'image': image_url
    }

    # Send a GET request with authentication to the specified URL
    response = session.get(url_access, params=params, headers=headers)

    # Check the response
    if response.status_code == 200:
        print(f"HTTP Respose Code: 200")
    else:
        print(f"failed")

# Function to delete a file from the Firebase Storage bucket
def delete_file(file_path):    
    blob = bucket.blob(file_path) # Create a reference to the file    
    blob.delete()                 # Delete the file       

# Function to store a file in the Firebase Storage bucket
def store_file(fileLoc):
    filename=os.path.basename(fileLoc)       # Get the file name from the file path    
    blob = bucket.blob('access/' + filename) # Create a reference to the file in the bucket
    outfile=fileLoc                          # Set the file path for the file to be uploaded
    blob.upload_from_filename(outfile)       # Upload the file to the bucket   
    blob.make_public()                       # Make the blob publicly readable    
    file_url = blob.public_url               # Get the URL of the file
    return file_url # Return the URL of the file

# Function to push data to the Firebase Realtime Database
def push_db(employeeID, device, firstname, lastname, image_url, time, fileLoc):
  filename=os.path.basename(fileLoc)        # Get the file name from the file path   

  # Push file reference to image in Realtime DB
  audittrail_ref.push({
    'employeeID': employeeID,
    'device': device,
    'fullname': firstname + ' ' + lastname,
    'image_url': image_url,
    'image': filename,
    'timestamp': time}
  )

# Function to get the employeeID from the Firebase Realtime Database
def get_id(firstname, lastname):
    # Query the database for a document with the specified fullName
    query = employees_ref.order_by_child('fullName').equal_to(firstname + ' ' + lastname)
    
    snapshot = query.get()     # Get the query results
    
    if snapshot:                              # Check if the query returned any results
        doc = next(iter(snapshot.items()))    # Get the first document from the query results
        data = doc[1]                         # Get the document's data       
        return data['employeeID']             # Return the employeeID
    else:
        print(f'No employeeID found for "{firstname} {lastname}"')
        return 'Unknown'

# Function to get the allowedDevices from the Firebase Realtime Database
def get_devices(firstname, lastname):
    # Query the database for a document with the specified fullName
    query = employees_ref.order_by_child('fullName').equal_to(firstname + ' ' + lastname)
    
    snapshot = query.get()    
    
    if snapshot:                              # Check if the query returned any results
        doc = next(iter(snapshot.items()))    # Get the first document from the query results
        data = doc[1]                         # Get the document's data       
        return data['devices']                # Return the employeeID
    else:
        print(f'No devices found for "{firstname} {lastname}"')
        return None

# Function to get the accessKey from the Firebase Realtime Database
def get_accesskey(firstname, lastname):
   # Query the database for a document with the specified fullName
    query = employees_ref.order_by_child('fullName').equal_to(firstname + ' ' + lastname)
    
    snapshot = query.get()    
    
    if snapshot:                              # Check if the query returned any results
        doc = next(iter(snapshot.items()))    # Get the first document from the query results
        data = doc[1]                         # Get the document's data       
        return data['accessKey']              # Return the employeeID
    else:
        print(f'No accessKey found for "{firstname} {lastname}"')
        return 'Unknown'

# Main loop for capturing and processing video frames
try:
    while True:
        ret, frame = cap.read()             
        
        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            
            # When button is pressed, perform facial recognition actions
            # Assign actions to button press and release events
            for button in buttons:
                button.when_pressed = device_interaction

            # Check if the name is not 'Unknown'
            if name in names_set:
              # Display name around detected face
              cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)              

            # Check if QR Code is to be read
            if checkQRCode == 1:
                im=decodeQRCode(frame) 
                
            original_frame = frame.copy()
            # Display rectangle around detected face            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)                                   

        # Display the video
        cv2.imshow('Facial Recognition and QR Code Reading', frame)
        cv2.moveWindow('Facial Recognition and QR Code Reading', window_x - 200, window_y - 200)

        key = cv2.waitKey(1)
        if key == 27: # Press ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()        

except KeyboardInterrupt:
    pass
