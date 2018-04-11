import numpy as np

__author__ = 'Guru Subramani'
__doc__ = "A datastructure to hold signals with labeled data. SignalBundle combines both signals and timestamps into" \
          "a signal-bundle. LabeledData combines the signal-bundles with their labels over time."

class SignalBundle:
    def __init__(self,signals,timestamps,name = 'None'):
        self.name = name
        if type(signals[0]) != type([]):
            signals = [signal.tolist() for signal in signals]
        if type(timestamps) != type([]):
            timestamps = timestamps.tolist()
        self.signals = signals
        self.timestamps = timestamps
    def signal_len(self):
        return len(self.timestamps)
    def clip(self,startId,endId):
        self.signals = [signal[startId:-endId] for signal in self.signals]
        self.timestamps = self.timestamps[startId:-endId]



class LabeledData:

    def __init__(self, signal_bundle,label = ""):
        self.signal_bundle = signal_bundle
        self.labels = [label] * self.signal_bundle.signal_len()

    def label_data(self,indices,label):
        for index in indices:
            self.labels[index] = label






