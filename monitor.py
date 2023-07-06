#!/usr/bin/python3

# Protocol docs https://github.com/jblance/mpp-solar/blob/master/docs/protocols/DALY-Daly_RS485_UART_Protocol.pdf
# Protocol examples and more info https://diysolarforum.com/threads/decoding-the-daly-smartbms-protocol.21898/
# Forked from https://github.com/MindFreeze/dalybms

# Modified for work standalone on Raspberry Pi, to send MQTT data at remote HA instance 
from config import *
import serial
import binascii
import time
import os
import paho.mqtt.client as mqtt
  

network_problems = NETWORK_PROBLEMS
pause_between_discovery = MQTT_DISCOVERY_WAIT

print('Starting BMS monitor...')

ser = serial.Serial(DEVICE, 9600, timeout=1)  # open serial port

# connect to MQTT server


client = mqtt.Client(client_id=MQTT_CLIENT_ID)

client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_SERVER)



# config mqtt
devId = DEVICE_ID
BASE_TOPIC = MQTT_DISCOVERY_PREFIX + '/sensor/'
STATE_TOPIC = BASE_TOPIC + devId
STATUS_TOPIC = STATE_TOPIC + '_status'
CELLS_TOPIC = STATE_TOPIC + '_balance'
TEMP_TOPIC = STATE_TOPIC + '_temp'
INFO_TOPIC = STATE_TOPIC + '_info'
ALARM_TOPIC = STATE_TOPIC + '_alarm'

deviceConf = '"device": {"manufacturer": "Dongfuan Daly Electronics", "name": "Smart BMS", "identifiers": ["' + devId + '"]}'

# publish MQTT Discovery configs to Home Assistant

# note that time.sleep(1) is necessary for permit HA to add the sensor the first time, without this 
# some sensor can be not recognized

# battery percent
socHaConf = '{"device_class": "battery", "name": "Percentuale Batteria", "state_topic": "' + STATE_TOPIC +'/state", "unit_of_measurement": "%", "value_template": "{{ value_json.percentuale}}", "unique_id": "' + devId + '_soc", ' + deviceConf + ', "json_attributes_topic": "' + STATUS_TOPIC + '/state"}' 
client.publish(STATE_TOPIC +'_percent/config', socHaConf, 0, True)
time.sleep(pause_between_discovery)

# battery voltage
voltageHaConf = '{"device_class": "voltage", "name": "Tensione Batteria", "force_update": "true", "state_topic": "' + STATE_TOPIC +'/state", "unit_of_measurement": "V", "value_template": "{{ value_json.tensione}}", "unique_id": "' + devId + '_voltage", ' + deviceConf + '}'
client.publish(STATE_TOPIC + '_volt/config', voltageHaConf, 0, True)
time.sleep(pause_between_discovery)

# battery current
currentHaConf = '{"device_class": "current", "name": "Corrente Batteria", "state_topic": "' + STATE_TOPIC +'/state", "unit_of_measurement": "A", "value_template": "{{ value_json.corrente}}", "unique_id": "' + devId + '_current", ' + deviceConf + '}' 
client.publish(STATE_TOPIC + '_curr/config', currentHaConf, 0, True)
time.sleep(pause_between_discovery)

# BMS mode
chargeHaConf = '{"name": "Status", "state_topic": "' + INFO_TOPIC +'/state", "value_template": "{{ value_json.mode}}", "unique_id": "' + devId + '_status", ' + deviceConf + '}' 
client.publish(STATE_TOPIC + '_car/config', chargeHaConf, 0, True)
time.sleep(pause_between_discovery)

# battery SOC in AH
modeHaConf = '{"device_class": "current", "name": "SOC Ah", "state_topic": "' + INFO_TOPIC +'/state", "unit_of_measurement": "Ah", "value_template": "{{ value_json.socAh}}", "unique_id": "' + devId + '_mode", ' + deviceConf + '}' 
client.publish(STATE_TOPIC + '_mode/config', modeHaConf, 0, True)
time.sleep(pause_between_discovery)

