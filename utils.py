#
# Helper functions module
#
import numpy as np
import tkinter as tk  # being used for get screen resolution
import os
#
import settings

# Debug and  Verbose flags
DEBUG = settings.DEBUG
VERBOSE = settings.VERBOSE


# A few things to do first
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
                if DEBUG:
                    print('Default camera is: {}'.format(Def_cam['Cam_name']))
            else:
                Cam_list.append(cam)

    assert Def_cam is not None, 'Must have Def_cam assigned'
    # Insert Def_cam in first place
    Cam_list.insert(0, Def_cam)
    return Cam_list


# Reading operation mode from settings
def get_operation_mode(Operation_mode_text):
    Operation_mode = None
    # Try to find in settings
    for mode in settings.Operation_modes:
        if mode['Mode_name'] == Operation_mode_text:
            Operation_mode = mode  # operation mode assignment
            N_cols, N_rows = settings.Def_cols, settings.Def_rows
            return Operation_mode, N_cols, N_rows
    # Try to resolve pattern ViewCxR
    if len(Operation_mode_text) >= 6:
        if Operation_mode_text[:4] == 'View':
            #
            Operation_mode = settings.Operation_modes[1]
            try:
                N_cols = int(Operation_mode_text[4])
            except ValueError:
                print('Impossible to use "{}" as N_cols, using defaults from settings'.format(Operation_mode_text[4]))
                # Return mode ViewCxR with defaults N_cols and N_rows
                N_cols, N_rows = settings.Def_cols, settings.Def_rows
                return Operation_mode, N_cols, N_rows
            try:
                N_rows = int(Operation_mode_text[6])
            except ValueError:
                print('Impossible to use "{}" as N_rows, using defaults from settings'.format(Operation_mode_text[6]))
                # Return mode ViewCxR with defaults N_cols and N_rows
                N_cols, N_rows = settings.Def_cols, settings.Def_rows
                return Operation_mode, N_cols, N_rows
            if N_cols > 0 and N_rows > 0:
                # Return mode ViewCxR with parsed N_cols and N_rows
                return Operation_mode, N_cols, N_rows
            else:
                print('Not allowed value(s): N_cols={0}, N_rows={1},'
                      ' using defaults from settings'.format(N_cols, N_rows))
                # Return mode ViewCxR with defaults N_cols and N_rows
                N_cols, N_rows = settings.Def_cols, settings.Def_rows
                return Operation_mode, N_cols, N_rows

    assert Operation_mode is not None, 'Operation_mode not found'
    # return Operation_mode, N_cols, N_rows


# Get screen resolution info
def get_screen_resolution():
    # TODO: is it possible to get screen resolution from opencv?
    root = tk.Tk()
    W = root.winfo_screenwidth()
    H = root.winfo_screenheight()
    # TODO: What is the minimum screen resolution allowed?
    if W < 1024 | H < 768:
        W = settings.Def_W
        H = settings.Def_H
    return W, H


#
# def get_optimal_font_scale(text, width):
#
#     for scale in reversed(range(0, 60, 1)):
#         textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
#         new_width = textSize[0][0]
#         if (new_width <= width):
#             return scale/10
#     return 1
#
# fontScale = 3*(img.shape[1]//6)
# font_size = get_optimal_font_scale(text, fontScale)
# cv2.putText(img, text, org, font, font_size, color, thickness, cv2.LINE_AA)


# Concatenation list of arrays
def concat_from_list(frame_list, N_cols, N_rows):
    row_list = []
    for r in range(N_rows):
        # row_list.append(np.concatenate([frame_list[N_cols * r + c] for c in range(N_cols)], axis=1))
        row_list.append(np.concatenate(frame_list[N_cols * r: N_cols * (r + 1)], axis=1))
    return np.concatenate(row_list, axis=0)
