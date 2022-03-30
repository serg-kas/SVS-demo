"""
Main function module
"""
# Necessary modules
import cv2 as cv
import numpy as np
import time
#
import settings         # settings
import utils            # helper functions
# Debug flag
DEBUG = settings.DEBUG


# Show video from source with calculating FPS
# TODO: Resize frame in accordance with SOURCE shape?
def show_from_source(Camera, W=1200, H=800):
    capture = cv.VideoCapture(Camera['RTSP'])
    # Source size
    capture_width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
    capture_height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
    if DEBUG:
        print('Source camera resolution: ({}, {})'.format(capture_width, capture_height))

    Window_name = Camera['Cam_name'] + ': ' + Camera['RTSP']

    # Calculate FPS after N_frames
    N_frames = 50
    frames_count = 0
    fps = 'Calculating fps...'
    font = cv.FONT_HERSHEY_SIMPLEX  # font to display FPS

    prev_time = time.time()  # record the time when we processed last frame

    while True:
        isTrue, frame = capture.read()
        #
        if frames_count == N_frames-1:
            new_time = time.time()  # time when we finish processing N_frames
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
        cv.imshow(Window_name, frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    capture.release()
    cv.destroyAllWindows()


# Show video from 4 cameras
def show_from_source_2x2(Cam_list, W=1200, H=800):
    # Template 2x2
    w = int(W/2)
    h = int(H/2)

    SOURCE_list = [cam['RTSP'] for cam in Cam_list]
    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]
    black_frame = np.zeros((h, w, 3), dtype=np.uint8)

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
        # If we don't have enough Active cameras
        for _ in range(4-len(frame_list)):
            frame_list.append(black_frame)
        # Preparing full frame
        row1 = np.concatenate((frame_list[0], frame_list[1]), axis=1)
        row2 = np.concatenate((frame_list[2], frame_list[3]), axis=1)
        full_frame = np.concatenate((row1, row2), axis=0)
        cv.imshow('View 2x2', full_frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()


# Show video from 16 cameras
def show_from_source_4x4(Cam_list, W=1200, H=800):
    # Template 4x4
    w = int(W/4)
    h = int(H/4)

    SOURCE_list = [cam['RTSP_sub'] for cam in Cam_list]
    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]
    black_frame = np.zeros((h, w, 3), dtype=np.uint8)
    frame_list_prev = [black_frame for _ in range(len(capture_list))]
    error_count_list = [0 for _ in range(len(capture_list))]
    N_errors = settings.N_errors_to_reset

    font = cv.FONT_HERSHEY_SIMPLEX  # font to display connecting status
    fontScale = 0.9  # TODO: Get optimal font scale and text position

    while True:
        frame_list = []
        for idx, cap in enumerate(capture_list):
            isTrue, frame = cap.read()
            if isTrue:
                frame = cv.resize(frame, (w, h), interpolation=cv.INTER_AREA)
                if DEBUG:
                    if error_count_list[idx] >= 1:
                        print('Successfully get frame from cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
                error_count_list[idx] = 0  # reset error count
            else:
                # Inkrement error count
                error_count_list[idx] += 1
                # Get previous frame
                frame = frame_list_prev[idx]
                # If this is first error put text on the frame
                if error_count_list[idx] == 1:
                    cv.putText(frame, 'Connecting...', (30, 40), font, fontScale, (100, 255, 0), 2, cv.LINE_AA)
                # RTSP errors handling after N_error times
                if error_count_list[idx] >= N_errors:
                    cap.release()
                    del capture_list[idx]
                    capture_list.insert(idx, cv.VideoCapture(SOURCE_list[idx]))
                    if DEBUG:
                        print('Reconnected cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
            frame_list.append(frame)

        # Copying current frame_list
        frame_list_prev = frame_list
        # If we don't have enough Active cameras
        for _ in range(16-len(frame_list)):
            frame_list.append(black_frame)
        # Preparing full frame
        row1 = np.concatenate((frame_list[0], frame_list[1], frame_list[2], frame_list[3]), axis=1)
        row2 = np.concatenate((frame_list[4], frame_list[5], frame_list[6], frame_list[7]), axis=1)
        row3 = np.concatenate((frame_list[8], frame_list[9], frame_list[10], frame_list[11]), axis=1)
        row4 = np.concatenate((frame_list[12], frame_list[13], frame_list[14], frame_list[15]), axis=1)
        full_frame = np.concatenate((row1, row2, row3, row4), axis=0)
        cv.imshow('View 4x4', full_frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()


# Show video from 25 cameras TEST
def show_from_source_5x5_test(Cam_list, W=1200, H=800):
    # Template 5x5
    w = int(W/5)
    h = int(H/5)

    SOURCE_list = [cam['RTSP_sub'] for cam in Cam_list]
    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]
    black_frame = np.zeros((h, w, 3), dtype=np.uint8)
    frame_list_prev = [black_frame for _ in range(len(capture_list))]
    error_count_list = [0 for _ in range(len(capture_list))]
    N_errors = settings.N_errors_to_reset

    font = cv.FONT_HERSHEY_SIMPLEX  # font to display connecting status
    fontScale = 0.9  # TODO: Get optimal font scale and text position

    while True:
        frame_list = []
        for idx, cap in enumerate(capture_list):
            isTrue, frame = cap.read()
            if isTrue:
                frame = cv.resize(frame, (w, h), interpolation=cv.INTER_AREA)
                if DEBUG:
                    if error_count_list[idx] >= 1:
                        print('Successfully get frame from cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
                error_count_list[idx] = 0  # reset error count
            else:
                # Inkrement error count
                error_count_list[idx] += 1
                # Get previous frame
                frame = frame_list_prev[idx]
                # If this is first error put text on the frame
                if error_count_list[idx] == 1:
                    cv.putText(frame, 'Connecting...', (30, 40), font, fontScale, (100, 255, 0), 2, cv.LINE_AA)
                # RTSP errors handling after N_error times
                if error_count_list[idx] >= N_errors:
                    cap.release()
                    del capture_list[idx]
                    capture_list.insert(idx, cv.VideoCapture(SOURCE_list[idx]))
                    if DEBUG:
                        print('Reconnected cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
            frame_list.append(frame)

        # Copying current frame_list
        frame_list_prev = frame_list
        # If we don't have enough Active cameras
        for _ in range(25-len(frame_list)):
            frame_list.append(black_frame)
        # Preparing full frame
        row1 = np.concatenate((frame_list[0], frame_list[1], frame_list[2], frame_list[3], frame_list[4]), axis=1)
        row2 = np.concatenate((frame_list[5], frame_list[6], frame_list[7], frame_list[8], frame_list[9]), axis=1)
        row3 = np.concatenate((frame_list[10], frame_list[11], frame_list[12], frame_list[13], frame_list[14]), axis=1)
        row4 = np.concatenate((frame_list[15], frame_list[16], frame_list[17], frame_list[18], frame_list[19]), axis=1)
        row5 = np.concatenate((frame_list[20], frame_list[21], frame_list[22], frame_list[23], frame_list[24]), axis=1)
        full_frame = np.concatenate((row1, row2, row3, row4, row5), axis=0)
        cv.imshow('View 5x5', full_frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()


# Show video from 36 cameras TEST
def show_from_source_6x6_test(Cam_list, W=1200, H=800):
    # Template 6x6
    w = int(W/6)
    h = int(H/6)

    SOURCE_list = [cam['RTSP_sub'] for cam in Cam_list]
    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]
    black_frame = np.zeros((h, w, 3), dtype=np.uint8)
    frame_list_prev = [black_frame for _ in range(len(capture_list))]
    error_count_list = [0 for _ in range(len(capture_list))]
    N_errors = settings.N_errors_to_reset

    font = cv.FONT_HERSHEY_SIMPLEX  # font to display connecting status
    fontScale = 0.9  # TODO: Get optimal font scale and text position

    while True:
        frame_list = []
        for idx, cap in enumerate(capture_list):
            isTrue, frame = cap.read()
            if isTrue:
                frame = cv.resize(frame, (w, h), interpolation=cv.INTER_AREA)
                if DEBUG:
                    if error_count_list[idx] >= 1:
                        print('Successfully get frame from cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
                error_count_list[idx] = 0  # reset error count
            else:
                # Inkrement error count
                error_count_list[idx] += 1
                # Get previous frame
                frame = frame_list_prev[idx]
                # If this is first error put text on the frame
                if error_count_list[idx] == 1:
                    cv.putText(frame, 'Connecting...', (30, 40), font, fontScale, (100, 255, 0), 2, cv.LINE_AA)
                # RTSP errors handling after N_error times
                if error_count_list[idx] >= N_errors:
                    cap.release()
                    del capture_list[idx]
                    capture_list.insert(idx, cv.VideoCapture(SOURCE_list[idx]))
                    if DEBUG:
                        print('Reconnected cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
            frame_list.append(frame)

        # Copying current frame_list
        frame_list_prev = frame_list
        # If we don't have enough Active cameras
        for _ in range(36-len(frame_list)):
            frame_list.append(black_frame)
        # Preparing full frame
        row1 = np.concatenate((frame_list[0], frame_list[1], frame_list[2],
                               frame_list[3], frame_list[4], frame_list[5]), axis=1)
        row2 = np.concatenate((frame_list[6], frame_list[7], frame_list[8],
                               frame_list[9], frame_list[10], frame_list[11]), axis=1)
        row3 = np.concatenate((frame_list[12], frame_list[13], frame_list[14],
                               frame_list[15], frame_list[16], frame_list[17]), axis=1)
        row4 = np.concatenate((frame_list[18], frame_list[19], frame_list[20],
                               frame_list[21], frame_list[22], frame_list[23]), axis=1)
        row5 = np.concatenate((frame_list[24], frame_list[25], frame_list[26],
                               frame_list[27], frame_list[28], frame_list[29]), axis=1)
        row6 = np.concatenate((frame_list[30], frame_list[31], frame_list[32],
                               frame_list[33], frame_list[34], frame_list[35]), axis=1)
        full_frame = np.concatenate((row1, row2, row3, row4, row5, row6), axis=0)
        cv.imshow('View 6x6', full_frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()
