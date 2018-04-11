import matplotlib.pyplot as plt
import matplotlib.cm
from scipy.signal import medfilt
import numpy as np


def splitSignal(array):
    split_indices = []
    labelorder = []
    sizes = []
    previous_element = array[0]
    sizes.append(0)
    labelorder.append(previous_element)
    for element in array:
        if(previous_element == element):
            sizes[-1]  = sizes[-1] + 1
            previous_element = element
        else:
            sizes.append(1)
            labelorder.append(element)
            previous_element = element
    return sizes,labelorder


def plotlabelpositions(array,timestamps):
    sizes,labelorder = splitSignal(array)
    label_indices = []
    start = []
    stop = []
    sum = 0
    for size in sizes:
        label_indices.append(timestamps[sum+size/2])
        start.append(timestamps[sum])
        sum = size + sum
        print sum,len(timestamps)
        stop.append(timestamps[sum-1])

    return label_indices,labelorder,start,stop


def plotResult(testPredict,timestamps,signal,labelsgiven = True,plotmeans = False,showplot = True,ax = None,labelNames = [],legend = False,line = False,medfiltwidth = 101,labelnumfilts= None,actuallabels = None):


    if ax is None:
        ax = plt.gca()
    if len(labelNames) ==0:
        labelNamesSet = set(testPredict)
        labelNames = list(labelNamesSet)


    testPredictIds = [labelNames.index(label) for idx, label in enumerate(testPredict)]
    testPredictIds = medfilt(testPredictIds,medfiltwidth)
    testPredictIds = (testPredictIds.astype(int)).tolist()
    testPredict = [labelNames[id] for id in testPredictIds]

    if labelnumfilts !=None:
        out_testPredict = []
        sizes, labelorder  = splitSignal(testPredict)
        for size,label in zip(sizes,labelorder):
            if size < labelnumfilts[labelNames.index(label)]:
                out_testPredict = out_testPredict + ['']*size
            else: out_testPredict = out_testPredict + [label]*size
        testPredict = out_testPredict
    print splitSignal(testPredict)

    testPredictIds = [labelNames.index(label) for idx, label in enumerate(testPredict)]


    for jj,label in enumerate(labelNames):
        testPredictIds[jj] = jj
    color_map_rgba = matplotlib.cm.ScalarMappable(cmap="Vega20").to_rgba(testPredictIds)

    if labelsgiven == True:
        for label_id in set(testPredictIds):
            if line == False:
                ax.scatter([timestamp for idx, timestamp in enumerate(timestamps) if testPredictIds[idx] == label_id], \
                           [signal_point for idx, signal_point in enumerate(signal) if testPredictIds[idx] == label_id], \
                           c= [color for idx, color in enumerate(color_map_rgba) if testPredictIds[idx] == label_id], lw=0,\
                           label = labelNames[label_id],s = 1)
            else:
                ax.plot([timestamp for idx, timestamp in enumerate(timestamps) if testPredictIds[idx] == label_id], \
                        [id for idx, id in enumerate(testPredictIds) if testPredictIds[idx] == label_id] ,\
                        '.k', label = labelNames[label_id],linewidth = 1, markersize=2,color = 'black')
                # ax.set_yticklabels(labelNames)
                labelNames_plot = [label.split('_')[0] for label in labelNames]
                print labelNames_plot
                labelNames_plot[0] = "unlabelled"
                ax.yaxis.set(ticks=np.arange(0, len(labelNames)), ticklabels=labelNames_plot)
                ax.set_ylim([-0.5,len(labelNames) + 0.25])
                if actuallabels != None:
                    label_indices ,label_order,starts,stops = plotlabelpositions(actuallabels,timestamps)

                    label_order_plot = [label.split('_')[0] for label in label_order]
                    ax.xaxis.set(ticks=label_indices, ticklabels=label_order_plot)
                    for start,stop,label in zip(starts,stops,label_order):
                        color = color_map_rgba[labelNames.index(label)]
                        ax.axvspan(start, stop, alpha=0.2, color=color)
                        ax.axvline(start,linewidth=0.5, color='k')
                        # ax.xaxis.grid(False)
                        ax.yaxis.grid(True)

                        # ax.axvline(start, linewidth=4, color='k')
                # else: ax.xaxis.set(ticks = np.arange(0.5,np.max(timestamps)))


    else: ax.scatter(timestamps, signal, c=testPredict, cmap=plt.cm.RdYlGn, lw=0,s = 1)

    if legend  == True:
        ax.legend()

    return ax


