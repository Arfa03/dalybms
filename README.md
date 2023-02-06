# Daly Smart BMS MQTT sensor for generic application/HA
## **Thanks to @mindFreeze for the great work!**
Monitor a Daly Smart BMS connected through UART USB to raspberry and publish the data to MQTT. If HA have MQTT discovery enabled, the sensors will be added automatically to HA.

>Preferisci l'italiano?
>[lingua italiana](https://github.com/Arfa03/dalybms#italian-language)

# ![bms image](https://sc01.alicdn.com/kf/H357b7272ba0344eabd0c33c20101d0c7N.jpg)

Based on the protocol docs found here https://github.com/jblance/mpp-solar/blob/master/docs/protocols/DALY-Daly_RS485_UART_Protocol.pdf and the discussion here https://diysolarforum.com/threads/decoding-the-daly-smartbms-protocol.21898/

> Original repo here: https://github.com/MindFreeze/dalybms

The main code is in monitor.py, if you want to expand or change it.

Preferisci l'italiano?
[lingua italiana](https://github.com/Arfa03/dalybms#italian-language)

## Install

#### Using docker:

Clone this repo in your preferred directory:
```
git clone https://github.com/Arfa03/dalybms
```

Set your MQTT and battery data in config.py
```
cd dalybms
sudo nano config.py
```
Then exit nano with ctrl+s and ctrl+x.
Left the folder and build docker image:
```
cd ..
docker build dalybms
```
Copy the image ID in the message **Succesfully built >id<**
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

#### Without using docker
Just execute monitor.py after configured parameter in config.py.
In dalybms folder:
```
python3 monitor.py
```

Here the guide for execute automatically on startup:
> https://raspberrypi-guide.github.io/programming/run-script-on-boot

#### Energy and power

You can do this easily. For power in `W`, just create a template sensor and multiply `current * voltage`. https://www.home-assistant.io/integrations/template/

Then to get `kWh` for energy you can create an integration sensor from the power sensor. https://www.home-assistant.io/integrations/integration/


///////////////////////////////////////////////////////////////////////////////////////////////////////////
## Italian Language:
Controlla uno Smart BMS Daly collegato ad un raspberry tramite USB e pubblica i dati su un server MQTT. 
Se la tua istanza di Home Assistant ha la funzione autodiscovery dei dispositivi MQTT abilitata, i sensori saranno aggiunti automaticamente.

## Installazione

#### Usando docker:

Clona questa repo nella directory che preferisci
```
git clone https://github.com/Arfa03/dalybms
```

Imposta i dati del tuo server MQTT e della batteria in config.py
```
cd dalybms
sudo nano config.py
```
Dopodiché esci da nano con ctrl+s, poi ctrl+x
Esci dalla cartella ed effettua il build con docker dell'immagine
```
cd ..
docker build dalybms
```
Copia l'ID dell'immagine appena creata nel messaggio **Succesfully built >id<**
A questo punto avvia l'immagine e controlla che dopo circa un minuto arrivino i dati.
Seleziona la porta USB corretta se necessario.
```
docker run -it --device=/dev/ttyUSB0 --name bms-daly --restart unless-stopped <image-id>
```
Quando vedrai i dati a schermo, tutto è andato come dovrebbe! Ferma l'esecuzione premendo ctrl+c.
Ora puoi far partire il container in background, per lasciargli fare le sue magie.
```
docker container start bms-daly
```
Finito!
I sensori appariranno automaticamente in HomeAssistant se hai precedentemente abilitato la funzione autodiscovery, altrimenti dovrai aggiungerli manualmente.

#### Senza usare docker
Avvia semplicemente monitor.py dopo aver configurato i parametri in config.py.
Recati nella cartella dalybms ed esegui il comando:
```
python3 monitor.py
```
Per far sì che si avvii automaticamente all'avvio del sistema, qui trovi la guida:
> https://raspberrypi-guide.github.io/programming/run-script-on-boot

#### Energia e potenza

Puoi ottenerle facilmente. Per la potenza in `W` crea un modello template e moltiplica corrente * tensione
https://www.home-assistant.io/integrations/template/

Per ottenere l'energia in `kWh` invece, puoi creare un sensore integrativo.
https://www.home-assistant.io/integrations/integration/