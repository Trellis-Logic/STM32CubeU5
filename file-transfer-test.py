import serial
import time
import os
import threading
import sys

# Serial port settings
port = "COM4"    # Serial port to use
baudrate = 921600  # Baud rate
#baudrate = 9600  # Baud rate
# File to send
file_path = sys.argv[1]

# Open serial port with CTS enabled and RTS manually managed
ser = serial.Serial(
    port,
    baudrate,
    timeout=2,
    rtscts=False,  # RTS/CTS flow control on (CTS will be used)
)
# Clear input buffer
ser.reset_input_buffer()
# Event to signal the reading thread to stop
stop_event = threading.Event()
bytes_sent = 0
# Function to send the file
def send_file(ser, file_path):
    global bytes_sent
    file_size = os.path.getsize(file_path)
    print(f"Sending File {file_path}")
    chunk_size = 1024  # Adjust chunk size as needed
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            print('.',end='', flush=True)
            ser.write(chunk)
            bytes_sent += len(chunk)

# Send the file
send_file(ser, file_path)
print(f"Sent {bytes_sent} bytes")
# Signal the reading thread to stop and wait for it to finish
ser.close()
