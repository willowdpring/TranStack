# -*- coding: utf-8 -*-
"""
TranStack.py 

A tool for stacking optical transmission curves of multiple surfaces

Created on Fri Sep  3 10:22:41 2021

@author: Willow

"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import TS_fio, TS_gui
from TS_settings import verbose, wavelength_min, wavelength_max, axcolor, wavelength_range, transmission, Filters, stacks, figMain, axMain


####    MAIN    ####
if __name__ == "__main__":
        
    TS_gui.goToFilDir()
    directory = os.getcwd()
    
    os.chdir(directory)
    for filename in os.listdir(directory):
        if filename.endswith(".csv") or filename.endswith(".xlsx"):
            TS_fio.add_curve_from_file(filename,Filters,wavelength_range)
    
    
    if len(Filters)>1:
        axMain.set_yscale('log')
        axMain.grid(which='both')
    
        axButStack=plt.axes([0.78, 0.94, 0.18, 0.03], facecolor=axcolor)
        butStack = Button(axButStack, label="Add Filter Stack", image=None, color='0.85', hovercolor='0.95')
        axButLog=plt.axes([0.78, 0.9, 0.06, 0.03], facecolor=axcolor)
        butLog = Button(axButLog, label="Log", image=None, color='0.85', hovercolor='0.95')
        axButLin=plt.axes([0.86, 0.9, 0.07, 0.03], facecolor=axcolor)
        butLin = Button(axButLin, label="Linear", image=None, color='0.85', hovercolor='0.95')
    
        butLog.on_clicked(TS_gui.log)
        butLin.on_clicked(TS_gui.lin)
    
        TS_gui.addStack()
        butStack.on_clicked(TS_gui.addStack)
    
        axMain.legend()
    
    
    elif len(Filters) == 1:
        plt.ion()
        axMain.set_yscale('log')
        axMain.grid(which='both')
        key = list(Filters)[0]
        if verbose:
            print("Plotting data for {}\n\n WR:{} \n\n TRANS:{}".format(key,wavelength_range,Filters[key]))
        axMain.plot(wavelength_range,Filters[key])
        axMain.relim()
        axMain.set_ybound(upper=1)
        axMain.autoscale_view()
        figMain.canvas.draw_idle()
    
    
    else:
        print("no filters found in {}".format(directory))