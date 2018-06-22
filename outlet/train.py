import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.metrics import confusion_matrix

paths = glob.glob('../CurrentData_constant/*')
files = [os.path.basename(p) for p in paths]
labels = list(set([f.split('-')[0] for f in files]))
print(labels)

def get_features(measure_data):
    mean_of_abs = measure_data.abs().mean()[0]
    window = 16
    mean_each_window = [measure_data[n:n+window].mean()[0] for n in range(0, len(measure_data), 10)]
    max_each_window = [measure_data[n:n+window].max()[0] for n in range(0, len(measure_data), 10)]
    min_each_window = [measure_data[n:n+window].min()[0] for n in range(0, len(measure_data), 10)]
    std_of_mean = np.std(mean_each_window)
    std_of_width = np.std([mx - mn for mx, mn in zip(max_each_window, min_each_window)])

    #return(np.array([mean_of_abs, std_of_mean, std_of_width]))
    return(np.array([mean_of_abs, 1]))

train_label = []
train_feature = []

for i, path in enumerate(paths):
    if files[i].split('-')[1].split('.')[0] in ['0'] + [str(s) for s in range(2, 10)]:
        try:
            measure_data = pd.read_csv(path, header=None)[10:-10]
            measure_data = measure_data.astype(np.float)
            train_label.append(files[i].split('-')[0])
            train_feature.append(get_features(measure_data))
        except Exception as e:
            print('err:', files[i], e.args)
train_feature = np.array(train_feature)

clf = RandomForestClassifier(random_state=0, n_estimators=100)
X = train_feature
y = train_label
clf.fit(X, y)
with open('model/clf_v1.pickle', mode='wb') as f:
    pickle.dump(clf, f)
