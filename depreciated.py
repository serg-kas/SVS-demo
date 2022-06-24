#
# Depreciated functions
#

import cv2 as cv
import numpy as np
import time

import settings
import utils

# Verbose and Debug options
VERBOSE = settings.VERBOSE
DEBUG = settings.DEBUG


# Show video from C*R cameras in uniform template with calculating fps for each cell (cam) separately
def show_uniform_fps_cells(Cam_list, W=1280, H=800, N_cols=2, N_rows=2, FPS_calc=False):
    """
    There is no need to measure fps for each cell.
    We process all sources sequentially one after another
    and spend some total time to form a complete frame.
    It is enough to measure the speed of formation of a full
    frame - this will be the effective fps value.
    """
    # Preparing template
    N_cells = int(N_cols * N_rows)
    assert N_cells > 0, 'Uniform template must be at least 1 cell in size'
    w, h = int(W / N_cols), int(H / N_rows)

    if N_cells > 4:
        SOURCE_list = [cam['RTSP_sub'] for cam in Cam_list]
    else:
        SOURCE_list = [cam['RTSP'] for cam in Cam_list]
    SOURCE_list = SOURCE_list[:N_cells]  # we don't need more cameras than we have cells

    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]

    black_frame = np.zeros((h, w, 3), dtype=np.uint8)

    frame_list_prev = [black_frame for _ in range(len(capture_list))]
    error_count_list = [0 for _ in range(len(capture_list))]
    N_errors = settings.N_errors_to_reset

    font = cv.FONT_HERSHEY_SIMPLEX  # font to display connecting status
    # fontScale = 0.9
    fontScale = utils.get_optimal_font_scale('Connecting...', int(w * 3 / 4))

    Window_name = 'View ' + str(N_cols) + ' x ' + str(N_rows)

    # Calculate FPS after N_frames for each cell (cam)
    N_frames = 50
    frames_count_list = [0 for _ in range(len(capture_list))]
    fps_list = ['Calculating FPS...' for _ in range(len(capture_list))]
    font_fps = cv.FONT_HERSHEY_SIMPLEX  # font to display FPS
    # fontScale_fps = 2
    fontScale_fps = utils.get_optimal_font_scale('Calculating FPS...', w)
    prev_time_list = [time.time() for _ in range(len(capture_list))]  # record the time when we processed last frame

    while True:
        frame_list = []
        for idx, cap in enumerate(capture_list):
            isTrue, frame = cap.read()
            if isTrue:
                frame = cv.resize(frame, (w, h), interpolation=cv.INTER_AREA)
                #
                if FPS_calc:
                    if frames_count_list[idx] == N_frames - 1:
                        new_time = time.time()  # time when we finish processing N_frames
                        # Calculating the fps
                        fps_list[idx] = 1 / (new_time - prev_time_list[idx]) * N_frames
                        fps_list[idx] = int(fps_list[idx])
                        prev_time_list[idx] = new_time
                        frames_count_list[idx] = 0
                    frames_count_list[idx] += 1
                cv.putText(frame, str(fps_list[idx]), (7, 35), font_fps, fontScale_fps, (100, 255, 0), 2, cv.LINE_AA)
                #
                if DEBUG:
                    if error_count_list[idx] > 0:
                        print('Successfully get frame from cap[{}] after {} errors'.format(idx, error_count_list[idx]))
                error_count_list[idx] = 0  # reset error count
                #
            else:
                # Increment error count
                error_count_list[idx] += 1
                # Get previous frame
                frame = frame_list_prev[idx].copy()
                # If this is first error put text on the frame
                if error_count_list[idx] == 1:
                    cv.putText(frame, 'Connecting...', (30, 40), font, fontScale, (100, 255, 0), 2, cv.LINE_AA)
                # RTSP errors handling after N_error times
                if error_count_list[idx] >= N_errors:
                    cap.release()
                    del capture_list[idx]
                    capture_list.insert(idx, cv.VideoCapture(SOURCE_list[idx]))
                    if DEBUG:
                        print('Reconnected cap[{}] after {} errors'.format(idx, error_count_list[idx]))
            frame_list.append(frame)

        # Save current frame_list
        frame_list_prev = frame_list
        # If we don't have enough cameras for all cells
        for _ in range(N_cells - len(frame_list)):
            frame_list.append(black_frame)
        # Preparing full frame and showing it
        full_frame = utils.concat_from_list(frame_list, N_cols, N_rows)
        cv.imshow(Window_name, full_frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()


# Show video from C*R cameras in uniform template with the possibility of calculation full screen FPS
def show_uniform(Cam_list, W=1280, H=800, N_cols=2, N_rows=2, FPS_calc=False):
    """
    There is no frame buffer in this function (only one previous frame is stored)
    """
    # Preparing template
    N_cells = int(N_cols * N_rows)
    assert N_cells > 0, 'Uniform template must be at least 1 cell in size'
    w, h = int(W / N_cols), int(H / N_rows)

    if N_cells > 4:
        SOURCE_list = [cam['RTSP_sub'] for cam in Cam_list]
    else:
        SOURCE_list = [cam['RTSP'] for cam in Cam_list]
    SOURCE_list = SOURCE_list[:N_cells]  # we don't need more cameras than we have cells

    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]

    black_frame = np.zeros((h, w, 3), dtype=np.uint8)

    frame_list_prev = [black_frame for _ in range(len(capture_list))]
    error_count_list = [0 for _ in range(len(capture_list))]
    N_errors = settings.N_errors_to_reset

    font = cv.FONT_HERSHEY_SIMPLEX  # font to display connecting status
    # fontScale = 0.9
    fontScale = utils.get_optimal_font_scale('Connecting...', int(w * 3 / 4))

    Window_name = 'View ' + str(N_cols) + ' x ' + str(N_rows)

    # Calculate FPS after N_frames
    if FPS_calc:
        N_frames = 50
        frames_count = 0
        fps = 'Calculating FPS...'
        font_fps = cv.FONT_HERSHEY_SIMPLEX  # font to display FPS
        # fontScale_fps = 3
        fontScale_fps = utils.get_optimal_font_scale(fps, int(W / 2))
        prev_time = time.time()  # record the time when we processed last frame

    while True:
        frame_list = []
        for idx, cap in enumerate(capture_list):
            isTrue, frame = cap.read()
            if isTrue:
                frame = cv.resize(frame, (w, h), interpolation=cv.INTER_AREA)
                if DEBUG:
                    if error_count_list[idx] > 0:
                        print('Successfully get frame from cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
                error_count_list[idx] = 0  # reset error count
            else:
                # Increment error count
                error_count_list[idx] += 1
                # Get previous frame
                frame = frame_list_prev[idx].copy()
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

        # Save current frame_list
        frame_list_prev = frame_list
        # If we don't have enough cameras for all cells
        for _ in range(N_cells - len(frame_list)):
            frame_list.append(black_frame)
        # Preparing full frame and showing it
        full_frame = utils.concat_from_list(frame_list, N_cols, N_rows)
        #
        if FPS_calc:
            if frames_count == N_frames - 1:
                new_time = time.time()  # time when we finish processing N_frames
                # Calculating the fps
                fps = 1 / (new_time - prev_time) * N_frames
                fps = int(fps)
                prev_time = new_time
                frames_count = 0
            frames_count += 1
            # Put FPS on the frame and show it
            cv.putText(full_frame, str(fps), (7, 70), font_fps, fontScale_fps, (100, 255, 0), 3, cv.LINE_AA)
        #
        cv.imshow(Window_name, full_frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()


# Show video from C*R cameras in a uniform template with buffering and the ability to calculate full-screen FPS
def show_uniform_buff(Cam_list, W=1280, H=800, N_cols=2, N_rows=2, FPS_calc=False):
    """
    Ready function with frame buffer (numpy array).
    Next comes the implementation of the MD detector
    """
    # Preparing template
    N_cells = int(N_cols * N_rows)
    assert N_cells > 0, 'Uniform template must be at least 1 cell in size'
    w, h = int(W / N_cols), int(H / N_rows)

    if N_cells > 4:
        SOURCE_list = [cam['RTSP_sub'] for cam in Cam_list]
    else:
        SOURCE_list = [cam['RTSP'] for cam in Cam_list]
    SOURCE_list = SOURCE_list[:N_cells]  # we don't need more cameras than we have cells

    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]
    N_captures = len(capture_list)

    N_buff = settings.N_buff  # buffer size for each capture
    buff_array = np.zeros((N_captures, N_buff, h, w, 3), dtype=np.uint8)
    buff_point = np.zeros(N_captures, dtype=np.uint8)

    black_frame = np.zeros((h, w, 3), dtype=np.uint8)
    black_frame_list = [black_frame for _ in range(N_cells - len(capture_list))]

    error_count = np.zeros(N_captures, dtype=np.uint8)
    N_errors = settings.N_errors_to_reset

    font = cv.FONT_HERSHEY_SIMPLEX  # font to display connecting status
    # fontScale = 0.9
    fontScale = utils.get_optimal_font_scale('Connecting...', int(w * 3 / 4))

    Window_name = 'View ' + str(N_cols) + ' x ' + str(N_rows)

    # Calculate FPS after N_frames
    if FPS_calc:
        N_frames = 50
        frames_count = 0
        fps = 'Calculating FPS...'
        font_fps = cv.FONT_HERSHEY_SIMPLEX  # font to display FPS
        # fontScale_fps = 3
        fontScale_fps = utils.get_optimal_font_scale(fps, int(W / 2))
        prev_time = time.time()  # record the time when we processed last frame

    while True:
        #
        for idx, cap in enumerate(capture_list):

            p = buff_point[idx]  # current pointer (buffer index)

            isTrue, frame = cap.read()
            if isTrue:
                frame = cv.resize(frame, (w, h), interpolation=cv.INTER_AREA)
                #
                if p == N_buff - 1:
                    p = 0
                else:
                    p += 1
                buff_array[idx][p] = frame.copy()  # save frame by current index (pointer)
                buff_point[idx] = p  # save pointer
                #
                if DEBUG:
                    if error_count[idx] > 0:
                        print('Successfully get frame from cap[{0}] after {1} errors'.format(idx, error_count[idx]))
                error_count[idx] = 0  # reset error count
            else:
                # Increment error count
                error_count[idx] += 1
                # If this is first error put text on the frame
                if error_count[idx] == 1:
                    # Get previous frame
                    frame = buff_array[idx][p].copy()
                    cv.putText(frame, 'Connecting...', (30, 40), font, fontScale, (100, 255, 0), 2, cv.LINE_AA)
                    #
                    if p == N_buff-1:
                        p = 0
                    else:
                        p += 1
                    buff_array[idx][p] = frame.copy()  # save frame by current index (pointer)
                    buff_point[idx] = p  # save pointer
                    #
                # RTSP errors handling after N_error times
                if error_count[idx] >= N_errors:
                    cap.release()
                    del capture_list[idx]
                    capture_list.insert(idx, cv.VideoCapture(SOURCE_list[idx]))
                    if DEBUG:
                        print('Reconnected cap[{0}] after {1} errors'.format(idx, error_count[idx]))
            #
        # Preparing full frame and showing it
        frame_list = [buff_array[idx][buff_point[idx]] for idx in range(N_captures)] + black_frame_list
        full_frame = utils.concat_from_list(frame_list, N_cols, N_rows)
        #
        if FPS_calc:
            if frames_count == N_frames - 1:
                new_time = time.time()  # time when we finish processing N_frames
                # Calculating the fps
                fps = 1 / (new_time - prev_time) * N_frames
                fps = int(fps)
                prev_time = new_time
                frames_count = 0
            frames_count += 1
            # Put FPS on the frame and show it
            cv.putText(full_frame, str(fps), (7, 70), font_fps, fontScale_fps, (100, 255, 0), 3, cv.LINE_AA)
        #
        cv.imshow(Window_name, full_frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()

