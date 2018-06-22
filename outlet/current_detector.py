
"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
Created on Thu Jun  7 22:39:21 2018

@author: Tatsuya
"""
import os
import glob
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import time
import pickle
import re
import urllib2
import json
from threading import (Event, Thread)

DETECT_DURATION = 1.0
SAMPLING_TIME = 1000
detect_lavel = ''
event = False

paths = glob.glob('/home/pi/current_detector/CurrentData_constant/*')
files = [os.path.basename(p) for p in paths]
labels = list(set([f.split('-')[0] for f in files]))
#'none','fryer','vacumer','ketle','light','fan','canopner','hotsand','sharpner','heater','slowcooker','handmixer','ricecooker','mixer','toaster'
lavel_cnt = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def get_features(measure_data):
    mean_of_abs = measure_data.abs().mean()[0]
    return(np.array([mean_of_abs, 1]))

def upload_sensor_data(str):
    data = {'data':{'data':{'outlet':{
        'device': str
    }}},
    'eventName': 'user99999/panel/outlet'}

    url = 'https://fy33dypvtg.execute-api.us-west-1.amazonaws.com/prod/v0/ctrl';
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    time.sleep(0.5)

    response = urllib2.urlopen(req, json.dumps(data))

def power_detector():
    pre_detect=''
    detect_count = 0

    
    with open('/home/pi/current_detector/outlet/model/clf_v1.pickle', mode='rb') as f:
        clf = pickle.load(f)
    
    while(1):
        try:
            if(event == True):
                continue
            filename = ('/home/pi/current_detector/outlet/data/current.txt')
            measure_data = pd.read_csv(filename, header=None)[10:-1][-int(DETECT_DURATION*SAMPLING_TIME):]
            measure_data = measure_data.astype(np.float)
            test_feature = get_features(measure_data)
            predict_label = clf.predict(test_feature.reshape(1, -1))
            predict_prob = clf.predict_proba(test_feature.reshape(1, -1))
            # print pd.DataFrame(predict_prob, columns=clf.classes_)
            print 'detection: %s (%.2f)' % (predict_label[0], predict_prob.max())
            if(pre_detect == predict_label[0]):
                detect_count = detect_count+1
            else:
                detect_count=0
                pre_detect = predict_label[0]
                      
        
            if(predict_label[0] == 'mixer' and detect_count == 3):
                if(lavel_cnt[11] != 0):
                    continue
                lavel_cnt[11] = 1
                data = {'data': {'push':{
                        'imageUrl': "/assets/img/device-detector/push/mixer_detect.png",
			'clickUrl':"/device-detector"
		}},
                'eventName': 'user99999/panel/outlet'}

                url = 'https://fy33dypvtg.execute-api.us-west-1.amazonaws.com/prod/v0/panel'
                req = urllib2.Request(url)
                req.add_header('Content-Type', 'application/json')
                response = urllib2.urlopen(req, json.dumps(data))
                #upload_sensor_data(str)
                
            if(predict_label[0] == 'canopener' and detect_count == 3):
                if(lavel_cnt[6] != 0):
                    continue
                lavel_cnt[6] = 1
                data = {'data': {'push':{
                        'imageUrl': "/assets/img/device-detector/push/canopener_detect.png",
			'clickUrl':"/device-detector"
		}},
                'eventName': 'user99999/panel/outlet'}
                print data
                url = 'https://fy33dypvtg.execute-api.us-west-1.amazonaws.com/prod/v0/panel'
                req = urllib2.Request(url)
                req.add_header('Content-Type', 'application/json')
                response = urllib2.urlopen(req, json.dumps(data))
            if(predict_label[0] == 'toaster' and detect_count == 3):
                if(lavel_cnt[12] != 0):
                    continue
                lavel_cnt[12] = 1
                data = {'data': {'push':{
                        'imageUrl': "/assets/img/device-detector/push/toaster_detect.png",
			'clickUrl':"/device-detector"
		}},
                'eventName': 'user99999/panel/outlet'}
                print data
                url = 'https://fy33dypvtg.execute-api.us-west-1.amazonaws.com/prod/v0/panel'
                req = urllib2.Request(url)
                req.add_header('Content-Type', 'application/json')
                response = urllib2.urlopen(req, json.dumps(data))
                req = urllib2.Request(url)
                req.add_header('Content-Type', 'application/json')
                response = urllib2.urlopen(req, json.dumps(data))
            if(predict_label[0] == 'fan' and detect_count == 3):
                if(lavel_cnt[5] != 0):
                    continue
                lavel_cnt[5] = 1
                data = {'data': {'push':{
                        'imageUrl': "/assets/img/device-detector/push/aircleaner.png",
			'clickUrl':"/aircleaner-install"
		}},
                'eventName': 'user99999/panel/outlet'}
                print data
                url = 'https://fy33dypvtg.execute-api.us-west-1.amazonaws.com/prod/v0/panel'
                req = urllib2.Request(url)
                req.add_header('Content-Type', 'application/json')
                response = urllib2.urlopen(req, json.dumps(data))
                
                
            if((predict_label[0] == 'none')and event == False):
                upload_sensor_data('none')
            elif(detect_count >= 3 and event == False):
                upload_sensor_data(predict_label[0])

        except Exception as e:
            print('err:', e.args)
        time.sleep(0.3)


if __name__ == '__main__':
    global event
    t = Thread(target=power_detector)
    t.start()
    try:
        while 1:
            str = raw_input()
            if str == '1':
                event = True
            elif str == '0':
                event = False
    except KeyboardInterrupt:
            pass

