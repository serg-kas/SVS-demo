#
# Main functions module
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


# Show video from one camera with the possibility of calculation FPS
def show_single(Camera, W=1280, H=800, FPS_calc=False):
    capture = cv.VideoCapture(Camera['RTSP'])
    # Source size
    capture_width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
    capture_height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
    if VERBOSE:
        print('Source camera resolution: ({}, {})'.format(capture_width, capture_height))
    #
    Window_name = Camera['Cam_name'] + ': ' + Camera['RTSP']
    #
    # Calculate FPS after N_frames
    if FPS_calc:
        N_frames = 50
        frames_count = 0
        fps = 'Calculating fps...'
        font = cv.FONT_HERSHEY_SIMPLEX  # font to display FPS
        # fontScale = 3
        fontScale = utils.get_optimal_font_scale(fps, int(W / 2))
        prev_time = time.time()  # record the time when we processed last frame
    #
    while True:
        isTrue, frame = capture.read()
        #
        frame = cv.resize(frame, (W, H), interpolation=cv.INTER_AREA)
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
            cv.putText(frame, str(fps), (7, 70), font, fontScale, (100, 255, 0), 3, cv.LINE_AA)
        #
        cv.imshow(Window_name, frame)
        #
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    capture.release()
    cv.destroyAllWindows()


