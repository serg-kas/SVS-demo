# The program receives video from cameras via rtsp.
# Video is processed by different algorithms and models according to the specified mode of operation.
# The models folder is for storing models.
# The out_files folder is for recording results (short clips or images).
# Settings are stored in settings.py
# Functions - in run.py and utils.py files
# The mode of operation can be set with a command line parameter.
#
import sys
#
import settings
import utils
import run
import depreciated as depr
#
# import warnings
# warnings.filterwarnings("ignore")


# Process function
def process(Operation_mode_string):
    """
    :param Operation_mode_string: Text string from which the operating mode is parsed
    :return: None
    """
    # Environment preparation
    utils.do_preparing()

    # Loading cameras configurations
    Cam_list = utils.get_cam_list()

    # Parsing operation mode from text
    Operation_mode, N_cols, N_rows = utils.get_operation_mode(Operation_mode_string)

    # Get screen resolution info
    W, H = utils.get_screen_resolution()
    # Set full frame size
    W_frame, H_frame = int(W * 0.85), int(H * 0.85)

    # Case switch for running in selected operation mode
    match Operation_mode['Mode_name']:
        case 'Single':
            #
            print('Operation mode: {}'.format(Operation_mode['Mode_name']))
            run.show_single(Cam_list[0], W_frame, H_frame, FPS_calc=settings.FPS_calc)

        case 'UniformCxR':
            #
            print('Operation mode: {}, C={}, R={}'.format(Operation_mode['Mode_name'], N_cols, N_rows))
            run.show_uniform_buff(Cam_list, W_frame, H_frame, N_cols, N_rows, FPS_calc=settings.FPS_calc)
        case 'Custom_CxR':
            #
            Events_line, Faces_line = settings.Events_line, settings.Faces_line
            print('Operation mode: {}, C={}, R={}, E={}, F={}'.format(Operation_mode['Mode_name'], N_cols, N_rows, Events_line, Faces_line))
            run.show_custom1(Cam_list, W_frame, H_frame, N_cols, N_rows, Events_line, Faces_line)

        case 'test':
            #
            print('Operation mode: {}'.format(Operation_mode['Mode_name']))
            #
            # depr.show_uniform_fps_cells(Cam_list, W_frame, H_frame, N_cols=4, N_rows=4, FPS_calc=True)
            # depr.show_uniform(Cam_list, W_frame, H_frame, N_cols=4, N_rows=4, FPS_calc=True)
            run.show_uniform_buff(Cam_list, W_frame, H_frame, N_cols=5, N_rows=4, FPS_calc=True)
            #
            # run.show_custom1(Cam_list, W_frame, H_frame, N_cols=5, N_rows=5, Events_line=True, Faces_line=True)
            #

        case _:
            print('Error starting operation mode (function not found).')


if __name__ == '__main__':
    # Verbose and Debug options
    VERBOSE = settings.VERBOSE
    if VERBOSE:
        print('Welcome, we are starting...')
    DEBUG = settings.DEBUG
    if DEBUG:
        print('DEBUG mode: on')
    # Operating_mode_string may be replaced from command line arg
    Operation_mode_string = settings.Operation_mode_string if len(sys.argv) <= 1 else sys.argv[1]
    # Run process
    process(Operation_mode_string)
