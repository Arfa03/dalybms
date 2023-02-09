MQTT_SERVER = "mqtt_ip_address"
MQTT_USER = "mqtt_user"
MQTT_PASS = "mqtt_pass"
MQTT_DISCOVERY_PREFIX = "homeassistant"
MQTT_CLIENT_ID = "dalybms"
DEVICE = "/dev/ttyUSB0"
DEVICE_ID = "Daly-Smart-BMS"
CELLS_IN_SERIES = 16


# If you have poor network connection, set this to True
NETWORK_PROBLEMS = True

# if you have problems of missing sensor on the first start, set this to 1 and restart.
MQTT_DISCOVERY_WAIT = 0.3