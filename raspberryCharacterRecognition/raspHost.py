import serial
import time

#aspetto che il raspberry mi scriva "letter", poi faccio qualcosa
#va unito al codice che riconosce i caratteri

def readLetter():
    return "c"

if __name__ == '__main__':
    ser= serial.Serial("/dev/ttyACM1", 9600, timeout=1)
    ser.reset_input_buffer()
    
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        if "letter" in line:
            lette=readLetter()+"\n"
            ser.write(lette.encode("utf-8"))
            
