# -*- coding: utf-8 -*-
"""
TS_gui.py

GUI related elements and Functions from the TranStack code

Created on Thu Sep  9 12:32:51 2021

@author: Willow
"""


import os
import numpy as np
from matplotlib.widgets import Button, TextBox
import ipywidgets as widgets
import platform
import matplotlib.pyplot as plt

import TS_fio
from TS_settings import defaultSubDir, verbose, x_h, x_off, y_off, Filters, stacks, wavelength_range, axMain, figMain, axcolor


def goToFilDir():
    """
    goToFilDir()
    change the working directory to one containing the csv files desired by the user:

    Returns
    -------
    None.

    """
    if(platform.system()=="Windows") :
        import win32gui
        from win32com.shell import shell, shellcon

        mydocs_pidl = shell.SHGetFolderLocation (0, shellcon.CSIDL_PERSONAL, 0, 0)
        pidl, display_name, image_list = shell.SHBrowseForFolder (
          win32gui.GetDesktopWindow (),
          mydocs_pidl,
          "Select a transmission curve file or folder",
          shellcon.BIF_BROWSEINCLUDEFILES,
          None,
          None
        )

        if (pidl, display_name, image_list) == (None, None, None):
          print("Nothing selected, using default")
          directory = os.path.join(os.getcwd(),defaultSubDir)
        else:
          directory = shell.SHGetPathFromIDList (pidl)
    else:
        tries = 5
        directory=""
        while(tries>0 and not os.path.isdir(directory)):
            directory = str(input("enter the directory of the filter curve files"))
        if(not os.path.isdir(directory)):
            directory = os.path.join(os.getcwd(),defaultSubDir)
    print("Switching To ", directory)
    os.chdir(directory)





class Counter(widgets.DOMWidget):
    """
    COUNTER : This class in a linkable iterator
    for tracking the number of a given filter in the stack
    and incrimenting and decrimenting it using linked matplotlib widgets
    """
    value = 0
    def up(self,*args):
        self.value += 1
        update()
    def down(self,*args):
        self.value -= 1 if self.value > 0 else 0
        update()


def update(*args):
    """
    update refreshes the plotted graph to reflect any changes

    Parameters
    ----------
    *args : Event Data
        DISCARDED

    Returns
    -------
    None. - redraws Main canvas

    """
    for stack in stacks:
        stack["line"].set_ydata(TS_fio.recalc(wavelength_range, Filters, stack["coeffs"]))
        stack["line"].set_label(stack["name"].text)
        for ind, button in enumerate(stack["buttons"][::2]):
            button.label.set_text("remove [{}]".format(stack["coeffs"][ind].value))
    axMain.relim()
    axMain.set_ybound(upper=1)
    axMain.autoscale_view()
    axMain.legend()
    figMain.canvas.draw_idle()

def log(*args):
    """
    log()
    sets Y-Scale to logarithmic

    Parameters
    ----------
    *args : Event Data
        DISCARDED

    Returns
    -------
    None. - calls update()

    """
    if verbose:    
        print("setting y to logarithmic")
    axMain.set_yscale('log')
    update()
    return()

def lin(*args):
    """
    lin()
    sets Y-Scale to linear

    Parameters
    ----------
    *args : Event Data
        DISCARDED

    Returns
    -------
    None. - calls update()

    """
    if verbose:    
        print("setting y to linear")
    axMain.set_yscale('linear')
    update()
    return()


def isolateCanvas(event):
    """
    isolateCanvas()
    returns the in group and out group of canvases assosciated with the event
    i.e. identifies the originating canvas for an event so that the corresponding stack can be deleted/updated/saved/etc.. (interacted with uniquely) 
    
    Parameters
    ----------
    event : EVENT
        an event originating from a user interaction on one of the matplotlib windows

    Returns
    -------
    MyStack : LIST 
        the ID for the canvas that originated the event
    otherStacks : LIST
        all stacks not assosciated with the event

    """
    def oncanvas(stack):
        return(event.canvas==stack["fig"].canvas)
    def offcanvas(stack):
        return(event.canvas!=stack["fig"].canvas)
    try:
        myStack = list(filter(oncanvas,stacks))[0]
        otherStacks = list(filter(oncanvas,stacks))
    except():
        print("MAJOR ERROR: This button is not connected to a stack canvas \n I thought this an unreachable state and therefore will not attempt to advise!\n")
        return(-1)    
    return(myStack,otherStacks)

