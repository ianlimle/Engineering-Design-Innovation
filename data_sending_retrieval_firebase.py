import requests
import json
import serial
import time

firebase_url = "https://bosch-55278.firebaseio.com/"
#URL to firebase database

#status = {"Temperature": "0.0", "Gas Switch Status": "On", "Audio": "0.0" }
#initialize the dictionary of sensor values

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=0)

fixed_interval = 10

location = "Bosch Data Repository"
            
var_lst = ["Temperature", "Gas Switch Status", "Audio"]

current_time = int(time.time())- int(time.time()) % 5
   
while True:
    try:
        read_serial =  ser.readline()
        sensor_list = read_serial.decode("ascii").strip().split(",")
        print("no. of sensor entries:{0}, sensor_list:{1}".format(len(sensor_list),sensor_list))
    
        time_hhmmss = time.strftime("%H:%M:%S")
        date_ddmmyyyy = time.strftime("%d/%m/%Y")
        
        data = {"date": date_ddmmyyyy, "time": time_hhmmss}
        
        if sensor_list == ['']:
            data.update({"status": "None"})
            print(data)
            print("\n")
        
        elif (len(sensor_list) == 3):
            for index in range(len(var_lst)):
                data.update({var_lst[index]:sensor_list[index]})
                

        result = requests.post(firebase_url + "/" + location + ".json", data=json.dumps(data))
                
        print("Record inserted. Result Code = " + str(result.status_code) + "," + result.text)
        print("\n")
               
    except IOError:
        print("Error")
        print("\n")
                
    time.sleep(fixed_interval)
        

    
        
        
    