def plotResult_colorbars(testPredict,timestamps,signal,labelsgiven = True,plotmeans = False,showplot = True,ax = None,labelNames = [],legend = False,line = False,medfiltwidth = 101,labelnumfilts= None,actuallabels = None):


    if ax is None:
        ax = plt.gca()
    if len(labelNames) ==0:
        labelNamesSet = set(testPredict)
        labelNames = list(labelNamesSet)


    testPredictIds = [labelNames.index(label) for idx, label in enumerate(testPredict)]
    testPredictIds = medfilt(testPredictIds,medfiltwidth)
    testPredictIds = (testPredictIds.astype(int)).tolist()
    testPredict = [labelNames[id] for id in testPredictIds]

    if labelnumfilts !=None:
        out_testPredict = []
        sizes, labelorder  = splitSignal(testPredict)
        for size,label in zip(sizes,labelorder):
            if size < labelnumfilts[labelNames.index(label)]:
                out_testPredict = out_testPredict + ['']*size
            else: out_testPredict = out_testPredict + [label]*size
        testPredict = out_testPredict
    print splitSignal(testPredict)

    testPredictIds = [labelNames.index(label) for idx, label in enumerate(testPredict)]


    for jj,label in enumerate(labelNames):
        testPredictIds[jj] = jj
    color_map_rgba = matplotlib.cm.ScalarMappable(cmap="RdYlGn").to_rgba(testPredictIds)

    if labelsgiven == True:
        for label_id in set(testPredictIds):
            if line == False:

                ax.set_ylim([-0.5, 0.25])
                if actuallabels != None:
                    label_indices ,label_order,starts,stops = plotlabelpositions(actuallabels,timestamps)

                    label_order_plot = [label.split('_')[0] for label in label_order]
                    ax.xaxis.set(ticks=label_indices, ticklabels=label_order_plot)
                    for start,stop,label in zip(starts,stops,label_order):
                        color = color_map_rgba[labelNames.index(label)]
                        ax.axvspan(start, stop, alpha=0.2, color=color)
                        ax.axvline(start,linewidth=0.5, color='k')
                        # ax.xaxis.grid(False)
                        ax.yaxis.grid(True)
            else:
                ax.plot([timestamp for idx, timestamp in enumerate(timestamps) if testPredictIds[idx] == label_id], \
                        [id for idx, id in enumerate(testPredictIds) if testPredictIds[idx] == label_id] ,\
                        '.k', label = labelNames[label_id],linewidth = 1, markersize=2,color = 'black')
                # ax.set_yticklabels(labelNames)
                labelNames_plot = [label.split('_')[0] for label in labelNames]
                print labelNames_plot
                labelNames_plot[0] = "unlabelled"
                ax.yaxis.set(ticks=np.arange(0, len(labelNames)), ticklabels=labelNames_plot)
                ax.set_ylim([-0.5,len(labelNames) + 0.25])
                if actuallabels != None:
                    label_indices ,label_order,starts,stops = plotlabelpositions(actuallabels,timestamps)

                    label_order_plot = [label.split('_')[0] for label in label_order]
                    ax.xaxis.set(ticks=label_indices, ticklabels=label_order_plot)
                    for start,stop,label in zip(starts,stops,label_order):
                        color = color_map_rgba[labelNames.index(label)]
                        ax.axvspan(start, stop, alpha=0.2, color=color)
                        ax.axvline(start,linewidth=0.5, color='k')
                        # ax.xaxis.grid(False)
                        ax.yaxis.grid(True)




    else: ax.scatter(timestamps, signal, c=testPredict, cmap=plt.cm.RdYlGn, lw=0,s = 1)

    if legend  == True:
        ax.legend()

    return ax
