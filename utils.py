"""
Module with functions
"""

import cv2 as cv

# Settings
import settings
# Debugging flag
DEBUG = settings.DEBUG

# Reading configuration settings
# H_frame = settings.H_frame
# W_frame = settings.W_frame
# Def_cam = settings.Def_Cam




# Show video from source
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
