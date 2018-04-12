""" Recognizing events in 1d signals
This python module allows creating a cwt based learning algorithm to detect events in signals. The algorithm
is classifier agnostic so you can - if you wish choose a classifier. The default classifier is a Neural Net.
See the example.py file for usage.
"""
__author__ = "Guru Subramani"

from wavelet_feature_transform import WaveletFeatureTransform
from signal_data_base import SignalDB
import numpy as np
from scipy import signal
from sklearn.neural_network import MLPClassifier
from labelSelectedData import SignalBundle, LabeledData



class CWT_learner:
    """
    CWT classifier

    Attributes
    ----------
    signal_indices: list of int
        The signal indices that should be included during training. For example, if an nd signal is provided,
        you could choose to only use [0,3,4] signals of the [0,1,2,3...n] signals.
    wavelet: str
        The wavelet used during training

    """
    signal_indices = [0]
    wavelet = 'morelet'

    def __init__(self,initial_training_set = None,signal_indices = None):
        '''
        :param initial_training_set:
            The initial training set is a list of LabeledData objects

        :param signal_indices:
            The indices used to train the model
        '''
        if initial_training_set == None:
            self.training_data_sets = []
        else:
            self.training_data_sets = initial_training_set
        self.signal_indices = signal_indices


    def get_examples_with_weights(self,ld_array,with_window = "Off",signal_indices = None,wavelet = "morlet"):
        """ applies the CWT to the data. It returns the transform. This function converts nd time domain signal into
        the CWT table.

        :param ld_array:
        :param with_window:
        :param signal_indices:
        :param wavelet:
        :return:
        """
        X = []
        Y = []
        for ld in ld_array:

            labels = ld.labels
            mf = WaveletFeatureTransform(ld.signal_bundle.signals,ld.signal_bundle.timestamps,scaling = "log",
                                         wavelet=wavelet)
            examples = mf.feature_matrix(magfunc = lambda x : np.log(np.abs(x)),phase = "Yes",
                                         mag = "Yes",features=(0,10),signal_indices = signal_indices)
            #print np.shape(examples)
            if with_window == "On": window = np.int32(np.floor(signal.gaussian(len(examples),len(examples)/3)*100))
            else: window = len(examples)*[1];
            for example,weight,label in zip(examples,window,labels):
                for ii in range(weight): X.append(example)
                for ii in range(weight): Y.append(label)

        return X,Y

    def train(self,classifier = MLPClassifier()):
        """
        Trains the learning algorithm using the added data.
        :param classifier: Any sklearn classifier can be provided.
        :return: None
        """
        (trainX,trainY) = self.get_examples_with_weights(self.training_data_sets,with_window = "Off",
                                                         signal_indices = self.signal_indices
                                                         ,wavelet = self.wavelet)
        # print trainX
        self.classifier = classifier.fit(trainX,trainY)

    def fit(self,signals,timestamps = None):
        """
        Fits new data to the model providing labels over time.
        :param signals: A list of numpy arrays or lists of same dimension. Data that needs to be tested on.
        :param timestamps: Time samples. Note that training and fitting the model should have the same sample time!
        :return: list The predicted labels over time.
        """
        if timestamps == None:
            timestamps = range(0,len(signals[0]))
        sb = SignalBundle(signals,timestamps)
        ld = LabeledData(signal_bundle=sb)
        (testX,testY) = self.get_examples_with_weights([ld],with_window = "Off",
                                                       signal_indices = self.signal_indices,wavelet = self.wavelet)
        predict_labels = self.classifier.predict(testX)
        return predict_labels

    def add_training_data(self,signals,labels,timestamps = None):
        """This allows the user to add training data one at a time.
        :param signals: A list of signals. This is a list of numpy 1d arrays. The dimensions of all arrays are the same
        :param labels: A list str corresponding to the labels at each sample. len(labels) == len(signals[0])
        :param timestamps: can provide timestamps if they are available, otherwise replaces them with [0,1,2,...]
        :return: None
        """
        if timestamps == None:
            timestamps = range(0,len(signals[0]))

        sb = SignalBundle(signals, timestamps)

        ld = LabeledData(signal_bundle=sb)
        ld.labels = labels
        self.training_data_sets.append(ld)





