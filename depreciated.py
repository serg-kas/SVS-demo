#
# Depreciated functions
#
import cv2 as cv
import numpy as np
import time
#
import settings
import utils

# Verbose and Debug options
VERBOSE = settings.VERBOSE
DEBUG = settings.DEBUG


# Show video from C*R cameras in uniform template with calculating fps for each cell (cam) separately
def show_uniform_fps_cells(Cam_list, W=1280, H=800, N_cols=2, N_rows=2, FPS_calc=False):
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
    fontScale = 0.9  # TODO: Get optimal font scale and text position

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
                # Inkrement error count
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