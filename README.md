# Daly Smart BMS MQTT sensor for generic application/HA
## **Thanks to @mindFreeze for the great work!**
Monitor a Daly Smart BMS through UART USB and publish the data to MQTT. If HA have MQTT discovery enabled, the sensors will be added automatically to HA.

# ![bms image](https://sc01.alicdn.com/kf/H357b7272ba0344eabd0c33c20101d0c7N.jpg)

Based on the protocol docs found here https://github.com/jblance/mpp-solar/blob/master/docs/protocols/DALY-Daly_RS485_UART_Protocol.pdf and the discussion here https://diysolarforum.com/threads/decoding-the-daly-smartbms-protocol.21898/

> Original repo here: https://github.com/MindFreeze/dalybms

The main code is in monitor.py, if you want to expand or change it.

## Install

###### Using docker:

Clone this repo in your preferred directory:
```
git clone https://github.com/Arfa03/daly-bms-comms
```

Set your MQTT and battery data in config.py
```
cd daly-bms-comms
sudo nano config.py
```
Then exit nano with ctrl+s and ctrl+x.
Left the folder and build docker image:
```
cd ..
docker build dalybms
```
Copy the image ID in the message *Succesfully built <id> *
Then run the image for checking if data flows, correct the USB port if needed
```
docker run -it --device=/dev/ttyUSB0 --name bms-daly --restart unless-stopped <image-id>
```
When you see data flowing, in about 1 mins, you're set! Stop the execution by hitting ctrl+c.
Now you can start the container in background for leave him do it's magics.
```
docker container start bms-daly
```
You're set!
The sensors will automatically appear in HomeAssistant if you have enabled MQTT autodiscovery, otherwise you've to add it manually.

###### Without using docker
Just execute monitor.py after configured parameter in config.py.

Here the guide:
> https://raspberrypi-guide.github.io/programming/run-script-on-boot

## Energy and power

You can do this easily. For power in `W`, just create a template sensor and multiply `current * voltage`. https://www.home-assistant.io/integrations/template/

Then to get `kWh` for energy you can create an integration sensor from the power sensor. https://www.home-assistant.io/integrations/integration/


