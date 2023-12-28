#!/usr/bin/python3

# Import necessary libraries
from signal import pause                    # For signal handling
from datetime import datetime               # For handling date and time
from time import sleep                      # For time-related functions
import time                                 # For time functions
from gpiozero import Button            # For controlling GPIO pins
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
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
base_url = os.getenv('URL')  # Store the base URL without the endpoint
firebase_bucket = os.getenv('BUCKET')  # Store the base URL without the endpoint
firebase_URL = os.getenv('DB_URL')  # Store the base URL without the endpoint

# Firebase Setup
cred=credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': firebase_bucket, #  BUCKET ID
    'databaseURL': firebase_URL # DB URL
})

bucket = storage.bucket() # Bucket

ref = db.reference('/')
audittrail_ref = ref.child('audittrail')
employees_ref = ref.child('employees')

# Concatenate the base URL with the specific endpoint for HTTP Requests
endpoint = '1'                  # Value to be pulled from DB
url = f"{base_url}{endpoint}"

# print("Url:{} | USERNAME: {} | PASSWORD: {}".format(url, username, password))

# Create a session with authentication for HTTP Requests
session = requests.Session()
session.auth = HTTPBasicAuth(username, password)

# Get the screen resolution
screen_width, screen_height = pyautogui.size()

# For Debug
#print("screen_width: {} | screen_height: {}".format(screen_width, screen_height))

# Set the capture resolution (optional)
capture_width, capture_height = 960, 720  # Adjust these values as needed

# For Debug
#print("capture_width: {} | capture_height: {}".format(capture_width, capture_height))

# Calculate the position for centering the window
window_x = int((screen_width - capture_width) / 2)
window_y = int((screen_height - capture_height) / 2)

# For Debug
#print("window_x: {} | window_y: {}".format(window_x, window_y))

# Initialize face recognition from images in the 'images/' folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Load Camera
cap = cv2.VideoCapture(0)

# For Debug
#print("CAP_PROP_FRAME_WIDTH: {} | CAP_PROP_FRAME_HEIGHT: {}".format(cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT))

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
globalbtn=0        #global button value

def set_global_toggle():
    global toggle  # Declaring that we're using the global variable
    toggle=1    # Modifying the global variable inside the function

def set_global_checkQRCode():
    global checkQRCode  # Declaring that we're using the global variable
    if checkQRCode == 0:
        checkQRCode=1    # Modifying the global variable inside the function
    else:
        checkQRCode=0

def set_globalbtn(button):
    global globalbtn  # Declaring that we're using the global variable
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
        print('globalbtn testing: ', buttons[globalbtn])   
        
        if toggle != 1:
            if name in names_set:
                #split the name up
                firstname, lastname = name.split()

                # Get the employeeID
                accesskey = get_accesskey(firstname, lastname)

                print('accesskey testing: ', accesskey)

            # If Barcode is correct
            if barcodeData == "Test":
                set_global_checkQRCode()   # Modifying the global variable            

                # if the name is in the recognized set
                if name in names_set:
                    #split the name up
                    firstname, lastname = name.split()

                    # Get the employeeID
                    allowedDevices = get_devices(firstname, lastname) # Get Allowed Devices
                    
                    #print(allowedDevices) #Debug

                    if int(buttons[globalbtn]) in allowedDevices:
                        print(f'{int(buttons[globalbtn])} is in allowedDevices')                    
                        toggle_device(globalbtn)  
                    else:
                        
                        print(f'{int(buttons[globalbtn])} is not in allowedDevices') 
                    
                    setAudittrail(globalbtn, firstname, lastname) # Set Audittrail
                
                if int(buttons[globalbtn]) == 3:
                    firstname = 'QR Code'
                    lastname = 'Ativation'
                    toggle_device(globalbtn) 
                    setAudittrail(globalbtn, firstname, lastname) # Set Audittrail
                
                
            else:
                print("Wrong QR Code Scanned")

            set_global_toggle()
    return image

