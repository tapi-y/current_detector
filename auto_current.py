import serial
import datetime


def main():
    ser = serial.Serial('/dev/current',115200,timeout=1)
    
    for i in range(10):
        f = open('none-'+ str(i) +'.txt','w')
        start = datetime.datetime.now()
        delta=0
        while delta< 5:
            serial_str = ser.readline()
            print serial_str;
            f.write(serial_str)
            deltatime = datetime.datetime.now()-start
            delta = deltatime.total_seconds()
        f.close()

if __name__ == '__main__':
    main()