# charging MOS status
modeHaConf = '{"device_class": "power", "name": "Stato MOS carica", "state_topic": "' + INFO_TOPIC +'/state", "value_template": "{{ value_json.chMos}}", "unique_id": "' + devId + '_chMos", ' + deviceConf + '}' 
client.publish(STATE_TOPIC + '_chMos/config', modeHaConf, 0, True)
time.sleep(pause_between_discovery)

# discharging MOS status
modeHaConf = '{"device_class": "power", "name": "Stato MOS scarica", "state_topic": "' + INFO_TOPIC +'/state", "value_template": "{{ value_json.dischMos}}", "unique_id": "' + devId + '_dischMos", ' + deviceConf + '}' 
client.publish(STATE_TOPIC + '_disCh/config', modeHaConf, 0, True)
time.sleep(pause_between_discovery)

# BMS cycles
cyclesHaConf = '{"name": "Cicli", "state_topic": "' + STATUS_TOPIC +'/state", "value_template": "{{ value_json.cicli}}", "unique_id": "' + devId + '_cicli", ' + deviceConf + '}' 
client.publish(STATE_TOPIC + '_cycles/config', cyclesHaConf, 0, True)
time.sleep(pause_between_discovery)

# difference from highest and lower cells in V
cellsHaConf = '{"device_class": "voltage", "name": "Differenza Celle", "state_topic": "' + CELLS_TOPIC + '/state", "unit_of_measurement": "V", "value_template": "{{ value_json.differenza}}", "json_attributes_topic": "' + CELLS_TOPIC + '/state", "unique_id": "' + devId + '_balance", ' + deviceConf + '}' 
client.publish(CELLS_TOPIC + '/config', cellsHaConf, 0, True)
time.sleep(pause_between_discovery)

# cells voltages
for cells in range(CELLS_IN_SERIES):
    cCell = str(cells+1)
    cellHaConf = '{"device_class": "voltage", "name": "Cella ' + cCell + '", "state_topic": "' + CELLS_TOPIC +'/state", "unit_of_measurement": "V", "value_template": "{{ value_json.cella' + cCell +'}}", "unique_id": "' + devId + '_cell-' + cCell +'-voltage", ' + deviceConf + '}'
    client.publish(CELLS_TOPIC + '_cella1'+cCell+'v/config', cellHaConf, 0, True)
    time.sleep(pause_between_discovery)


# cell with the lower voltage
cellMinHaConf = '{"device_class": "voltage", "name": "Cella Minima", "state_topic": "' + CELLS_TOPIC +'/state", "unit_of_measurement": "V", "value_template": "{{ value_json.minima}}", "unique_id": "' + devId + '_cell-min-value", ' + deviceConf + '}'
client.publish(CELLS_TOPIC + '_cellMin/config', cellMinHaConf, 0, True)
time.sleep(pause_between_discovery)

# cell with the highest voltage
cellMaxHaConf = '{"device_class": "voltage", "name": "Cella Massima", "state_topic": "' + CELLS_TOPIC +'/state", "unit_of_measurement": "V", "value_template": "{{ value_json.massima}}", "unique_id": "' + devId + '_cell-max-value", ' + deviceConf + '}'
client.publish(CELLS_TOPIC + '_cellMax/config', cellMaxHaConf, 0, True)
time.sleep(pause_between_discovery)

# number of the lower voltage cell
cellNoMinHaConf = '{"name": "Numero cella minima", "state_topic": "' + CELLS_TOPIC +'/state", "value_template": "{{ value_json.cella_minima}}", "unique_id": "' + devId + '_cell-no-min", ' + deviceConf + '}'
client.publish(CELLS_TOPIC + '_cellNoMin/config', cellNoMinHaConf, 0, True)
time.sleep(pause_between_discovery)

