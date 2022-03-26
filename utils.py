"""
Module with functions
"""
# Necessary modules
import cv2 as cv
import tkinter as tk    # for screen resolution info
import time
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
def show_from_source(SOURCE, W=1200, H=800):
    capture = cv.VideoCapture(SOURCE)

    # Рассчитаем коэффициент для изменения размера
    capture_width = capture.get(cv.CAP_PROP_FRAME_WIDTH)    # float
    capture_height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)  # float
    if DEBUG:
        print('Camera resolution: {},{}'.format(int(capture_width), int(capture_height)))
    # if width > height:
    #     scale_frame = IMG_SIZE / width
    # else:
    #     scale_frame = IMG_SIZE / height
    # # и новые размеры фрейма
    # new_width = int(width * scale_frame)
    # new_height = int(height * scale_frame)

    while True:
        isTrue, frame = capture.read()
        frame = cv.resize(frame, (W, H), interpolation=cv.INTER_AREA)
        cv.imshow(SOURCE, frame)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    capture.release()
    cv.destroyAllWindows()


# Show video from source with calculating FPS
def show_from_source_fps(SOURCE, W=1200, H=800):
    capture = cv.VideoCapture(SOURCE)

    # to calculate FPS after N_frames
    N_frames = 50
    frames_count = 0
    # font which we will be using to display FPS
    font = cv.FONT_HERSHEY_SIMPLEX
    # FPS
    fps = 0
    # record the time when we processed last frame
    prev_time = time.time()

    while True:
        isTrue, frame = capture.read()
        #
        if frames_count == N_frames-1:
            print(frames_count)
            # time when we finish processing N_frames
            new_time = time.time()
            # Calculating the fps
            fps = 1 / (new_time - prev_time) * N_frames
            fps = int(fps)
            prev_time = new_time
            frames_count = 0
        frames_count += 1
        #
        frame = cv.resize(frame, (W, H), interpolation=cv.INTER_AREA)
        # Put FPS on the frame
        cv.putText(frame, str(fps), (7, 70), font, 3, (100, 255, 0), 3, cv.LINE_AA)
        #
        cv.imshow(SOURCE, frame)
        #
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    capture.release()
    cv.destroyAllWindows()


# Show video from source 4 cameras
# TODO: MAKE 4 CAMERAS TEMPLATE
def show_from_source_4(Cam_list, W=1200, H=800):
    SOURCE = Cam_list[0]['RTSP']
    capture = cv.VideoCapture(SOURCE)


    while True:
        isTrue, frame = capture.read()
        frame = cv.resize(frame, (W, H), interpolation=cv.INTER_AREA)
        cv.imshow(SOURCE, frame)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    capture.release()
    cv.destroyAllWindows()