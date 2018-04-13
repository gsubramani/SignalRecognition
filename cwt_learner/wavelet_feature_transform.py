from wavelets import Morlet,DOG,DOG1,Haar,HaarW
import numpy as np
from warnings import warn

__author__ = 'Guru Subramani'
"""Some auxilary methods to interface with the wavelet library"""


class WaveletFeatureTransform:
    """Computes the complex wavelet transform using the Morlet wavelet. Allows specifying mulitple signals."""
    def __init__(self,signals,timestamps,scaling = "log",wavelet = "morlet"):
        """inputs -> signals -- array of signals, timestamps -- specify timestamps
        scaling specifies either "log" or "linear" """
        self.wavelet = wavelet
        self.scaling = scaling
        self.signals = []
        self.timestamps = []
        self.cwt_complex = []
        self.timestamps = self._padArrayPower2ND([timestamps])[0] #since we want to index into [timestamps]array
        #sometimes some signals are empty, filling them with zeros
        for id, signal in enumerate(signals):
            if len(signal) == 0:
                signals[id] = np.zeros(len(signals[0]))
        self.signals, padsizel, padsizer = self._padArrayPower2ND(signals)
        self._findWaveletTrasform_ND_struct(wavelet = self.wavelet)
        self._clip(padsizel, padsizer)

    def feature_matrix(self,magfunc = lambda x : np.log(np.abs(x)),phasefunc = lambda x:np.angle(x),\
                        clip = None,features = None,signal_indices = None,phase = "Yes",mag = "Yes"):
        """Creates feature matrix for machine learning, appends features in order, sig0.mag sig0.phase sig1.mag ...
        param magfunc -> specify a function to calculate absolute values
        features -> can be a list or tuple, if it is a tuple of 2 then (start, end) indices if it is list then it uses
        those indices
        signal_indices -> specify the indices of the signals or interest
        clip - > tuple of 2, used to specify the start and end of the example length
        phase and mag can be set to Yes or No, No will omit this in the transform"""
        n_sig,n_examp,n_feat = np.shape(self.cwt_complex)
        if clip == None:
            start_examp = 0
            end_examp = n_examp
        else: start_examp,end_examp = clip
        if features == None:
            start_feat = 0
            end_feat = n_feat
            feat_indices = range(start_feat,end_feat)
        elif type(features) == type([]):
            feat_indices = features
        else:
            start_feat, end_feat  = features
            feat_indices = range(start_feat, end_feat)
            if end_feat >n_feat:
                end_feat = n_feat
                warn("specified length of features exceeds available freatures")
        n_feat = len(feat_indices)
        if signal_indices == None:
            signal_indices = range(n_sig)
        n_sig = len(signal_indices)
        if phase == "Yes" and mag == "Yes":
            featmat = np.ones((n_examp,n_feat*n_sig*2))
        elif phase == "No" or mag == "No":
            featmat = np.ones((n_examp, n_feat * n_sig))
        if phase == "No" and mag == "No": raise NameError('phase and mag cant both be No')
        for iexamp in range(start_examp,end_examp):
            for id_s, isig in enumerate(signal_indices):
                for idx_f,ifeat in enumerate(feat_indices):
                    if phase == "Yes" and mag == "Yes":
                        featmat[iexamp][n_feat * id_s + idx_f] = magfunc(self.cwt_complex[isig][iexamp][ifeat])
                        featmat[iexamp][n_feat*n_sig  + n_feat*id_s+ idx_f] = phasefunc(self.cwt_complex[isig][iexamp][ifeat])
                    if phase == "No" and mag == "Yes":
                        featmat[iexamp][n_feat * id_s + idx_f] = magfunc(self.cwt_complex[isig][iexamp][ifeat])
                    if phase == "Yes" and mag == "No":
                        featmat[iexamp][n_feat * id_s + idx_f] = phasefunc(self.cwt_complex[isig][iexamp][ifeat])

        return featmat

    def get_dims(self):
        n_sig, n_examp, n_feat = np.shape(self.cwt_complex)
        return n_sig,n_examp,n_feat

    def getn_feat(self):
        n_sig, n_examp, n_feat = np.shape(self.cwt_complex)
        return n_feat

    def getn_examp(self):
        n_sig, n_examp, n_feat = np.shape(self.cwt_complex)
        return n_examp

    def getn_sig(self):
        n_sig, n_examp, n_feat = np.shape(self.cwt_complex)
        return n_sig

    def _findWaveletTrasform_ND_struct(self,wavelet = "morlet"):
        """returns the wavelet transform of ND signals as a struct
        signals and timestamps need to be the same length and powers of 2"""

        for signal in self.signals:
            maxscale = 1
            if wavelet == "morlet":
                # print "using morlet"
                cw = Morlet(signal, maxscale, scaling=self.scaling)
            elif wavelet == "DOG":
                # print "using DOG"
                cw = DOG(signal, maxscale, scaling=self.scaling)
            elif wavelet == "DOG1":
                # print "using DOG1"
                cw = DOG1(signal, maxscale, scaling=self.scaling)
            elif wavelet == "Haar":
                cw = Haar(signal, maxscale, scaling=self.scaling)
            elif wavelet == "HaarW":
                cw = HaarW(signal, maxscale, scaling=self.scaling)
            else:
                cw = Morlet(signal, maxscale, scaling=self.scaling)
            cwdata = np.transpose(cw.getdata())
            # arrangement: cwdata [time[scales]]
            self.cwt_complex.append(cwdata)

    def _magArr(self):
        """returns magnitude of cwt"""
        return np.abs(self.cwt_complex).tolist()
    def _phaseArr(self):
        """returns phase of cwt"""
        return np.angle(self.cwt_complex).tolist()

    def _clip(self,startId,endId):
        """clips cwt start and end indices"""
        self.cwt_complex = [cwt[startId:-endId] for cwt in self.cwt_complex]
        self.signals = [signal[startId:-endId] for signal in self.signals]
        self.timestamps = self.timestamps[startId:-endId]

    def _padArrayPower2ND(self,array):
        """    Pads arrays to 2^n length so the fft algorithm used for cwt works
        array -> an array of signals
        """
        arraySize = len(array[0])
        i = 1
        while ((arraySize >> i) > 0):
            i = i + 1
        rest = ((1 << i) - len(array[0]))

        padsizel = rest % 2 + rest / 2
        padsizer = rest / 2
        array = np.pad(array, [(0, 0), (padsizel, padsizer)], 'edge')
        return array, padsizel, padsizer

if __name__ == "__main__":
    time = [ii / 100.0 for ii in range(1000)]
    sig = np.random.rand(1000)
    mf = WaveletFeatureTransform([sig, sig * 10], time, scaling="log",wavelet="morlet")
    print np.shape(mf.feature_matrix(signal_indices=[0], magfunc=lambda x: np.log(np.abs(x)), mag="Yes",
                      phase="No"))

