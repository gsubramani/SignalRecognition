import hashlib
import pickle
from os.path import join

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RectangleSelector
from pydblite import Base

from cwt_learner.labelSelectedData import LabeledData, SignalBundle

__author__ = "Guru Subramani"
__doc__ = "Provides a way to manage signals in a database. This is a convenient way to store, label and retrieve " \
          "signals. We might need to relabel signals or label over signals. You can add a signal again and it will know" \
          "that that signal has already been added before. "


class SelectData:

    def __init__(self,timestamps,signals,button_names = []):
        self.button_names = button_names
        self.signals = signals
        self.timestamps = timestamps
        self.pick_indices = range(len(timestamps))
        self.button_array = []

    def onclick(self,event):
        self.event = event

    def line_select_callback(self, eclick, erelease):
        """eclick and erelease are the press and release events"""
        self.x1, self.y1 = eclick.xdata, eclick.ydata
        self.x2, self.y2 = erelease.xdata, erelease.ydata

    def close_calback(self):
        plt.close()

    def name_calback(self,event,name):
        print name

    def boxSelect(self):
        fig, current_ax = plt.subplots()

        print len(self.signals)
        for signal in self.signals:
            plt.plot(self.timestamps,signal)

        self.RS = RectangleSelector(current_ax, self.line_select_callback,
                                               drawtype='box', useblit=True,
                                               button=[1, 3],  # don't use middle button
                                               minspanx=5, minspany=5,
                                               spancoords='pixels'
                                               )
        self.RS.set_active(True)


        plt.show()
        examp_indices = self.subsetData(self.x1,self.x2)
        return examp_indices

    def subsetData(self,x1,x2):
        dt = self.timestamps[len(self.timestamps)/2] - self.timestamps[len(self.timestamps)/2 - 1]
        x1_offset = x1 - self.timestamps[0]
        x2_offset = x2 - self.timestamps[0]
        start_idx = np.floor(x1_offset/dt).astype(int)
        end_idx = np.floor(x2_offset/dt).astype(int)
        return range(start_idx,end_idx)


class SignalDB:
    def __init__(self,name,path = './',mode = "open"):
        '''mode can be 'override' '''

        name_sig = name + '_sig.pdl'
        name_sig = join(path, name_sig)
        self.db_sig = Base(name_sig)
        self.db_sig.create('signal_bundle','signals','timestamps','name','labels','md5','sublabel',mode = mode)
        self.db_sig.open()

    def commit(self):
        self.db_sig.commit()

    def tohash(self,data):
        md5 = hashlib.md5(pickle.dumps(data)).hexdigest()
        return md5
    def findld(self,ld):
        md5 = self.tohash(ld.signal_bundle.signals[0])
        recarr = [r for r in (self.db_sig('md5') == md5)]
        if len(recarr) > 1:
            print 'duplicate signal bundles'
        elif len(recarr) == 1:
            r = recarr[0]
            sb = r['signal_bundle']
            labels = r['labels']
            name = r['name']
            ld_out = LabeledData(sb)
            ld_out.labels = labels
            return ld_out
        else:
            print "signal doesn't currently exist"
            return None

    def add_labeleddata(self,ld,overwrite = False):
        md5 = self.tohash(ld.signal_bundle.signals[0])
        recarr = [r for r in (self.db_sig('md5') == md5)]
        if len(recarr) > 1:
            print 'duplicate signal bundles'
        if not recarr:
            self.db_sig.insert(signal_bundle = ld.signal_bundle,\
                               signals = ld.signal_bundle.signals,\
                               timestamps = ld.signal_bundle.timestamps,\
                               name = ld.signal_bundle.name, \
                               labels = ld.labels,\
                               md5 = md5)

        else:
            rec = recarr[0]
            print rec['__id__']
            if overwrite == False:
                for idx, (reclabel,ldlabel) in enumerate(zip(rec['labels'],ld.labels)):
                    if reclabel == '':
                        rec['labels'][idx] = ldlabel
            else:
                for idx, (reclabel,ldlabel) in enumerate(zip(rec['labels'],ld.labels)):
                    if ldlabel != '':
                        rec['labels'][idx] = ldlabel


            # print rec['__id__'],rec['labels']
            self.db_sig.update(rec, labels=rec['labels'])

    def get_labeleddata(self):
        ld_arr = []
        # signal_bundle, timestamps = None, label = "")
        for r in self.db_sig:
            sb = r['signal_bundle']
            labels = r['labels']
            name = r['name']
            ld = LabeledData(sb)
            ld.labels = labels
            ld_arr.append(ld)
        return ld_arr



if __name__ == "__main__":


    sdb = SignalDB('test')

    time = [ii / 100.0 for ii in range(1000)]
    sig = np.random.rand(1000)
    # sig = np.ones(1000)
    # print len(time),len(sig)

    sb = SignalBundle([sig,sig],time)

    sd = SelectData(time,[sig,sig])
    indices = sd.boxSelect()

    ld = LabeledData(sb, time)
    ld.label_data(indices,'hello')

    sdb.add_labeleddata(ld)

    sd = SelectData(time,[sig])
    indices = sd.boxSelect()
    ld2 = LabeledData(sb,time)
    ld2.label_data(indices,'newlabel')

    sdb.add_labeleddata(ld2)


    sdb.commit()

    rec = [r for r in sdb.db_sig]
    print rec[0]['labels']
    print len(rec)

