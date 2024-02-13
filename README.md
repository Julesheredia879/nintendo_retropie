# Gameboy Zero RetroPie status overlays
This repository contains a script to display lovely slightly-transparent overlays on top of your RetroPie games and emulationstation menus

## What can it do?
- display battery level (Requires ADS1x15)
- display WiFi state (connected/disconnected/disabled)
- display Bluetooth state (connected/disconnected/disabled)
- display under-voltage state
- display warning if frequency-capped
- display warning if throttling
- adjust icons' position to current display resolution
- gracefully shut down the Pi after 60s from when voltage goes below 3.2V
- show a big imminent shutdown warning when the counter starts ticking

## What do I need to get it running?
- See [installation instructions](#installation-instructions) below for setup steps
- [pngview](https://github.com/AndrewFromMelbourne/raspidmx/tree/master/pngview) from AndrewFromMelbourne
- [material-design-icons](https://github.com/google/material-design-icons/archive/master.zip) from Google
- Adafruit ADS1015 with Vbat on A0 (or alternative)
- a symbolic link to *overlay\_icons/ic\_battery\_alert\_red\_white\_36dp.png* under *material\_design\_icons\_master/device/drawable-mdpi/*
- an entry in crontab to start this on boot
- check and adjust paths in the script header if required
- some battery readings calibration - check logs
- some patience

## But what does it look like?
Like that:

![Bluetooth, wifi connected, battery discharging](_images/connected.png)  
Bluetooth, wifi connected, battery discharging

![Bluetooth, wifi disconnected, battery discharging](_images/disconnected.png)  
Bluetooth, wifi disconnected, battery discharging

![Bluetooth, wifi disabled, battery charging](_images/disabled_charging.png)  
Bluetooth, wifi disabled, battery charging

![CPU throttled due to high temperature](_images/throttle.png)  
CPU throttled due to high temperature

![Under-Voltage, Freq-capped due to high temperature, battery critical, shutdown imminent warning](_images/freqcap_undervolt_criticalbat_shutdown.png)  
Under-Voltage, Freq-capped due to high temperature, battery critical, shutdown imminent warning - shutting down in 60s

![In-game](_images/ingame.png)  
In-game
### 0. Install nintendo switch 

    
    git clone https://github.com/nicman23/dkms-hid-nintendo
    cd dkms-hid-nintendo
    sudo dkms add .
    sudo dkms build nintendo -v 3.2
    sudo dkms install nintendo -v 3.2
    sudo apt-get install libevdev-dev
    git clone https://github.com/DanielOgorchock/joycond.git
    cd joycond
    cmake .
    sudo make install
    sudo systemctl enable --now joycond
### 0.1 Install things with bluetooth     
    sudo apt install bluetooth blueman bluez-hcidump checkinstall libusb-dev libbluetooth-dev joystick pkg-config
    sudo apt install pi-bluetooth
        


https://retropie.org.uk/docs/Nintendo-Switch-Controllers/ ,
https://retropie.org.uk/docs/PS3-Controller/?h=bluetooth#persisting-bluetooth-ps3controller-only ,
https://retropie.org.uk/docs/Bluetooth-Controller/?h=blu ,
https://github.com/Julesheredia879/nintendo_retropie.git and 
https://projects.raspberrypi.org/en/projects/nix-python-reading-serial-data



## Installation Instructions

SSH into your device or access the terminal using F4. We're assuming you already have Internet access configured

### 1. Install pngview by AndrewFromMelbourne
    mkdir ~/src && cd ~/src
    git clone --depth 1 https://github.com/AndrewFromMelbourne/raspidmx.git
    cd raspidmx/
    make -j4
    sudo cp pngview/pngview /usr/local/bin/


### 2. Download the script and install dependencies:
    mkdir ~/scripts && cd ~/scripts
    git clone --depth 1 https://github.com/Julesheredia879/nintendo_retropie.git
    sudo apt-get update
    sudo apt-get install build-essential python3-dev python3-smbus python3-pip
    sudo pip3 install pyserial

#### 3. Test the script:

    python3 ~/scripts/nintendo_retropie/overlay.py &

You should now see overlay icons

### 4. Set up script autostart
Note: Do not use rc.local, it's deprecated

    sudo crontab -e

Then at the bottom of the file, add the line:

    @reboot python3 /home/pi/scripts/gbz_overlay/overlay.py

You can use this one-liner instead if you prefer:

    (crontab -l ; echo "@reboot python3 /home/pi/scripts/gbz_overlay/overlay.py") | crontab -

### 5. Reboot
