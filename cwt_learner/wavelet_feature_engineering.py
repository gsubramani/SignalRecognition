from wavelet_feature_transform import WaveletFeatureTransform
from signal_data_base import SignalDB
import numpy as np
from scipy import signal
from sklearn.neural_network import MLPClassifier
from labelSelectedData import SignalBundle, LabeledData

__author__ = "Guru Subramani"
__doc__ = "This python module allows creating a cwt based learning algorithm to detect events in signals. The algorithm" \
          "is classifier agnostic so you can - if you wish chose a classifier. The default classifier is a Neural Net. " \
          "Useage: Create a CWT_learner" \
          "Add training data using add_training_data member function." \
          "Call train member function to train with the training data. " \
          "Test with arbitrary data. "

class CWT_learner:
    def __init__(self,inital_traing_set = None,signal_indices = None):
        if inital_traing_set == None:
            self.training_data_sets = []
        else:
            self.training_data_sets = inital_traing_set
        self.use_signals = signal_indices
        self.wavelet = "morelet"
        self.signal_indices = signal_indices

    def get_examples_with_weights(self,ld_array,with_window = "Off",signal_indices = None,wavelet = "morlet",verbs_only = False):
        X = []
        Y = []
        for ld in ld_array:

            labels = ld.labels
            mf = WaveletFeatureTransform(ld.signal_bundle.signals,ld.signal_bundle.timestamps,scaling = "log",wavelet=wavelet)
            examples = mf.feature_matrix(magfunc = lambda x : np.log(np.abs(x)),phase = "Yes",mag = "Yes",features=(0,10),signal_indices = signal_indices)
            print np.shape(examples)
            if with_window == "On": window = np.int32(np.floor(signal.gaussian(len(examples),len(examples)/3)*100))
            else: window = len(examples)*[1];
            for example,weight,label in zip(examples,window,labels):
                for ii in range(weight): X.append(example)
                for ii in range(weight): Y.append(label)
        # if verbs_only == True:
        #     Y = [y.split('_')[0] for y in Y]
        #     Y = [y.split(' ')[0] for y in Y]

        return (X,Y)

    def train(self,classifier = MLPClassifier()):
        (trainX,trainY) = self.get_examples_with_weights(self.training_data_sets,with_window = "Off",signal_indices = self.use_signals,wavelet = self.wavelet ,verbs_only = False)
        # print trainX
        self.classifier = classifier.fit(trainX,trainY)

    def test(self,signals,timestamps = None):
        if timestamps == None:
            timestamps = range(0,len(signals[0]))
        sb = SignalBundle(signals,timestamps)
        ld = LabeledData(signal_bundle=sb)
        (testX,testY) = self.get_examples_with_weights([ld],with_window = "Off",signal_indices = self.use_signals,wavelet = self.wavelet ,verbs_only = False)
        predict_labels = self.classifier.predict(testX)
        return predict_labels

    def add_training_data(self,signals,labels,timestamps = None):
        __doc__ = "This allows the user to add training data one at a time. signals is the set of signals you would like" \
                  "to use for the algorithm. You can also choose later on if you would like to leave out a few signals." \
                  "using signal indices. This helps mix and match without having to put in the training data. "
        if timestamps == None:
            timestamps = range(0,len(signals[0]))

        sb = SignalBundle(signals, timestamps)

        ld = LabeledData(signal_bundle=sb)
        ld.labels = labels
        self.training_data_sets.append(ld)





