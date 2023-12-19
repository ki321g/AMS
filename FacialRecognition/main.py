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
os.environ['QT_QPA_PLATFORM'] = 'xcb'
#from firebase import FirebaseApp    # Custom face recognition library

# Load variables from .env file
load_dotenv()

# Retrieve variables from the .env file to use in HTTP Requests
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
base_url = os.getenv('URL')  # Store the base URL without the endpoint
firebase_bucket = os.getenv('BUCKET')  # Store the base URL without the endpoint
firebase_URL = os.getenv('DB_URL')  # Store the base URL without the endpoint

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
print("screen_width: {} | screen_height: {}".format(screen_width, screen_height))

# Set the capture resolution (optional)
capture_width, capture_height = 960, 720  # Adjust these values as needed

# For Debug
print("capture_width: {} | capture_height: {}".format(capture_width, capture_height))

# Calculate the position for centering the window
window_x = int((screen_width - capture_width) / 2)
window_y = int((screen_height - capture_height) / 2)

# For Debug
print("window_x: {} | window_y: {}".format(window_x, window_y))

# Initialize face recognition from images in the 'images/' folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Load Camera
cap = cv2.VideoCapture(0)

# For Debug
print("CAP_PROP_FRAME_WIDTH: {} | CAP_PROP_FRAME_HEIGHT: {}".format(cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT))

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
    checkQRCode=1    # Modifying the global variable inside the function

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
        
        if toggle != 1:

            if barcodeData == "Test":
                # # Send a GET request with authentication to the specified URL
                # response = session.get(url)

                # # Check the response
                # if response.status_code == 200:
                #     print("Request successful! Plug Turned on")
                # else:
                #     print(f"Request failed with status code {response.status_code}")  
                toggle_device(globalbtn)
            else:
                print("Wrong QR Code Scanned")

            set_global_toggle()
    return image

# Define action for button press
def toggle_device(button):
    
    # Concatenate the base URL with the specific endpoint for HTTP Requests
    endpoint = buttons[button]                  # Value to be pulled from DB
    url = f"{base_url}{endpoint}"
   
    print(f"Button# {buttons[button]} on GPIO{button.pin.number} pressed")

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
        print("Access Granted to ", name)
        names_set.add(name)  

        # # Send a GET request with authentication to the specified URL
        # response = session.get(url)

        # # Check the response
        # if response.status_code == 200:
        #     print("Request successful! Plug Turned on")
        # else:
        #     print(f"Request failed with status code {response.status_code}")    
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
        toggle_device(globalbtn)

# Needs QR Code read
def security_type_3():    
    set_global_checkQRCode() 

def security_type_4():
    print("Case#4")
    
    # Concatenate the base URL with the specific endpoint for HTTP Requests
    endpoint = buttons[button]                  # Value to be pulled from DB
    url = f"{base_url}{endpoint}"
   
    print(f"Button# {buttons[button]} on GPIO{button.pin.number} pressed")

     # Send a GET request with authentication to the specified URL
    response = session.get(url)

    # Check the response
    if response.status_code == 200:
        print(f"Request successful! Toggled Device#{buttons[button]}")
    else:
        print(f"Request failed with status code {response.status_code}")    

def security_type_5():
    print("Case#5")
    # Save the image
    cv2.imwrite('mynewimage.jpg', frame)

# Define action for when button is press
def device_interaction(button):
    # set global variable
    set_globalbtn(button)
    
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

            # Decode QR/barcode if the name is in the recognized set
            if name in names_set:
              # Display name around detected face
              cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)              

            if checkQRCode == 1:
                im=decodeQRCode(frame) 
        
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
