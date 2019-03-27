import serial
ser = serial.Serial()
from time import sleep
ser.port = "/dev/ttyACM0"
#ser.port = "/dev/ttyS2"
ser.baudrate = 9600
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2
sendtray = []
def listtray(msg_payload):
    for key , value in msg_payload.items() :
        if value == 1 :
            sendtray.append(key)
    return sendtray

def sendData (sendtray):
    ser.open()
    sleep(1)
    for i in sendtray:
        ser.flushOutput()
        ser.flushInput()
        ser.write(b'%d' %(i))
        print("message sent"+str(i))
        feedback = ser.read(1)
        print(feedback)
        while feedback != b'%d' %(i) :
             sleep(0.4)
             feedback = ser.read(1)
             print("waiting...")
             print(feedback)
    ser.close()
    status = 'sendData done'
    return status

sendData(listtray({1:1 , 2:1}))