# Define action for button press
def toggle_device(button):
    
    # Concatenate the base URL with the specific endpoint for HTTP Requests
    endpoint = buttons[button]                  # Value to be pulled from DB
    url = f"{base_url}{endpoint}"
    
    # For Debug
    #print(f"Button# {buttons[button]} on GPIO{button.pin.number} pressed")

     # Send a GET request with authentication to the specified URL
    response = session.get(url)

    # Check the response
    if response.status_code == 200:
        print(f"Request successful! Toggled Device#{buttons[button]}")
    else:
        print(f"Request failed with status code {response.status_code}")    

# Function to perform actions based on facial recognition 
def checkForKnownFace():  

    # Check if the name is not 'Unknown' 
    if name != 'Unknown':  
        #print("Access Granted to ", name)
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
         #split the name up
        firstname, lastname = name.split()

        toggle_device(globalbtn)

        # Get the employeeID
        allowedDevices = get_devices(firstname, lastname)

        print(', '.join(allowedDevices))

        setAudittrail(globalbtn, firstname, lastname) # Set Audittrail


# Needs QR Code read
def security_type_3():    
    set_global_checkQRCode() 


# Needs Button Press - HTTP Request
def security_type_4():    
    checkForKnownFace() 
   
    # if the name is in the recognized set
    if name in names_set:
         #split the name up
        firstname, lastname = name.split()   

        # Get the employeeID
        allowedDevices = get_devices(firstname, lastname)

        print(', '.join(allowedDevices))

        setAudittrail(globalbtn, firstname, lastname) # Set Audittrail

    # Concatenate the base URL with the specific endpoint for HTTP Requests
    endpoint = buttons[button]                  # Value to be pulled from DB
    url = f"{base_url}{endpoint}"
   
    # For Debug
    #print(f"Button# {buttons[button]} on GPIO{button.pin.number} pressed")

     # Send a GET request with authentication to the specified URL
    response = session.get(url)

    # Check the response
    if response.status_code == 200:
        print(f"Request successful! Toggled Device#{buttons[button]}")
    else:
        print(f"Request failed with status code {response.status_code}")    

def security_type_5():
    checkForKnownFace() 
    # if the name is in the recognized set
    if name in names_set:        
        #split the name up
        firstname, lastname = name.split()

        # Get the current date and time
        now = datetime.now()

        # Format the date and time
        formatted_date_time = now.strftime("%d%m%Y_%H%M%S")
        formatted_date_time_DB = now.strftime("%d/%m/%Y %H:%M:%S")

        # Use the formatted date and time in a file name
        image_name = f'{firstname}_{lastname}_{formatted_date_time}'

        cv2.imwrite(f'./images/access/{image_name}.jpg', original_frame) # Save the image

        device = buttons[button] # Setting Devive to Activate
        image_url = store_file(f'./images/access/{image_name}.jpg') # Image URL to send
        
        # Get the employeeID
        employeeID = get_id(firstname, lastname)
       
        # Print the employeeID
        print('employeeID: ', employeeID)    
        push_db(employeeID, device, firstname, lastname, image_url, formatted_date_time_DB, f'./{image_name}.jpg')
        
        #os.remove(f'./images/access/{firstname}_{lastname}.jpg') # Delete Local Image
        os.remove(f'./images/access/{image_name}.jpg') # Delete Local Image      
       
        request_access(device, firstname, lastname, image_url)


def setAudittrail(button, firstname, lastname):
    # Get the current date and time
    now = datetime.now()

    # Format the date and time
    formatted_date_time = now.strftime("%d%m%Y_%H%M%S")
    formatted_date_time_DB = now.strftime("%d/%m/%Y %H:%M:%S")

    # Use the formatted date and time in a file name
    image_name = f'{firstname}_{lastname}_{formatted_date_time}'

    cv2.imwrite(f'./images/access/{image_name}.jpg', original_frame) # Save the image

    device = buttons[button] # Setting Devive to Activate
    image_url = store_file(f'./images/access/{image_name}.jpg') # Image URL to send
    
    # Get the employeeID
    employeeID = get_id(firstname, lastname)
   
    # Print the employeeID
    print('employeeID: ', employeeID)    
    push_db(employeeID, device, firstname, lastname, image_url, formatted_date_time_DB, f'./{image_name}.jpg')
    
    os.remove(f'./images/access/{image_name}.jpg') # Delete Local Image 