# Show video from C*R cameras in a uniform template with buffering and the ability to calculate full-screen FPS
def show_uniform_md(Cam_list, W=1280, H=800, N_cols=2, N_rows=2, FPS_calc=False):
    """
    All frames from all cameras are stored in a ring buffer buff_array.
    The vector buff_point contains pointers to the position of the actual frames in the buffer.
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

    # Buffer ring-like for frames and vector for indexes
    N_buff = settings.N_buff  # buffer size for each capture
    buff_array = np.zeros((N_captures, N_buff, h, w, 3), dtype=np.uint8)
    buff_point = np.zeros(N_captures, dtype=np.uint8)

    # Motion detection
    md_enabled_list = [cam['MD_enabled'] for cam in Cam_list]
    md_status = np.zeros(N_captures, dtype=np.uint8)  # motion was detected status

    # For empty frames
    black_frame = np.zeros((h, w, 3), dtype=np.uint8)
    black_frame_list = [black_frame for _ in range(N_cells - N_captures)]

    # Counting successful and errors frames for each capture device
    success_count = np.zeros(N_captures, dtype=np.uint8)
    error_count = np.zeros(N_captures, dtype=np.uint8)
    N_errors = settings.N_errors_to_reset  # how many errors are allowed before doing reset capture device

    #
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

            # If there was motion detected, dropping the last frame (md_frame with depicted bb's)
            if md_status[idx] > 0:
                # p -= 1 if p > 0 else N_buff - 1
                if p > 0:
                    p -= 1
                else:
                    p = N_buff - 1

            isTrue, frame = cap.read()
            if isTrue:
                frame = cv.resize(frame, (w, h), interpolation=cv.INTER_AREA)
                #
                if DEBUG:
                    if error_count[idx] > 0:
                        print('Successfully get frame from cap[{0}] after {1} errors'.format(idx, error_count[idx]))
                #
                error_count[idx] = 0  # reset error count
                if success_count[idx] < N_buff:
                    success_count[idx] += 1

                # Put current frame in buffer
                # p += 1 if p < N_buff - 1 else 0
                if p < N_buff - 1:
                    p += 1
                else:
                    p = 0
                buff_array[idx][p] = frame.copy()  # save frame by current index (pointer)
                buff_point[idx] = p  # save pointer

                # Motion detection
                got_motion = False
                if md_enabled_list[idx] and success_count[idx] > 15:
                    #
                    # Get background and foreground
                    background_array = utils.get_frames_from_buff(buff_array[idx], buff_point[idx], 15)
                    background = np.mean(background_array, axis=0, dtype=np.float32)
                    #
                    foreground_array = utils.get_frames_from_buff(buff_array[idx], buff_point[idx], 5)
                    for i in range(5):
                        foreground_array[i] = foreground_array[i] * (i+1) / 5
                    foreground = np.mean(foreground_array, axis=0, dtype=np.float32)
                    #
                    contours = utils.md_diff(foreground, background)

                    # Frame for visualization bb's on it
                    md_frame = frame.copy()
                    #
                    if len(contours) != 0:
                        # got_motion = True
                        # cv.drawContours(md_frame, contours, -1, (0, 255, 0), 2)
                        for contour in contours:
                            if cv.contourArea(contour) < 700:
                                continue
                            got_motion = True
                            (xc, yc, wc, hc) = cv.boundingRect(contour)
                            cv.rectangle(md_frame, (xc, yc), (xc + wc, yc + hc), (0, 255, 0), 2)

                # Update md_status
                # md_status[idx] += 1 if got_motion else 0
                if got_motion:
                    md_status[idx] += 1
                else:
                    md_status[idx] = 0
                if md_status[idx] > N_buff:
                    md_status[idx] = N_buff

                # Put frame with depicted bb's in buffer
                if got_motion:
                    # p += 1 if p < N_buff - 1 else 0
                    if p < N_buff - 1:
                        p += 1
                    else:
                        p = 0
                    buff_array[idx][p] = md_frame.copy()  # save frame with rectangles by current index (pointer)
                    buff_point[idx] = p
                    #
                    print('idx={}, p={}, md_status={}, success_count={}'.format(idx, p, md_status[idx], success_count[idx]))
                #
            else:
                # Reset the success counter
                success_count[idx] = 0
                # Increment error count
                error_count[idx] += 1
                # If this is first error put text on the frame
                if error_count[idx] == 1:
                    # Get previous frame
                    frame = buff_array[idx][p].copy()
                    cv.putText(frame, 'Connecting...', (30, 40), font, fontScale, (100, 255, 0), 2, cv.LINE_AA)
                    #
                    # p += 1 if p < N_buff - 1 else 0
                    if p < N_buff - 1:
                        p += 1
                    else:
                        p = 0
                    buff_array[idx][p] = frame.copy()  # save frame by current index (pointer)
                    buff_point[idx] = p  # save pointer
                    md_status[idx] = 0
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
        #
        cv.imshow(Window_name, full_frame)
        #
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()


# Show video in custom template Def_cam + some other cams + events/faces lines
def show_custom1(Cam_list, W=1280, H=800, N_cols=2, N_rows=2, Events_line=True, Faces_line=True):
    # Preparing template
    w, h = int(W / N_cols), int(H / N_rows)

    # Lines reserved for events/faces
    Bottom_lines = int(Events_line) + int(Faces_line)
    #
    assert Bottom_lines > 0, 'Must have at least 1 line for events or faces'
    assert N_cols > 1, 'Must have at least 2 columns'
    assert N_rows - Bottom_lines > 0, 'Must have at least 1 row for cameras'
    assert N_cols - (N_rows - Bottom_lines) > 0, 'Must have at least 1 column for other cameras'

    # Def_cam will be the size of all rows except those reserved for event lines
    Def_cam_size = N_rows - Bottom_lines
    #
    Def_cam_w, Def_cam_h = Def_cam_size * w, Def_cam_size * h
    #
    N_places = (N_cols - Def_cam_size) * Def_cam_size + 1  # how many cameras are placed on frame including Def_cam
    #
    SOURCE_list = [Cam_list[0]['RTSP']] + [cam['RTSP_sub'] for cam in Cam_list[1:]]  # Def_cam uses RTSP main stream
    SOURCE_list = SOURCE_list[:N_places]  # we don't need cameras more than we have places

    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]
    N_captures = len(capture_list)

    black_frame = np.zeros((h, w, 3), dtype=np.uint8)
    def_cam_black_frame = np.zeros((Def_cam_h, Def_cam_w, 3), dtype=np.uint8)

    frame_list_prev = [def_cam_black_frame] + [black_frame for _ in range(N_captures - 1)]
    error_count = np.zeros(N_captures, dtype=np.uint8)
    N_errors = settings.N_errors_to_reset

    font = cv.FONT_HERSHEY_SIMPLEX  # font to display connecting status
    # fontScale = 0.9
    fontScale = utils.get_optimal_font_scale('Connecting...', int(w * 3 / 4))

    Window_name = 'Custom View ' + str(N_cols) + ' x ' + str(N_rows)

    while True:
        frame_list = []
        for idx, cap in enumerate(capture_list):
            isTrue, frame = cap.read()
            if isTrue:
                if idx == 0:
                    frame = cv.resize(frame, (Def_cam_w, Def_cam_h), interpolation=cv.INTER_AREA)
                else:
                    frame = cv.resize(frame, (w, h), interpolation=cv.INTER_AREA)
                if DEBUG:
                    if error_count[idx] >= 1:
                        print('Successfully get frame from cap[{0}] after {1} errors'.format(idx, error_count[idx]))
                error_count[idx] = 0  # reset error count
            else:
                # Increment error count
                error_count[idx] += 1
                # Get previous frame
                frame = frame_list_prev[idx].copy()
                # If this is first error put text on the frame
                if error_count[idx] == 1:
                    cv.putText(frame, 'Connecting...', (30, 40), font, fontScale, (100, 255, 0), 2, cv.LINE_AA)
                # RTSP errors handling after N_error times
                if error_count[idx] >= N_errors:
                    cap.release()
                    del capture_list[idx]
                    capture_list.insert(idx, cv.VideoCapture(SOURCE_list[idx]))
                    if DEBUG:
                        print('Reconnected cap[{0}] after {1} errors'.format(idx, error_count[idx]))
            frame_list.append(frame)

        # Save current frame_list
        frame_list_prev = frame_list
        # If we don't have enough cameras for all cells
        for _ in range(N_places - len(frame_list)):
            frame_list.append(black_frame)

        # TODO: Now there are stubs until the necessary functions are made
        event_list = [black_frame for _ in range(N_cols)]
        face_list = [black_frame for _ in range(N_cols)]

        # Preparing full frame
        right_part = utils.concat_from_list(frame_list[1:], N_cols - Def_cam_size, Def_cam_size)
        upper_part = np.concatenate((frame_list[0], right_part), axis=1)
        #
        events = utils.concat_from_list(event_list, N_cols, 1)
        faces = utils.concat_from_list(face_list, N_cols, 1)
        #
        full_frame = np.concatenate((upper_part, events, faces), axis=0)
        cv.imshow(Window_name, full_frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    for cap in capture_list:
        cap.release()
    cv.destroyAllWindows()

#
