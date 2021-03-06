# Recognizing Events and Patterns in Signals
This python library allows detecting patterns in *n-dimensional
time domain signals*.

Colors represent different labels over time.

![Training Data](https://github.com/gsubramani/SignalRecognition/blob/master/training_data_fig.png "Training Data")

![Test Example](https://github.com/gsubramani/SignalRecognition/blob/master/test_example_fig.png "Test Example")


The library uses the Continuous Wavelet Transform, similar to time-frequency 
 analysis such as the fourier transform, to transform an *n* dimensional
time domain signal into *k\*n* dimension signals or *k\*n* features per
time sample. Then it trains a classifier using the continuous wavelet transform
features. 

Please cite our work!

[ G. Subramani, D. Rakita, H. Wang, J. Black, M. Zinn and M. Gleicher, 
"Recognizing actions during tactile manipulations through force sensing," 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), Vancouver, BC, 2017, pp. 4386-4393. doi: 10.1109/IROS.2017.8206302
](https://ieeexplore.ieee.org/abstract/document/8206302/)

# Requirements
## For the package cwt_learner
1. Numpy
1. scikit-learn - optional if you are using your own classifier

## For the Example ([Example.ipynb](https://github.com/gsubramani/SignalRecognition/blob/master/example.ipynb))
You will also need: 
1. Pydblite
1. Matplotlib

# How it works
Time series signals are transformed into the time-frequency domain using
the Continuous Wavelet Transform. This turns a n-channel signal into a k\*n channel 
signal where k is the number of scales\frequencies of interest, providing
 k\*n features at every sample time. The k\*n features are used to describe
the local behavior of the signal. These descriptions along with the class label are used
to train a ML classifier.


# Details of API
`cwt_learner` is the main software package.

`wavelet_feature_engineering.py` provides the interface to
apply machine learning classifiers to the transformed data. The 
default ML classifier is a `sklearn.neural_network. MLPClassifier`
but this can be changed to a different classifier. 

`wavelet_feature_transform.py` transforms the time domain multi-channel
 signal into the continuous wavelet transform. This function 
interfaces with the `wavelets.py` library. Additional transformations
 such as extracting magnitude and phase is possible. The default wavelet
 is the *morelet* wavelet but other wavelets are also possible. 




