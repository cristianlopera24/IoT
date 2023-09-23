#3. SUEÑO PROFUNDO

from machine import Pin
from machine import ADC
from time import sleep_ms
from machine import deepsleep
from machine import RTC

pin = Pin(34)
adc=ADC(pin)
adc.atten(ADC.ATTN_11DB)
button = Pin (0, Pin.IN)
    
if button.value()==1:
    deepsleep(1000)


#3. SUEÑO LIGERO

from machine import Pin
from machine import ADC
from time import sleep_ms
from time import sleep
from machine import lightsleep
from machine import RTC

pin = Pin(34)
adc=ADC(pin)
adc.atten(ADC.ATTN_11DB)
button = Pin (0, Pin.IN)

print('Going into Light Sleep Mode')

while True:
    val1 = adc.read()
    val2 = 3.3 * val1 / 4095
    print('Raw value: ', val1, ' and voltage: ', val2)

    if button.value()==0:
        break
    lightsleep(1000)     #10000ms sleep time
    
