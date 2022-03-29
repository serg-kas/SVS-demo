"""
Module with functions
"""
# Necessary modules
import cv2 as cv
import numpy as np
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
        # Put FPS on the frame and show it
        cv.putText(frame, str(fps), (7, 70), font, 3, (100, 255, 0), 3, cv.LINE_AA)
        cv.imshow(SOURCE, frame)
        #
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    capture.release()
    cv.destroyAllWindows()


# Show video from source 4 cameras
def show_from_source_2x2(Cam_list, W=1200, H=800):

    # Template 2x2
    w = int(W/2)
    h = int(H/2)

    SOURCE_list = [cam['RTSP'] for cam in Cam_list]
    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]

    while True:
        frame_list = []
        for cap in capture_list:
            isTrue, frame = cap.read()
            frame = cv.resize(frame, (w, h), interpolation=cv.INTER_AREA)
            frame_list.append(frame)

        # Preparing full frame
        row1 = np.concatenate((frame_list[0], frame_list[1]), axis=1)
        row2 = np.concatenate((frame_list[2], frame_list[3]), axis=1)
        frame = np.concatenate((row1, row2), axis=0)
        cv.imshow('View4', frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()


# Show video from source 16 cameras
def show_from_source_4x4(Cam_list, W=1200, H=800):
    # Template 4x4
    w = int(W/4)
    h = int(H/4)

    SOURCE_list = [cam['RTSP_sub'] for cam in Cam_list]
    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]
    #
    black_frame = np.zeros((h, w, 3), dtype=np.uint8)
    #
    while True:
        frame_list = []
        for idx, cap in enumerate(capture_list):
            isTrue, frame = cap.read()
            if isTrue:
                frame = cv.resize(frame, (w, h), interpolation=cv.INTER_AREA)
            else:
                # set frame as black frame
                frame = black_frame
                # RTSP errors handling
                cap.release()
                del capture_list[idx]
                capture_list.insert(idx, cv.VideoCapture(SOURCE_list[idx]))
            frame_list.append(frame)
        # if we don't have enough Active cameras
        for _ in range(16-len(frame_list)):
            frame_list.append(black_frame)
        # Preparing full frame
        row1 = np.concatenate((frame_list[0], frame_list[1], frame_list[2], frame_list[3]), axis=1)
        row2 = np.concatenate((frame_list[4], frame_list[5], frame_list[6], frame_list[7]), axis=1)
        row3 = np.concatenate((frame_list[8], frame_list[9], frame_list[10], frame_list[11]), axis=1)
        row4 = np.concatenate((frame_list[12], frame_list[13], frame_list[14], frame_list[15]), axis=1)
        full_frame = np.concatenate((row1, row2, row3, row4), axis=0)
        cv.imshow('View4x4', full_frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()
