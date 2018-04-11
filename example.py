from cwt_learner.wavelet_feature_engineering import CWT_learner
from signal_data_base import SignalDB

if __name__ == "__main__":
    sdb = SignalDB('JLego', path='./sample_data/')
    training_data = sdb.get_labeleddata()
    cwt_learn = CWT_learner(signal_indices = [0,1,2,3])
    for ld in training_data:
        labels = [label.split(' ')[0] for label in ld.labels]
        labels = [label.split(' ')[0] for label in ld.labels]
        cwt_learn.add_training_data(ld.signal_bundle.signals,labels)

    cwt_learn.train()
    print cwt_learn.test(training_data[8].signal_bundle.signals)