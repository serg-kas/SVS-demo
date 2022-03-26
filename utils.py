"""
Module with functions
"""
# Necessary modules
import cv2 as cv
import tkinter as tk    # for screen resolution info
import settings         # settings
# Debug flag
DEBUG = settings.DEBUG


# Get screen resolution info
# TODO: is it possible to get screen resolution from opencv ?
def get_screen_resolution():
    root = tk.Tk()
    W = root.winfo_screenwidth()
    H = root.winfo_screenheight()
    return W, H


# Show video from source
# TODO: Resize frame in accordance with SOURCE shape
def show_from_source(SOURCE, W=900, H=500):
    capture = cv.VideoCapture(SOURCE)
    while True:
        isTrue, frame = capture.read()
        #
        frame = cv.resize(frame, (W, H), interpolation=cv.INTER_AREA)
        #
        cv.imshow(SOURCE, frame)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    capture.release()
    cv.destroyAllWindows()