# number of the highest voltage cell
cellNoMaxHaConf = '{"name": "Numero cella massima", "state_topic": "' + CELLS_TOPIC +'/state", "value_template": "{{ value_json.cella_massima}}", "unique_id": "' + devId + '_cell-no-max", ' + deviceConf + '}'
client.publish(CELLS_TOPIC + '_cellNoMax/config', cellNoMaxHaConf, 0, True)
time.sleep(pause_between_discovery)

# average voltage of the cells
cellAvgHaConf = '{"device_class": "voltage", "name": "Media celle", "state_topic": "' + CELLS_TOPIC +'/state", "unit_of_measurement": "V", "value_template": "{{ value_json.media}}", "unique_id": "' + devId + '_cell-avg", ' + deviceConf + '}'
client.publish(CELLS_TOPIC + '_cellAvg/config', cellAvgHaConf, 0, True)
time.sleep(pause_between_discovery)

# sum of all the cells
cellSumHaConf = '{"device_class": "voltage", "name": "Somma celle", "state_topic": "' + CELLS_TOPIC +'/state", "unit_of_measurement": "V", "value_template": "{{ value_json.somma}}", "unique_id": "' + devId + '_cell-sum", ' + deviceConf + '}'
client.publish(CELLS_TOPIC + '_cellSum/config', cellSumHaConf, 0, True)
time.sleep(pause_between_discovery)

# battery temperature
tempHaConf = '{"device_class": "temperature", "name": "Temperatura Batteria", "state_topic": "' + TEMP_TOPIC + '/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.valore}}", "unique_id": "' + devId + '_temp", ' + deviceConf + ', "json_attributes_topic": "' + TEMP_TOPIC + '/state"}'
client.publish(TEMP_TOPIC + 'temp/config', tempHaConf, 0, True)
time.sleep(pause_between_discovery)

# alarm voltage
tempHaConf = '{"name": "Allarme tensione", "state_topic": "' + ALARM_TOPIC + '/state", "value_template": "{{ value_json.voltageAlarm}}", "unique_id": "' + devId + '_voltAlarm", ' + deviceConf + '}'
client.publish(ALARM_TOPIC + '_voltageAlarm/config', tempHaConf, 0, True)
time.sleep(pause_between_discovery)



def cmd(command):
    res = []
    ser.write(command)
    while True:
        s = ser.read(13)
        if (s == b''):
            break
        res.append(s)
    return res

def publish(topic, data):
    try:
        client.publish(topic, data, 0, False)
    except Exception as e:
        print("Error sending to mqtt: " + str(e))

def extract_cells_v(buffer):
    return [
        int.from_bytes(buffer[5:7], byteorder='big', signed=False),
        int.from_bytes(buffer[7:9], byteorder='big', signed=False),
        int.from_bytes(buffer[9:11], byteorder='big', signed=False)
    ]

def get_cell_balance(cell_count):
    res = cmd(b'\xa5\x40\x95\x08\x00\x00\x00\x00\x00\x00\x00\x00\x82')
    if len(res) < 1:
        print('Empty response get_cell_balance')
        return
    cells = []
    for frame in res:
        cells += extract_cells_v(frame)
    cells = cells[:cell_count]
    json = '{'
    sum = 0
    for i in range(cell_count):
        cells[i] = cells[i]/1000
        sum += cells[i]
        json += '"cella' + str(i+1) + '":' + str(cells[i]) + ','
    json += '"somma":' + str(round(sum, 1)) + ','
    json += '"media":' + str(round(sum/16, 3)) + ','
    min_v = min(cells)
    max_v = max(cells)
    json += '"minima":' + str(min_v) + ','
    json += '"cella_minima":' + str(cells.index(min_v) + 1) + ','
    json += '"massima":' + str(max_v) + ','
    json += '"cella_massima":' + str(cells.index(max_v) + 1) + ','
    json += '"differenza":' + str(round(max_v - min_v, 3))
    json += '}'
    if sum > 60: {print('Value too high: probably a read error. Skipping cells voltage.')}
    else: publish(CELLS_TOPIC + '/state', json)

