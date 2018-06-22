import os
import serial
from threading import (Event, Thread)

event = False
ser = serial.Serial('/dev/ttyACM0',115200,timeout=1)

def upload_current_data():
    f = open('/home/pi/current_detector/outlet/data/current.txt','w')
    data_cnt = 0
    global ser,event
    try:
        while 1:
            if event == True:
                f.close()
                os.remove('/home/pi/current_detector/outlet/data/current.txt')
                f = open('/home/pi/current_detector/outlet/data/current.txt','a')
                continue
            serial_str = ser.readline()
            #print serial_str;
            #print event
            f.write(serial_str)
            data_cnt = data_cnt + 1
            if data_cnt == 20000:
                data_cnt = 0
                f.close()
                os.remove('/home/pi/current_detector/outlet/data/current.txt')
                f = open('/home/pi/current_detector/outlet/data/current.txt','a')
    except KeyboardInterrupt:
        f.close()
        pass
    
    
def main():
    global ser,event
    t = Thread(target=upload_current_data)
    t.start()
    try:
        while 1:
            str = raw_input()
            ser.write(str)
            if str == '1':
                event = True
            elif str == '0':
                event = False
    except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
