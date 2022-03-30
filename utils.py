"""
Helper functions module
"""
# Necessary modules
# import cv2 as cv
# import numpy as np
import tkinter as tk    # for screen resolution info
# import time
#
import settings         # settings
# Debug flag
DEBUG = settings.DEBUG


# Loading Active cameras configurations from settings
def get_cam_list():
    Cam_list = []
    Def_cam = None
    for cam in settings.Cameras:
        if cam['Active']:
            if cam['Cam_name'] == settings.Def_cam_name:
                Def_cam = cam  # default camera assignment
                if DEBUG:
                    print('Default camera is: {}'.format(Def_cam['Cam_name']))
            else:
                Cam_list.append(cam)

    assert Def_cam is not None, 'Must have Def_cam assigned'
    # Insert Def_cam in first place
    Cam_list.insert(0, Def_cam)
    return Cam_list


# Reading operation mode from settings
def get_operation_mode(Operation_mode_name):
    Operation_mode = None
    for mode in settings.Operation_modes:
        if mode['Mode_name'] == Operation_mode_name:
            Operation_mode = mode  # operation mode assignment
    assert Operation_mode is not None, 'Operation_mode not found'
    return Operation_mode


# Get screen resolution info
# TODO: is it possible to get screen resolution from opencv ?
def get_screen_resolution():
    root = tk.Tk()
    W = root.winfo_screenwidth()
    H = root.winfo_screenheight()
    return W, H