def get_battery_state():
    res = cmd(b'\xa5\x40\x90\x08\x00\x00\x00\x00\x00\x00\x00\x00\x7d')
    if len(res) < 1:
        print('Empty response get_battery_state')
        return
    buffer = res[0]
    voltage = int.from_bytes(buffer[4:6], byteorder='big', signed=False) / 10
    current = int.from_bytes(buffer[8:10], byteorder='big', signed=False) / 10 - 3000
    soc = int.from_bytes(buffer[10:12], byteorder='big', signed=False) / 10    
    json = '{'
    json += '"tensione":' + str(voltage) + ','
    json += '"corrente":' + str(round(current, 1)) + ','
    json += '"percentuale":' + str(soc)
    json += '}'
    print(json)
    if voltage > 60: {print('Value too high: probably a read error. Skipping voltage.')}
    elif voltage < 40: {print('Value too low: probably a read error. Skipping voltage.')}
    elif current > 110: {print('Value too high: probably a read error. Skipping current.')}
    elif current < -110: {print('Value too low: probably a read error. Skipping current.')}
    elif soc > 101: {print('Value too high: probably a read error. Skipping soc.')}
    else: publish(STATE_TOPIC +'/state', json)

def get_battery_status():
    res = cmd(b'\xa5\x40\x94\x08\x00\x00\x00\x00\x00\x00\x00\x00\x81')
    if len(res) < 1:
        print('Empty response get_battery_status')
        return
    buffer = res[0]
    batt_string = int.from_bytes(buffer[4:5], byteorder='big', signed=False)
    temp = int.from_bytes(buffer[5:6], byteorder='big', signed=False)
    cycles = int.from_bytes(buffer[9:11], byteorder='big', signed=False)
    json = '{'
    json += '"stringa":' + str(batt_string) + ','
    json += '"temperatura":' + str(temp) + ','
    json += '"cicli":' + str(cycles)
    json += '}'
    if batt_string > 16: {print('Value too high: probably a read error. Skipping string.')}
    elif temp > 60: {print('Value too high: probably a read error. Skipping temp.')}
    else: publish(STATUS_TOPIC +'/state', json)

def get_battery_info():
    res = cmd(b'\xa5\x40\x93\x08\x00\x00\x00\x00\x00\x00\x00\x00\x80')
    if len(res) < 1:
        print('Empty response get_battery_info')
        return
    buffer = res[0]
    charger_mode = int.from_bytes(buffer[4:5], byteorder='big', signed=False)
    socAh = (int.from_bytes(buffer[8:12], byteorder='big', signed=False) / 1000)
    chMos = (int.from_bytes(buffer[5:6], byteorder='big', signed=False))
    dischMos = (int.from_bytes(buffer[6:7], byteorder='big', signed=False))

    if charger_mode == 1:
        charger = '"In carica"'
    elif charger_mode == 2:
        charger = '"In scarica"'
    elif charger_mode == 0:
        charger = '"Standby"'
    json = '{'
    json += '"mode":' + str(charger) + ','
    json += '"socAh":' + str(round(socAh, 1)) + ','
    json += '"chMos":' + str(chMos) + ','
    json += '"dischMos":' + str(dischMos)
    json += '}'
    # print(json)
    if socAh > 400: {print('Value too high: probably a read error. Skipping socAh.')}
    elif chMos > 1: {print('Value too high: probably a read error. Skipping chMos.')}
    elif dischMos > 1: {print('Value too high: probably a read error. Skipping dischMos.')}
    else: publish(INFO_TOPIC +'/state', json)

