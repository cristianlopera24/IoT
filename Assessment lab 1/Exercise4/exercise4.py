#4. SUEÑO PROFUNDO con valor maximo

from machine import Pin, ADC, deepsleep, RTC, wake_reason
from time import sleep_ms
import ujson

# Configuración del pin ADC
pin = Pin(34)
adc = ADC(pin)
adc.atten(ADC.ATTN_11DB)
button = Pin(0, Pin.IN)
rtc = RTC()

# Inicializar el valor máximo a un valor muy pequeño
max_value = 0
for _ in range(10):

    val1 = adc.read()
    val2 = 3.3 * val1 / 4095
    print('Raw value: ', val1, ' and voltage: ', val2)

# Actualizar el valor máximo si es necesario
    if val1 > max_value:
        max_value = val1
    
# Almacenar el valor máximo en el área de RAM RTC
    rtc.memory(ujson.dumps({'max_value': max_value}))

# Imprimir el valor máximo antes de entrar en suspensión profunda
print('Max value: ', max_value)
# Comprobar si se presionó el botón para entrar en suspensión profunda

if button.value() == 1:
    # Entrar en suspensión profunda durante 1 segundo
    deepsleep(1000)
