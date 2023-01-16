# About the project
'Smart Home' allows you to control devices connected to your localhost via the website.

You can control:

light in the aquarium,
light on the stairs,
lamp in the house,
sunblind.

You can also open the gate in the fence via an RFID card and make hourly temperature measurements.

The microcontroller software located in this repo is intended for the ESP8266.

On the website, you can create an account.

If you create an account with 'tester' in the name, e.g. 'usertester' or 'testeruser', three devices from each category will be added to your account.

Device names containing 'tester' are 'connected' to real devices, so you can check what happens on the website when you control a real device.

On the website, you can do the following:

Light -> Turn on/off light for selected light,

Stairs -> Change lightning time, brightness, number of steps to full brightness and manually turn on/off lightning,

Temperature -> See temperature measurement chart with average day and night temperatures,

Aquarium -> Change color of RGB LEDs, lighting time of LEDs and fluorescent lamps, manually turn on/off LEDs and fluorescent lamps

Sunblind -> Calibrate the sunblind and its sliding and unfolding

Device -> Add, delete and search for devices

RPL -> Group together outside lamps with buttons and RFID sensors

Settings -> Change password, email, image on home page and delete account

If you forgot your password, you can use the 'remind password' option on the login page. To do this, you need the e-mail address provided during registration.

To check the website, you can use https://dawidfranczak.pythonanywhere.com.

# Installation

You can use the environment located in server/smart_home/env 

or use pip:

python -m pip install -r requirements.txt

Then you can run the server using python manage.py runserver

To upload the software to the ESP8266, you need Visual Studio Code with Platform.io or Arduino IDE.
