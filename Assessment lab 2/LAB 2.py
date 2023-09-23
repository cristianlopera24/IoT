# MAESTRIA EN INGENIERIA, ELECTIVA INTERNET DE LAS COSAS
# LABORATORIO 2, MARIA CAMILA QUINTERO Y CRISTIAN LOPERA

#2. central BLE
# This example finds and connects to a BLE temperature sensor (e.g. the one in ble_temperature.py).

import bluetooth
import random
import struct
import time
import sys
from simpleBLE import BLECentral 

# Bluetooth object
ble = bluetooth.BLE()

# Environmental service
service='4d810f27-2bce-4def-968c-c58ed45e586c'

# Temperature characteristic
characteristic='b96c84d4-1dd7-416e-95ea-1837e56cdff2' 

# BLE Central object
central = BLECentral(ble,service,characteristic)

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

central.on_notify(callback= lambda data :print('Notified') )

# Explicitly issue reads, using "print" as the callback.
while central.is_connected():
    central.read(callback=lambda data: print(data[0]))
    time.sleep_ms(2000)

# Alternative to the above, just show the most recently notified value.
# while central.is_connected():
#     print(central.value())
#     time.sleep_ms(2000)

print("Disconnected")