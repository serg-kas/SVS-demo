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
def show_from_source_fps(Camera, W=1280, H=800):
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


# Show video from C*R cameras
def show_from_source_cxr(Cam_list, W=1280, H=800, N_cols=2, N_rows=2):
    # Preparing template
    w, h = int(W / N_cols), int(H / N_rows)
    N_cells = int(N_cols * N_rows)
    assert N_cells > 0, 'Template must be at least 1 cell'

    if N_cells > 4:
        SOURCE_list = [cam['RTSP_sub'] for cam in Cam_list]
    else:
        SOURCE_list = [cam['RTSP'] for cam in Cam_list]
    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]
    black_frame = np.zeros((h, w, 3), dtype=np.uint8)

    frame_list_prev = [black_frame for _ in range(len(capture_list))]
    error_count_list = [0 for _ in range(len(capture_list))]
    N_errors = settings.N_errors_to_reset

    font = cv.FONT_HERSHEY_SIMPLEX  # font to display connecting status
    fontScale = 0.9  # TODO: Get optimal font scale and text position

    Window_name = 'View ' + str(N_cols) + ' x ' + str(N_rows)

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
        # If we don't have enough Active cameras for all cells
        for _ in range(N_cells - len(frame_list)):
            frame_list.append(black_frame)
        # Preparing full frame
        row_list = []
        for r in range(N_rows):
            row_list.append(np.concatenate([frame_list[N_cols * r + c] for c in range(N_cols)], axis=1))
        full_frame = np.concatenate(row_list, axis=0)
        cv.imshow(Window_name, full_frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()


