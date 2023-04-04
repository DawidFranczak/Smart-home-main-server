
# About the project 
**Smart home** is a project that allows controlling certain elements of a house through a website.

 
**The project includes management of** : 
* sunblinds, 
* indoor lighting,
* cascading stair lighting,
* aquarium lighting,
* outdoor lighting,
* opening doors/gates using magnetic cards,
* periodic temperature measurements.

To check the functionality of the website, you can create an account with the suffix **"tester"**.
Then three devices of each type and random temperature
values from the last 8 days will be assigned. Devices with the name "tester" are "connected" to a physical device.


## Website

The website is bilingual. The default language is English, but if the browser language is set to Polish, the website will be displayed in Polish.

### Login
<img src="/readme_images/login.png" alt="Login page" style="width: 400px;">

### Register
<img src="/readme_images/register.png" alt="Register page" style="width: 400px;">


### Home page
<img src="/readme_images/home.png" alt="Home page" style="width: 800px;">

On the homepage, you can navigate by selecting the appropriate option from the navigation bar or by clicking on the corresponding icon.

### Devices
<img src="/readme_images/devices_1.png" alt="Devices page 1">

Here, you can see all added devices, remove a device by clicking on the red cross icon (the cross icons will be displayed after clicking on "remove device" button), and add a device by clicking on "add device" button.

<img src="/readme_images/devices_2.png" alt="Devices page 2">

To add a new device, enter its name and select its functionality, then click the "Save" button.

### Sunblinds
<img src="/readme_images/sunblind.png" alt="Sunblind page" style="width: 800px;">

By setting the appropriate value on the slider, you can move the sunblind to any position. If it is not possible to communicate with the microcontroller, the message "No connection" will be displayed. However, if it is not possible to connect to the home server, the message "No connection to home server" will be displayed.
To start using the sunblinds, they must be calibrated first. After pressing the "Calibration" button, calibration buttons will appear on the right side.

### Calibration

<img src="/readme_images/calibration.png" alt="Calibration page">

To calibrate the roller blind, use the up/down arrows and follow the instructions accordingly.


### Aquariums
<img src="/readme_images/aqua_1.png" alt="Aquarium page 1">

After selecting an aquarium, a new window will open, presenting you with various settings you can change, including: the color of the LED strip, the time when the LED and fluorescent lights turn on, and whether you want it to work in automatic or manual mode.

<img src="/readme_images/aqua_2.png" alt="Aquarium page 2">

In manual mode, you can turn the LED strip and fluorescent lights on or off, and change the color of the LED strip. The aquarium in manual mode will be skipped during the cyclic check of the time.


### Stairs
<img src="/readme_images/stairs.png" alt="Stairs page">

After selecting the stairs, you can change settings such as the lighting time, brightness, and smoothness of illumination.

### Temperature chart 
<img src="/readme_images/chart.png" alt="Chart page">

By selecting a date range, a chart representing the measurements taken will be displayed. If the number of days in the given range is fewer than 8, a single chart with temperature readings taken every hour will be displayed.if the number is greater than 8 days, two charts with average temperatures will be displayed. Additionally, a table with average temperature values will be displayed below the charts.

### Setting
<img src="/readme_images/settings.png" alt="Settings page">

In the settings, you can change your password, email address, profile picture on the home page as well as delete your account, and change the address of the home server.

### Light
<img src="/readme_images/light.png" alt="Light page">

Turning on/off the lamp is done by clicking on the light icon.
If successful, the light bulb icon will change accordingly. If it is not possible to communicate with the microcontroller, the message "No connection" will be displayed. However, if it is not possible to connect to the home server, the message "No connection to home server" will be displayed.

### RPL
<img src="/readme_images/rpl.png" alt="RPL page">

By pressing the button or placing an RFID card on the reader, the lamps assigned to the group can be turned on.One lamp can be assigned to any number of RFID sensors or buttons, while each sensor or button can only be assigned to one lamp.

# Installation
```bash
python3 -m pip install -r requirements.txt
```

Then you can run the server using 

``` bash
python manage.py runserver
```

# Repositories
This project consists of 3 repositories.
* Main server repository.
* Client-side server repository. -> https://github.com/DawidFranczak/Smart-home-client-server
* Repository of microcontroller software -> https://github.com/DawidFranczak/Smart-home-microcontrollers
