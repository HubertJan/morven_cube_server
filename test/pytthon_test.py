import time
import serial

serialConnection = serial.Serial("COM6", "9600")
serialConnection.timeout = 1
print("Test yolo.")
time.sleep(5)
serialConnection.write("Screw you.".encode())
text1 = serialConnection.readline()
serialConnection.write("Screw you.".encode())
text2 = serialConnection.readline()
text2 = serialConnection.readline()
print("Text: " + str(text2))
input()