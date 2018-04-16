# Recognizing Events and Signal Shapes in Time Domain Signals
This python library allows detecting patterns in *ndimensional
time domain signals*
along the *time domain axis*.

The library uses the Continuous Wavelet Transform, similar to time frequency 
 analysis such as the fourier transform, to transform an *n* dimensional
time domain signal into *k\*n* dimension signals or *k\*n* features per
time sample. Then it trains a classifier using the continuous wavelet transform
features. 

Please cite our work!

###[Recognizing actions during tactile manipulations through force sensing](https://ieeexplore.ieee.org/abstract/document/8206302/)

# Requirements
## For the recognition package CWT_LEARNER
1. Numpy
1. scikit-learn - optional if you are using your own classifier

## For the Example
You will also need: 
1. Pydblite
1. Matplotlib





