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
        case 'Single_fps':
            #
            print('Operation mode: {}'.format(Operation_mode['Mode_name']))
            run.show_single_fps(Cam_list[0], W_frame, H_frame)
        case 'UniformCxR':
            #
            print('Operation mode: {}, C={}, R={}'.format(Operation_mode['Mode_name'], N_cols, N_rows))
            run.show_uniform(Cam_list, W_frame, H_frame, N_cols, N_rows)
        case 'Custom_CxR':
            #
            print('Operation mode: {}, C={}, R={}, E={}'.format(Operation_mode['Mode_name'], N_cols, N_rows, 1))
            run.show_custom1(Cam_list, W_frame, H_frame, N_cols, N_rows, 1)
        case 'test':
            #
            print('Operation mode: {}'.format(Operation_mode['Mode_name']))
            # run.show_uniform(Cam_list, W_frame, H_frame, 4, 4)
            # run.show_uniform_fps(Cam_list, W_frame, H_frame, 4, 4)
            # run.show_custom1(Cam_list, W_frame, H_frame, 4, 3, True, True)
            run.show_custom1_fps(Cam_list, W_frame, H_frame, 6, 4, True, False)
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
