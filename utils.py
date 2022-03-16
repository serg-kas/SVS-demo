"""
Module with functions
"""

# Settings module
import settings

# Debugging flag
DEBUG = settings.DEBUG

# Importing
import cv2 as cv


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