def get_battery_temp():
    res = cmd(b'\xa5\x40\x92\x08\x00\x00\x00\x00\x00\x00\x00\x00\x7f')
    if len(res) < 1:
        print('Empty response get_battery_temp')
        return
    buffer = res[0]
    maxTemp = int.from_bytes(buffer[4:5], byteorder='big', signed=False) - 40
    maxTempCell = int.from_bytes(buffer[5:6], byteorder='big', signed=False)
    minTemp = int.from_bytes(buffer[6:7], byteorder='big', signed=False) - 40
    minTempCell = int.from_bytes(buffer[7:8], byteorder='big', signed=False)
    json = '{'
    json += '"valore":' + str((maxTemp + minTemp) / 2) + ','
    json += '"temperatura_massima":' + str(maxTemp) + ','
    json += '"cella_temperatura_massima":' + str(maxTempCell) + ','
    json += '"temperatura_minima":' + str(minTemp) + ','
    json += '"cella_temperatura_minima":' + str(minTempCell)
    json += '}'
    if ((maxTemp + minTemp) / 2) > 60: {print('Value too high: probably a read error. Skipping average temp.')}
    else: publish(TEMP_TOPIC +'/state', json)

def get_battery_alarm():
    res = cmd(b'\xa5\x40\x98\x08\x00\x00\x00\x00\x00\x00\x00\x00\x85')
    if len(res) < 1:
        print('Empty response get_battery_alarm')
        return
    buffer = res[0]
    al1 = ord(buffer[4:5])
    al1 = bin(al1)[2:].rjust(8, '0')
    alarmMessage = ''
    if al1[0] == '1': alarmMessage = ''
    if al1[1] == '1': alarmMessage = ''
    if al1[2] == '1': alarmMessage = ''
    if al1[3] == '1': alarmMessage = ''
    if al1[4] == '1': alarmMessage = '"Allarme 1 tensione alta"'
    if al1[5] == '1': alarmMessage = '"Allarme 2 tensione alta"'
    if al1[6] == '1': alarmMessage = '"Allarme 1 tensione bassa"'
    if al1[7] == '1': alarmMessage = '"Allarme 2 tensione bassa"'
    if alarmMessage == '': alarmMessage = '"Nessun allarme tensione"'

    json = '{'
    json += '"voltageAlarm":' + str(alarmMessage)
    json += '}'
    publish(ALARM_TOPIC +'/state', json)

def setSocValue(soc):
    if isinstance(soc, int) and 0 <= soc <= 1000:
        print('Setting SoC value at: ' + str(soc / 10))
        base = b'\xa5\x40\x21\x08\x16\x0c\x0d\x15\x1d\x27'
        socValue = soc.to_bytes(2, 'big')
        completed = base + socValue
        checksum = ((sum(completed)) & 0xFF).to_bytes(1, 'big')
        command = completed + checksum
        res = cmd(command)
        print("SoC set to " + str(soc / 10))
    else:
        print("Invalid input")

i=0

while True:
    # Set function topic:
    socTopic = "homeassistant/command/dalybms/soc"

    if i == 10 and network_problems == True:   
        try:
            client = mqtt.Client(client_id=MQTT_CLIENT_ID)
            client.username_pw_set(MQTT_USER, MQTT_PASS)
            client.connect(MQTT_SERVER)
            publish(STATE_TOPIC +'/mqtt_info', 'mqtt reconnected')
            i=0
        except Exception as e:
            print(e)
    if network_problems: i = i+1

    def on_connect(client, userdata, flags, rc):
        client.subscribe([(socTopic, 0)])

    def on_message(client, userdata, msg):
        time.sleep(3)
        try:
            if(msg.topic == socTopic):
                value = (int(msg.payload.decode()))*10
                setSocValue(value)
        except Exception as e:
            print('Invalid input.')
        

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop(.1)

    ######################################################

    get_battery_state()
    get_cell_balance(CELLS_IN_SERIES)
    get_battery_status()
    get_battery_info()
    get_battery_temp()
    get_battery_alarm()
    time.sleep(1)
    
ser.close()
print('done')