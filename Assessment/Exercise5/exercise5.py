#5. Threads
    
from machine import Pin, ADC
import _thread
import utime

# Variable para controlar si se debe imprimir
printing_enabled = True
lock = _thread.allocate_lock()  # Lock para evitar condiciones de carrera

# Función para imprimir los valores
def print_values():
    global printing_enabled
    global lock
    
    pin = Pin(34)
    adc=ADC(pin)
    adc.atten(ADC.ATTN_11DB)

    while True:
        with lock:
            if printing_enabled:
                val1=adc.read()
                val2=3.3*val1/4095
                print('Raw value: ',val1,' and voltage: ',val2)
            utime.sleep(1)

# Función para leer el botón y controlar la impresión
def control_printing():
    global printing_enabled
    global lock
    
    button = Pin(0, Pin.IN, Pin.PULL_UP)

    while True:
        # Supongamos que la lectura del botón devuelve 1 si está presionado y 0 si no
        #button_state = 0  # Supongamos que inicialmente no está presionado
        if not button.value():  # Si el botón se presiona (LOW porque tiene PULL_UP)
            with lock:
                printing_enabled = not printing_enabled
            # Espera un tiempo para evitar múltiples cambios rápidos debido a rebotes del botón
            utime.sleep(1)
            
try:
    # Crear e iniciar los hilos
    _thread.start_new_thread(print_values, ())
    _thread.start_new_thread(control_printing, ())

    # Mantener el hilo principal corriendo
    while True:
        pass
except KeyboardInterrupt:
    # Captura Ctrl + C para detener los hilos y salir del programa
    with lock:
        printing_enabled = False
    utime.sleep(2)  # Espera para permitir que los hilos se detengan
    print("Programa detenido por el usuario.")