def Saveline(event):
    """
    Saveline()
    Saves the line data as a csv named according to the stack name
    
    TODO - add check if file exists and request overwrite permission


    Parameters
    ----------
    event : EVENT
        an event that triggers the save to file of a stack

    Returns
    -------
    None. - saved stack to file

    """
    myStack,otherStacks = isolateCanvas(event)
    name = myStack["name"]
    if verbose:print("Saving csv data for {}".format(name.text))

    data = np.transpose(myStack["line"].get_data())

    np.savetxt("{}.csv".format(name.text),data,delimiter=',',newline='\n',header='wavelength,transmission')

    return()

def Remstack(event):
    """
    Remstack()
    deletes the line and gui for the stack.

    Parameters
    ----------
    event : EVENT
        an event that triggers the deletion of a stack

    Returns
    -------
    None. - closes a window

    """
    myStack, otherStacks = isolateCanvas(event)
    name = myStack["name"]
    if verbose:print("User Requested Close Stack:  {}".format(name.text))
    plt.close(myStack["fig"])
    myStack["line"].remove()
    del(myStack)
    update()
    return()


def addStack(*args):    
    """
    addStack

    adds a new line to the plot and opens the associated GUI

    Parameters
    ---------- 
    *args : Event Data
        DISCARDED
        
        
    Returns
    -------
    None. - adds a line to main fig and opens a new stack gui

    """
    numStack = len(stacks)
    stacks.append({})
    stacks[numStack] = {"buttons":[]}
    stacks[numStack].update({"coeffs":[Counter() for _ in Filters]})

    stackfig, stackax = plt.subplots()
    plt.axis("off")
    plt.subplots_adjust(bottom=0.2)
    initial_text = "stack {}".format(numStack)

    taxbox = plt.axes([0.1, 0.85, 0.6, 0.075])
    stacks[numStack].update({"name":TextBox(taxbox, 'Name', initial=initial_text)})
    axButSav=plt.axes([0.7, 0.85, 0.1, 0.075], facecolor=axcolor)
    stacks[numStack].update({"saver":Button(axButSav, label="SAVE", image=None, color='0.85', hovercolor='0.95')})

    axButRem=plt.axes([0.85, 0.85, 0.1, 0.075], facecolor=axcolor)
    stacks[numStack].update({"rem":Button(axButRem, label="DEL", image=None, color='0.85', hovercolor='0.95')})

    stacks[numStack]["rem"].on_clicked(Remstack)
    stacks[numStack]["saver"].on_clicked(Saveline)
    stacks[numStack]["name"].on_submit(update)

    stacks[numStack].update({"fig":stackfig,"ax":stackax})

    y_h = (0.85 - y_off * 2)/len(Filters) 
    
    for ind, Filter in enumerate(Filters):
        #axTxt = plt.axes([x_off, y_off + 0.05*(1+ind), 0.08, 0.03],facecolor=axcolor)
        #stacks[numStack]["text"].append(axTxt.text("{}".format(Filter)))
        axButMin=plt.axes([x_off, y_off + y_h*(ind), 0.09, 0.03], facecolor=axcolor)
        axButPlus=plt.axes([x_off + x_h, y_off + y_h*(ind), 0.06, 0.03], facecolor=axcolor)
        stacks[numStack]["buttons"].append(Button(axButMin, label="remove [0]", image=None, color='0.85', hovercolor='0.95'))
        stacks[numStack]["buttons"][-1].label.set_x(0.05)
        stacks[numStack]["buttons"][-1].label.set_horizontalalignment('left')
        stacks[numStack]["buttons"].append(Button(axButPlus, label="add  {}".format(Filter), image=None, color='0.85', hovercolor='0.95'))
        stacks[numStack]["buttons"][-1].label.set_x(0.2)
        stacks[numStack]["buttons"][-1].label.set_horizontalalignment('left')
        if verbose:
            print("\n buttons assigned for stack {}, itteration: {} \n {}".format(len(stacks),ind,Filter))

    line, = axMain.plot(wavelength_range,TS_fio.recalc(wavelength_range,Filters,stacks[numStack]["coeffs"]),label=stacks[numStack]["name"].text)
    stacks[numStack].update({"line":line})

    for ind, button in enumerate(stacks[numStack]["buttons"]):
        i=int(np.floor(ind/2))
        if (ind/2)%1==0:
            button.on_clicked(stacks[numStack]["coeffs"][i].down)
        else:
            button.on_clicked(stacks[numStack]["coeffs"][i].up)