# Define action for when button is press
def device_interaction(button):
    # set global variable
    set_globalbtn(button)

    print('globalbtn: ', buttons[globalbtn])   
    
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

def request_access(device, firstname, lastname, image_url):
    # Concatenate the base URL with the specific endpoint for HTTP Requests  
    access_point = 'telegram'                  # Value to be pulled from DB
    url_access = f"{base_url}{access_point}"

    #print(url_access)

    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'device': device,
        'firstname': firstname,
        'lastname': lastname,
        'image': image_url
    }

    #response = session.get(url)

    response = session.get(url_access, params=params, headers=headers)


    # Check the response
    if response.status_code == 200:
        print(f"HTTP Respose Code: 200")
    else:
        print(f"failed")

    #delete_file(url_access) # Delete Local Image

def delete_file(file_path):
    # Create a reference to the file
    blob = bucket.blob(file_path)

    # Delete the file
    blob.delete()       

def store_file(fileLoc):
    filename=os.path.basename(fileLoc)

    # Store File in FB Bucket
    #blob = bucket.blob(filename)
    # Include the folder name in the blob name
    blob = bucket.blob('access/' + filename)
    outfile=fileLoc
    blob.upload_from_filename(outfile)

    # Make the blob publicly readable
    blob.make_public()

    # Get the URL of the file
    file_url = blob.public_url

    return file_url


def push_db(employeeID, device, firstname, lastname, image_url, time, fileLoc):

  filename=os.path.basename(fileLoc)

  # Push file reference to image in Realtime DB
  audittrail_ref.push({
    'employeeID': employeeID,
    'device': device,
    'fullname': firstname + ' ' + lastname,
    'image_url': image_url,
    'image': filename,
    'timestamp': time}
  )

def get_id(firstname, lastname):
    # Query the database for a document with the specified fullName
    query = employees_ref.order_by_child('fullName').equal_to(firstname + ' ' + lastname)
    
    snapshot = query.get()    
    
    if snapshot:                              # Check if the query returned any results
        doc = next(iter(snapshot.items()))    # Get the first document from the query results
        data = doc[1]                         # Get the document's data       
        return data['employeeID']             # Return the employeeID
    else:
        print('No document with the specified filename found')
        return 'Unknown'

def get_devices(firstname, lastname):
    # Query the database for a document with the specified fullName
    query = employees_ref.order_by_child('fullName').equal_to(firstname + ' ' + lastname)
    
    snapshot = query.get()    
    
    if snapshot:                              # Check if the query returned any results
        doc = next(iter(snapshot.items()))    # Get the first document from the query results
        data = doc[1]                         # Get the document's data       
        return data['devices']             # Return the employeeID
    else:
        print('No document with the specified filename found')
        return None

def get_accesskey(firstname, lastname):
   # Query the database for a document with the specified fullName
    query = employees_ref.order_by_child('fullName').equal_to(firstname + ' ' + lastname)
    
    snapshot = query.get()    
    
    if snapshot:                              # Check if the query returned any results
        doc = next(iter(snapshot.items()))    # Get the first document from the query results
        data = doc[1]                         # Get the document's data       
        return data['accessKey']             # Return the employeeID
    else:
        print('No document with the specified filename found')
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
            #original_frame = frame.
            # Display rectangle around detected face            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)                                   

        # Display the video
        cv2.imshow('Facial Recognition and QR Code Reading', frame)
        cv2.moveWindow('Facial Recognition and QR Code Reading', window_x - 200, window_y - 200)

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()        

except KeyboardInterrupt:
    pass

#finally:
