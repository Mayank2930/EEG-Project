# import requests
# ESP8266_IP = "192.168.1.100"
# PORT = 80

# def send_to_arduino(command):
#     url = f"http://{ESP8266_IP}:{PORT}/"
#     try:
#         response = requests.post(url, data={'command': command})
#         if response.status_code == 200:
#             return True
#         else:
#             return f"Failed to send command. HTTP {response.status_code}: {response.text}"
#     except Exception as e:
#         return str(e)
    
import serial
import time

ARDUINO_PORT = "COM5"  
BAUD_RATE = 9600
TIMEOUT = 2  

def send_to_arduino(command):
    try:
        with serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=TIMEOUT) as arduino:
            arduino.write(str(command).encode())  # Send the command as bytes
            print(f"Command '{command}' sent to Arduino.")
    except Exception as e:
        print(f"Error: {e}")


