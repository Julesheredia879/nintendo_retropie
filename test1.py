import time
import serial
import re
import RPi.GPIO as GPIO
import os,sys

def lectura(serial_port):
    accumulated_data = ''  # Variable para acumular los datos recibidos

    while True:
        try:
            read_byte = serial_port.read().decode('utf-8')  # Decodifica el byte a una cadena UTF-8
            #print(read_byte, end='')  # Imprime el byte (opcional, solo para depuración)

            accumulated_data += read_byte

            if read_byte == '\n':
                # Encuentra un salto de línea, devuelve la cadena acumulada hasta ese punto
                return accumulated_data
        except serial.SerialException as e:
            #print("-")
            reconectar_serial(serial_port)
            return None  # Puedes manejar la reconexión aquí o devolver un valor específico


def reconectar_serial(serial_port):
    while True:
        try:
            serial_port.close()
            serial_port.open()
            #print("Reconnected to serial port.")
            break
        except serial.SerialException as e:
            #print("Error reconnecting to serial port")
            time.sleep(1)  # Espera 1 segundo antes de intentar la reconexión nuevamente


def verificar_estructura(data):
    pattern = re.compile(r'\$ SmartUPS (.*?),Vin (.*?),BATCAP (.*?),Vout (.*?) \$')

    matches = pattern.findall(data)

    if len(matches) == 1:
        version, vin, batcap, vout = matches[0]
        return True, version, vin, batcap, vout
    else:
        return False, None, None, None, None








class UPS2_IO:
    def __init__(self,bcm_io=18):
        self.shutdown_check_pin = bcm_io
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.shutdown_check_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.shutdown_check_pin, GPIO.FALLING, callback= self.RPI_shutdown,bouncetime=1000)


    def RPI_shutdown(self,channel):
        print("detect bat LOW, system will shutdown in 10s!")
        for i in range(10,0,-1):
            print(i,end = ' ',flush=True)
            time.sleep(1)
            
        print("\nexecute System shudown!\n")
        os.system("sudo shutdown -t now")
        sys.exit()
    

    def cleanup():
        print("clean up GPIO.")
        GPIO.cleanup() 


    def datos_de_regreso(ser):
        try:
            dato =lectura(ser)
            if dato ==None:
                dato=anterior
            print(dato)
            es_valido, version, vin, batcap, vout = verificar_estructura(dato)

            if es_valido:
                print("Estructura válida:")
            #print(f"Versión: {version}")
                print(f"Vin: {vin}")
                print(f"BATCAP: {batcap}")
                print(f"Vout: {vout}")
                print(" ")
                anterior=dato
            else:
                print("Estructura no válida")
                print(" ")
        except Exception as error:
            print("E")


# Crear instancia del objeto Serial
ser = serial.Serial("/dev/ttyAMA0", baudrate=9600)
global dato=""
global anterior="$ SmartUPS V3.2P,Vin NG,BATCAP 100,Vout 5178 $"
control=UPS2_IO()
while True:
    datos_de_regreso()
