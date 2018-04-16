from cwt_learner.wavelet_feature_engineering import CWT_learner
from signal_data_base import SignalDB
import matplotlib.pyplot as plt
from plot_generator import plotResult_colorbars


"""
Usage: Create a CWT_learner

Add training data using add_training_data member function.
Call train member function to train with the training data. 
Test with arbitrary data. "
"""


if __name__ == "__main__":
    sdb = SignalDB('JLego', path='./sample_data/')
    training_data_ = sdb.get_labeleddata()
    cwt_learn = CWT_learner(signal_indices = [0,1,2,3])
    training_data = training_data_[0:8]
    testing_data = training_data_[8:10]
    for ld in training_data:
        labels = [label.split(' ')[0] for label in ld.labels]
        labels = [label.split(' ')[0] for label in ld.labels]
        cwt_learn.add_training_data(ld.signal_bundle.signals,labels)

    cwt_learn.train()
    labels = cwt_learn.fit(testing_data[0].signal_bundle.signals)

    plt.figure()

    ax = plt.subplot(2, 1, 1)
    plt.title("Test Example")
    plt.plot(testing_data[0].signal_bundle.signals[0])
    ax.get_yaxis().set_visible(False)

    plt.subplot(2, 1, 2)
    plotResult_colorbars(labels, range(len(labels)))

    plt.show()

