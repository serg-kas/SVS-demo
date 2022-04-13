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
    # Calculate FPS after N_frames
    if FPS_calc:
        N_frames = 50
        frames_count = 0
        fps = 'Calculating fps...'
        font = cv.FONT_HERSHEY_SIMPLEX  # font to display FPS
        fontScale = 3  # TODO: Get optimal font scale and text position
        prev_time = time.time()  # record the time when we processed last frame
    #
    while True:
        isTrue, frame = capture.read()
        #
        frame = cv.resize(frame, (W, H), interpolation=cv.INTER_AREA)
        #
        if FPS_calc:
            if frames_count == N_frames-1:
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


# Show video from C*R cameras in uniform template
def show_uniform(Cam_list, W=1280, H=800, N_cols=2, N_rows=2):
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
                        print('Reconnected cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
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


# Show video from C*R cameras in uniform template with calculating fps
def show_uniform_fps_old(Cam_list, W=1280, H=800, N_cols=2, N_rows=2):
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

    # Calculate FPS after N_frames
    N_frames = 50
    frames_count = 0
    fps = 'Calculating FPS...'
    font_fps = cv.FONT_HERSHEY_SIMPLEX  # font to display FPS
    fontScale_fps = 3  # TODO: Get optimal font scale and text position
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

def show_uniform_fps(Cam_list, W=1280, H=800, N_cols=2, N_rows=2, FPS_calc=False):
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

    # Calculate FPS after N_frames for each cam
    N_frames = 50
    frames_count_list = [0 for _ in range(len(capture_list))]
    fps_list = ['Calculating FPS...' for _ in range(len(capture_list))]
    font_fps = cv.FONT_HERSHEY_SIMPLEX  # font to display FPS
    fontScale_fps = 2  # TODO: Get optimal font scale and text position
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
                cv.putText(frame, str(fps_list[idx]), (7, 70), font_fps, fontScale_fps, (100, 255, 0), 3, cv.LINE_AA)
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


# Show video custom template Def_cam + some other cams + event/face lines
def show_custom1(Cam_list, W=1280, H=800, N_cols=2, N_rows=2, Event_line=True, Face_line=True):
    # Preparing template
    w, h = int(W / N_cols), int(H / N_rows)
    # Lines reserved for events/faces
    Bottom_lines = int(Event_line) + int(Face_line)
    assert Bottom_lines > 0, 'Custom template must have at least one line for events or faces'
    assert N_cols > 1 and N_rows > Bottom_lines, 'Custom template must be at least 2x(Bottom_lines+1) cells in size'
    # Def_cam will be the size of all rows except those reserved for event lines
    Def_cam_size = N_rows - Bottom_lines
    #
    Def_cam_w, Def_cam_h = Def_cam_size * w, Def_cam_size * h
    #
    N_places = (N_cols-Def_cam_size) * Def_cam_size + 1  # how many cameras are placed on frame including Def_cam
    #
    SOURCE_list = [Cam_list[0]['RTSP']] + [cam['RTSP_sub'] for cam in Cam_list[1:]]  # Def_cam uses RTSP main stream
    SOURCE_list = SOURCE_list[:N_places]  # we don't need cameras more than we have places

    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]

    black_frame = np.zeros((h, w, 3), dtype=np.uint8)
    def_cam_black_frame = np.zeros((Def_cam_h, Def_cam_w, 3), dtype=np.uint8)

    frame_list_prev = [def_cam_black_frame] + [black_frame for _ in range(len(capture_list)-1)]
    error_count_list = [0 for _ in range(len(capture_list))]
    N_errors = settings.N_errors_to_reset

    font = cv.FONT_HERSHEY_SIMPLEX  # font to display connecting status
    fontScale = 0.9  # TODO: Get optimal font scale and text position

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
                    if error_count_list[idx] >= 1:
                        print('Successfully get frame from cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
                error_count_list[idx] = 0  # reset error count
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
                        print('Reconnected cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
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
        right_part = utils.concat_from_list(frame_list[1:], N_cols-Def_cam_size, Def_cam_size)
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


# Show video custom template Def_cam + some other cams + event/face lines
def show_custom1_fps(Cam_list, W=1280, H=800, N_cols=2, N_rows=2, Event_line=True, Face_line=True):
    # Preparing template
    w, h = int(W / N_cols), int(H / N_rows)
    # Lines reserved for events/faces
    Bottom_lines = int(Event_line) + int(Face_line)
    assert Bottom_lines > 0, 'Custom template must have at least one line for events or faces'
    assert N_cols > 1 and N_rows > Bottom_lines, 'Custom template must be at least 2x(Bottom_lines+1) cells in size'
    # Def_cam will be the size of all rows except those reserved for event lines
    Def_cam_size = N_rows - Bottom_lines
    #
    Def_cam_w, Def_cam_h = Def_cam_size * w, Def_cam_size * h
    #
    N_places = (N_cols-Def_cam_size) * Def_cam_size + 1  # how many cameras are placed on frame including Def_cam
    #
    SOURCE_list = [Cam_list[0]['RTSP']] + [cam['RTSP_sub'] for cam in Cam_list[1:]]  # Def_cam uses RTSP main stream
    SOURCE_list = SOURCE_list[:N_places]  # we don't need cameras more than we have places

    capture_list = [cv.VideoCapture(source) for source in SOURCE_list]

    black_frame = np.zeros((h, w, 3), dtype=np.uint8)
    def_cam_black_frame = np.zeros((Def_cam_h, Def_cam_w, 3), dtype=np.uint8)

    frame_list_prev = [def_cam_black_frame] + [black_frame for _ in range(len(capture_list)-1)]
    error_count_list = [0 for _ in range(len(capture_list))]
    N_errors = settings.N_errors_to_reset

    font = cv.FONT_HERSHEY_SIMPLEX  # font to display connecting status
    fontScale = 0.9  # TODO: Get optimal font scale and text position

    Window_name = 'Custom View ' + str(N_cols) + ' x ' + str(N_rows)

    # Calculate FPS after N_frames
    N_frames = 50
    frames_count = 0
    fps = 'Calculating FPS ...'
    font_fps = cv.FONT_HERSHEY_SIMPLEX  # font to display FPS
    fontScale_fps = 3  # TODO: Get optimal font scale and text position
    prev_time = time.time()  # record the time when we processed last frame

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
                    if error_count_list[idx] >= 1:
                        print('Successfully get frame from cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
                error_count_list[idx] = 0  # reset error count
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
                        print('Reconnected cap[{0}] after {1} errors'.format(idx, error_count_list[idx]))
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
        right_part = utils.concat_from_list(frame_list[1:], N_cols-Def_cam_size, Def_cam_size)
        upper_part = np.concatenate((frame_list[0], right_part), axis=1)
        #
        events = utils.concat_from_list(event_list, N_cols, 1)
        faces = utils.concat_from_list(face_list, N_cols, 1)
        #
        full_frame = np.concatenate((upper_part, events, faces), axis=0)
        #
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