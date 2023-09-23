#punto 1
from machine import Pin, ADC
import time
import bluetooth
import random
from simpleBLE import BLEPeripheral

adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB) 

# Bluetooth object
ble = bluetooth.BLE()

# Servicio de Calidad del Aire
service = '4d810f27-2bce-4def-968c-c58ed45e586c'

# Característica de Calidad del Aire
characteristic = 'b96c84d4-1dd7-416e-95ea-1837e56cdff2'

# BLE peripheral object
air_quality = BLEPeripheral(ble, "mc", service, characteristic)


while True:
    # Leer el valor del sensor MQ135
    
    valor_mq135 = adc.read()

    print('Raw value: ', valor_mq135)
    
    # Escribir el valor leído en la característica BLE
    air_quality.set_values([valor_mq135], notify=True, indicate=False)
    
    time.sleep_ms(1000)  # Esperar un segundo antes de la próxima lectura