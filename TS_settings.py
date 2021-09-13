# -*- coding: utf-8 -*-
"""
TS_settings.py

A collection of user editable Globals to controll the behaviour of TranStack Gui amd console log

Created on Thu Sep  9 12:54:58 2021

@author: Willow
"""
import numpy as np
import matplotlib.pyplot as plt

# text outputs detailed logging to console
#"""
verbose = True
"""
verbose = False
#"""

# set default working directory if none chosen by user
defaultSubDir = "ExampleCSVs"


# Spectral range over which to work
wavelength_min = 0.2 # 0.5 um
wavelength_1um = 1
wavelength_max = 1 # 20 um



#graphical settings

axcolor = "lightgoldenrodyellow"

x_off = 0.2
x_h = 0.13

y_off = 0.05




# DO NOT EDIT #
wavelength_range = np.linspace(wavelength_min, wavelength_max, num=int((wavelength_max - wavelength_min) *10000))
transmission = np.ones(len(wavelength_range))
Filters = {}
stacks = []

plt.ion()
figMain, axMain = plt.subplots()
