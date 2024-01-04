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
    <li><a href="#Home-Assistant-run-on-a-Raspberry-Pi">Home Assistant run on a Raspberry Pi</a></li>    
    <li><a href="#installation">Installation</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- Home Assistant run on a Raspberry Pi -->
## Home Assistant run on a Raspberry Pi
Home Assistant running on a Raspberry Pi offers a versatile and accessible smart home solution. Leveraging the Pi's capabilities, it serves as a robust hub for automation, allowing users to seamlessly control and manage various smart devices. The combination of Home Assistant's flexibility and the Raspberry Pi's affordability creates an efficient, DIY-friendly platform for building and customizing smart home experiences.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Prerequisites

- Raspberry Pi with an SD card and power supply
- Internet connection
- Access to a router for network configuration

## Installation

### Step 1: Install Home Assistant

1. Download the Home Assistant image for your Raspberry Pi model from the [official website](https://www.home-assistant.io/installation/raspberrypi).
2. Flash the image to your SD card using a tool like [Balena Etcher](https://www.balena.io/etcher/).
3. Insert the SD card into your Raspberry Pi and power it on.
4. Follow the on-screen instructions to complete the setup.

### Step 2: Install HACS

1. Follow the instructions on the [HACS installation page](https://hacs.xyz/docs/installation/installation) to install HACS on your Home Assistant instance.

 Incase you need a video with instructions visit **[HOW TO - Install HACS 2023 ](https://youtu.be/oXaGqjaKbeE?si=TWl5kl-18Ps7yi3m)**

 **Note:** Home Assistant might look a bit different in your install as its a older video

### Step 3: Install Node-RED

1. In Home Assistant, go to the HACS Store.
2. Search for Node-RED and install it.
3. Follow the instructions on the [Node-RED installation page](https://zachowj.github.io/node-red-contrib-home-assistant-websocket/guide/installation.html) to complete the setup.

### Step 4: Install Node-RED Companion Integration

1. In Node-RED, go to the Palette Manager.
2. Search for Node-RED Companion and install it.

If you cant find the Palette Manager you can follow the instructions on the **[Node-RED Companion Integration](https://github.com/zachowj/hass-node-red)** git repo

### Step 5: Install HA Addons

1. Follow the instructions on the [Cloudflared installation page](https://github.com/brenner-tobias/ha-addons) to install Cloudflared on your Raspberry Pi.

### Step 6: Install Cloudflared

1. Follow the instructions on the [Cloudflared installation page](https://github.com/brenner-tobias/addon-cloudflared) to install Cloudflared on your Raspberry Pi.

### Step 7: Install Tuya

1. Follow the instructions on the [Tuya installation page](https://www.home-assistant.io/integrations/tuya/) to install Tuya on your Home Assistant instance.

## Usage

After installation, you can access your Home Assistant instance by navigating to `http://<your-raspberry-pi-ip-address>:8123` in your web browser.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact
Your Name - Kieron Garvey

Project Link: [https://github.com/ki321g/AMS/](https://github.com/ki321g/AMS)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



