import current_detector as cd
import threading
import time
import re
import urllib2
import json


def upload_sensor_data():
    detection_lavel=cd.get_lavel()
    data = {'data': {'push':{
			imageUrl: '/assets/img/fridge/beer.png',
			clickUrl: '/fridge-beer'
		}},
            'eventName': 'user99999/panel'}
    if(detection_lavel == 'none'):
        return
    url = 'https://fy33dypvtg.execute-api.us-west-1.amazonaws.com/prod/v0/panel'
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))
    t = threading.Timer(0, upload_sensor_data)
    t.start()
    
def main():
    cd.initialize()
    t = threading.Thread(target=upload_sensor_data)
    t.start()

    
if __name__ == '__main__':
    main()