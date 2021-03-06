#!/usr/bin/env python2
# -*- coding: utf-8 -*-from sklearn.externals import joblib


from array import array
import cPickle as pickle
from scipy.stats import ks_2samp
import numpy as np
import pandas as pd
import datetime
import math
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
import numpy as np
import math
import pickle


from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


trainFraction = 0.7
classifier = MLPClassifier(activation='tanh', alpha=1e-05, batch_size='auto',
                           beta_1=0.9, beta_2=0.999, early_stopping=False,
                           epsilon=1e-08, hidden_layer_sizes=(25, 20), learning_rate='adaptive',
                           learning_rate_init=0.001, max_iter=200, momentum=0.9,
                           nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
                           solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,
                           warm_start=False)


print 'Loading signal data file...'
sig_data1 = pd.read_pickle('../data/signal_data.p')
sig_data = pd.DataFrame(data=sig_data1)
print 'Loading background data file...'
bkg_data1 = pd.read_pickle('../data/background_data.p')
bkg_data = pd.DataFrame(data=bkg_data1)
#
cutIndex = int(trainFraction * len(sig_data))
#
print ' '

print "For features at index ",i," and ",j," :"
sigTrain = sig_data.iloc[0:cutIndex,[i,j]]
sigTest = sig_data.iloc[cutIndex: ,[i,j]]
bgTrain = bkg_data.iloc[0:cutIndex,[i,j]]
bgTest = bkg_data.iloc[cutIndex: ,[i,j]]

# Create the scaler to preprocess the data
scaler = StandardScaler(copy=True, with_mean=True, with_std=True).fit(sigTrain)

# transform the training sameple
sigTrain = scaler.transform(sigTrain)
# do the same to the test data
sigTest = scaler.transform(sigTest)
# do the same to the test data
bgTrain = scaler.transform(bgTrain)
# do the same to the test data
bgTest = scaler.transform(bgTest)

print 'Learning...'
train = np.append(sigTrain, bgTrain, axis=0)

target = [-1] * len(sigTrain) + [1] * len(bgTrain)
classifier.fit(train, target)

joblib.dump(classifier, 'classifier_jindal.pkl')
joblib.dump(scaler, 'scaler_jindal.pkl')
print 'Classifier saved to file'
