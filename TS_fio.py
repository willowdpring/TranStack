# -*- coding: utf-8 -*-
"""
TS_fio.py

File I/O and transmission curve functions for TranStack

Created on Thu Sep  9 12:39:13 2021

@author: Willow
"""

import os
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import wget
from TS_settings import verbose




"""
Optical Curve generates an interpolator from a csv file of wavelength transimission values
"""
def optical_curve(file):
    data = pd.read_csv(file, delimiter=',')
    data.columns = data.columns.str.strip()
    try:
        wavey = [col for col in data.columns if("wave" in col.lower()) ]
        wavelength = (data[wavey[0]])
    except:
        print("\n\n __ERROR__ \n Wavelength Data not found for file: {} \n please check data headings".format(file))
        return(-1)
    try:
        transmission = abs(data["transmission"])
    except:
        print("\n\n __ERROR__ \n Transmission Data not found for file: {} \n please check data headings".format(file))
        return(-1)
    if max(wavelength)>100:
        wavelength=wavelength/1000
        if verbose:
            print("Wavelength data in File {} appears to be in nm (max(w)>10), upscaling ... ".format(file))
    if max(transmission)>1:
        transmission=transmission/100
        if verbose:
            print("The transmission data in File {} appears to be in percent, downscaling ... ".format(file))
    f2 = interp1d(wavelength, transmission, kind='cubic',bounds_error=False,fill_value=0.0001)
    if verbose:
        print("interpolation generated for {}".format(file))
    return f2


def csvFromXl(xlfile):
    name = xlfile.split(".")[-2]
    if verbose:
        print("file name : {}".format(name))
    if os.path.exists(os.path.join(name,".csv")):
        if verbose:
            print("{}.csv exists".format(name))
        pass
    else:
        csvfile = open("{}.csv".format(name), 'w+', encoding='utf-8')
        pd.read_excel(xlfile).to_csv(csvfile, encoding='utf-8')
        #struct = csvdat
        #struct
        csvfile.close()
        if verbose:
            print("{}.csv file created".format(name))
    return("{}.csv".format(name))

"""
Add Curve form file adds an interpolated transmission curve for the file (generated by optival curve) to the dictionary of filters
"""
def add_curve_from_file(file,Filters,wavelength_range):

    name = file.split('.')[0]
    nameST = "{}".format(name)
    if verbose:
        print("\n Found Filter {} \n at {}".format(nameST,file))

    if file.endswith(".xlsx"):
        file = csvFromXl(file)
        if verbose:
            print("found EXCEL file checking for csv")

    func = optical_curve(file)
    if func != -1:
        Filters.update({nameST:func(wavelength_range)})
    return()


"""add_curve_from_URL - NOT IN USE """
def add_curve_from_url(url):
    if type(url)!=str:
        print("getURL expects a string, got a {}".format(type(url)))
        return(-1)
    else:
        try:
            file = wget.download(url)
        except:
           print("wget download failed please check URL")
           return(-1)
        if file.endswith(".xls") or file.endswith(".csv"):
            return(add_curve_from_file(file))
        else:
            print("File is not a recognised type")
            return(-1)
    pd.read_excel()

"""
recalc - recalculates the transmission of the whole stack based on the counters assigned to each filter
"""
def recalc(WR, Filters, Coeffs):
    Trans = np.ones_like(WR)
    if len(Filters)==len(Coeffs):
        for ind, Filter in enumerate(Filters):
            Trans=Trans*(Filters[Filter]**Coeffs[ind].value)
    return(Trans)