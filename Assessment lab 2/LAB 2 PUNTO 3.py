#punto 3.

from os import statvfs
from time import sleep
import network
from mqtt import MQTTClient 
import machine 
import time
import json
import random
from micropython import const
from machine import Pin, ADC
import bluetooth
from simpleBLE import BLECentral
import struct
import sys

USERNAME = const('AwA8LwEUKAUaJwcPIwkNLh8')
CLIENTID = const('AwA8LwEUKAUaJwcPIwkNLh8')
PASS = const('IbuPShk7ikfTJRNiO+W372u5')
SERVER = const('mqtt3.thingspeak.com')
CHANNEL = const('2279558')

# Inicializar el ADC para leer el sensor MQ135 en el pin 34

# Bluetooth object
ble = bluetooth.BLE()

# Servicio de Calidad del Aire
service = '4d810f27-2bce-4def-968c-c58ed45e586c' 

# Característica de Calidad del Aire
characteristic = 'b96c84d4-1dd7-416e-95ea-1837e56cdff2' 

# BLE Central object
central = BLECentral(ble, service, characteristic)
not_found = False

def on_scan(addr_type, addr, name):
    if addr_type is not None:
        print("Found sensor:", addr_type, addr, name)
        central.connect()
    else:
        global not_found
        not_found = True
        print("No sensor found.")

central.scan(callback=on_scan)
# Wait for connection...
while not central.is_connected():
    time.sleep_ms(100)
    if not_found:
        sys.exit()

print("Connected")
central.on_notify(callback=lambda data: print('Notified'))


client = MQTTClient(client_id = CLIENTID, server = SERVER, user = CLIENTID,password = PASS )
client.connect()

def publish(data):
    try:
        client.publish(topic="channels/" + CHANNEL + "/publish", msg='field1='+str(data))
    except OSError as e:
        print(e)
        print('Failed')

while central.is_connected():
    # Read the characteristic value
    central.read(callback=lambda data: publish(data[0]))
    time.sleep_ms(30000)

print("Disconnected")