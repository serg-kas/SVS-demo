#
# Helper functions module
#

import cv2 as cv
import numpy as np
import tkinter as tk  # used for get screen resolution
import os

import settings

# Verbose and Debug options
VERBOSE = settings.VERBOSE
DEBUG = settings.DEBUG


# A few things to do in first
def do_preparing():
    # Reading folder configuration from settings
    model_PATH = settings.model_PATH
    out_PATH = settings.out_PATH
    # Create folders if needed
    if not (model_PATH in os.listdir('.')):
        os.mkdir(model_PATH)
    if not (out_PATH in os.listdir('.')):
        os.mkdir(out_PATH)


# Loading cameras configurations from settings
def get_cam_list():
    Cam_list = []
    Def_cam = None
    for cam in settings.Cameras:
        if cam['Is_active']:
            if cam['Cam_name'] == settings.Def_cam_name:
                Def_cam = cam  # default camera assignment
                if VERBOSE:
                    print('Default camera: {}'.format(Def_cam['Cam_name']))
            else:
                Cam_list.append(cam)
    # Insert Def_cam in first place
    assert Def_cam is not None, 'Must have Def_cam assigned'
    Cam_list.insert(0, Def_cam)
    if VERBOSE:
        print('Loaded active cameras: {}'.format(len(Cam_list)))
    return Cam_list


# Parsing operation mode from text
def get_operation_mode(Operation_mode_string):
    Operation_mode = None
    if VERBOSE:
        print('Trying to resolve Operation mode from string: {}'.format(Operation_mode_string))
    for mode in settings.Operation_modes:
        # Try to find Mode_name in settings
        if mode['Mode_name'] == Operation_mode_string:
            Operation_mode = mode  # set operation mode
            N_cols, N_rows = settings.Def_cols, settings.Def_rows
            # Return founded operation mode with default cols and rows from settings
            return Operation_mode, N_cols, N_rows
        # Try to parse operation mode
        if mode['Mode_name'][:7].lower() == Operation_mode_string[:7].lower():
            Operation_mode = mode  # set operation mode
            # Parsing cols and rows from string
            string_to_parse = Operation_mode_string[7:].lower()
            if (len(string_to_parse) < 3) or ('x' not in string_to_parse):
                # Return founded operation mode with default cols and rows from settings
                N_cols, N_rows = settings.Def_cols, settings.Def_rows
                return Operation_mode, N_cols, N_rows
            idx_x = string_to_parse.index('x')
            try:
                N_cols = int(string_to_parse[:idx_x])
            except ValueError:
                print('Impossible to use "{}" as N_cols, using defaults from settings'.format(string_to_parse[:idx_x]))
                # Return founded operation mode with default cols and rows from settings
                N_cols, N_rows = settings.Def_cols, settings.Def_rows
                return Operation_mode, N_cols, N_rows
            try:
                N_rows = int(string_to_parse[idx_x+1:])
            except ValueError:
                print('Impossible to use "{}" as N_rows, using defaults from settings'.format(string_to_parse[idx_x:]))
                # Return founded operation mode with default cols and rows from settings
                N_cols, N_rows = settings.Def_cols, settings.Def_rows
                return Operation_mode, N_cols, N_rows
            if DEBUG:
                print('Parsed: Mode_name={}, N_cols={}, N_rows={}'.format(mode['Mode_name'], N_cols, N_rows))
            # Return founded operation mode with parsed cols and rows
            return Operation_mode, N_cols, N_rows
    assert Operation_mode is not None, 'Operation_mode not found'


# Get screen resolution info
def get_screen_resolution():
    # TODO: is it possible to get screen resolution from opencv?
    root = tk.Tk()
    W = root.winfo_screenwidth()
    H = root.winfo_screenheight()
    if DEBUG:
        print('Screen resolution: ({},{})'.format(W, H))
    # TODO: What is the minimum acceptable screen resolution that can be allowed?
    if W < 1024 or H < 768:
        W = settings.Def_W
        H = settings.Def_H
    return W, H


# Get optimal font scale
def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
        textSize = cv.getTextSize(text, fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=scale/10, thickness=3)
        new_width = textSize[0][0]
        if new_width <= width:
            return scale/10
    return 1


# Concatenation list of arrays
def concat_from_list(frame_list, N_cols, N_rows):
    row_list = []
    for r in range(N_rows):
        row_list.append(np.concatenate(frame_list[N_cols * r: N_cols * (r + 1)], axis=1))
    return np.concatenate(row_list, axis=0)


# Motion detection with two frames
def md_diff(frame1, frame2):
    diff = cv.absdiff(frame1, frame2)
    diff = diff.astype(np.uint8, copy=False)
    gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=3)
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return contours


# Get some frames from buffer
def get_frames_from_buff(buffer, point, frames_to_return):
    if point > frames_to_return:
        # print(point, buffer[point-frames_to_return:point].shape)
        return buffer[point - frames_to_return:point]
    else:
        N_buff = settings.N_buff
        # print(point, buffer[N_buff-frames_to_return+point:].shape, buffer[:point].shape)
        return np.concatenate([buffer[N_buff - frames_to_return + point:], buffer[:point]], axis=0)

