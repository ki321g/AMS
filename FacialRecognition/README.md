<a name="readme-top"></a>
<!-- PROJECT SHIELDS -->
<!-- PROJECT LOGO -->
<div align="center">
  <h1 align="center">AMS - “Automated Management Systems”</h1>
<!--   <img src="readme/images/weathertop.png" alt="Logo">  -->
</div>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#facial-recognition">Facial Recognition</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- Facial Recognition -->
## Facial Recognition
Documentation is the lifeblood of any project, serving as its roadmap, its history, and its guidebook. It's the bridge between ideas and execution. Clear, concise, and comprehensive documentation not only ensures smoother development but also empowers users to harness the full potential of the project. Within this repository, you'll find my documentation, designed to explain how i have done things, and pave the way for an enriching experience while looking at this project."

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Installation -->
### Installation

To import all the relevant libraries into your Python script on your Raspberry Pi, you need to install them first. Below you will find a list of the commands I used in my terminal to install these libraries. 

I had to run some of the command with **--break-system-packages** added to the end in order to force them to install properly

Follow these steps to set up and run the website:

1. **1.	Update & Upgrade Raspberry Pi**: First, you need to update & upgrade your Pi:

```bash
sudo apt update -y && sudo apt upgrade -y
``` 

2. **CV2 (OpenCV)**: : This command installs the OpenCV (Open Source Computer Vision Library) package for Python 3. OpenCV is a library of programming functions mainly aimed at real-time computer vision. It's used for tasks such as object detection, face recognition, and many other computer vision tasks:

```bash
sudo apt-get install python3-opencv -y
``` 

3. **pyzbar**: is a Python library to read one-dimensional barcodes and QR codes. It uses the zbar barcode detection library, which means it can handle multiple types of barcodes and QR codes:

```bash
pip3 install pyzbar --break-system-packages
``` 

4. **Opencv-python**: is a library of Python bindings designed to solve computer vision problems:

```bash
pip3 install opencv-python --break-system-packages
``` 
**Note**: This may take some time

1. **face_recognition**: is a simple and easy-to-use library for face recognition tasks. It's built using dlib's state-of-the-art face recognition built with deep learning. The model has an accuracy of 99.38% on the Labeled Faces in the Wild benchmark.:

```bash
pip3 install face_recognition --break-system-packages
``` 

6. **pyautogui**: is a Python module that programmatically controls the mouse and keyboard: 

```bash
pip3 install pyautogui --break-system-packages
``` 

7. **requests**: is a popular Python library used for making HTTP requests:

```bash
pip3 install requests
```  

8. **python-dotenv**:  is a Python library that allows you to specify environment variables in traditional UNIX-like ".env" (dotenv) files. This can be particularly useful in development environments where you might want to keep certain settings, such as database credentials or API keys, out of your code:

```bash
pip3 install python-dotenv
```  

9. **gpiozero**: is a simple interface to GPIO devices with Raspberry Pi. It provides a straightforward way to control devices such as LEDs, buttons, sensors, motors, and other physical components that you can connect to your Raspberry Pi.:

```bash
sudo pip3 install gpiozero
``` 

10. **firebase-admin**: The firebase-admin SDK provides an API that allows you to interact with Firebase from a Python environment.:

```bash
pip3 install firebase-admin
```  


11. **cvzone**: is a computer vision library that includes several utilities to help you with computer vision tasks.:

```bash
pip3 install cvzone
```  

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact
Your Name - Kieron Garvey

Project Link: [https://github.com/ki321g/AMS/](https://github.com/ki321g/AMS)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



