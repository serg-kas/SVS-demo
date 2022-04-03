# Программа получает видео с камер по rtsp.
# Видео обрабатывается разными алгоритмами и моделями согласно заданного режима работы.
# Папка models предназначена для хранения моделей.
# Папка out_files предназначена для записи результатов (коротких роликов или изображений).
# Параметры хранятся в файле settings.py
# Функции - в файлах run.py и utils.py
# Режим работы может быть задан параметром командной строки.
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
def process(Operation_mode_text):
    """
    :param Operation_mode_text: Operation mode text for resolving
    :return: None
    """
    # Environment preparation
    utils.do_preparing()

    # Loading cameras configurations
    Cam_list = utils.get_cam_list()
    if VERBOSE:
        print('Loaded active cameras: {}'.format(len(Cam_list)))

    # Parsing operation mode from text
    Operation_mode, N_cols, N_rows = utils.get_operation_mode(Operation_mode_text)
    if VERBOSE:
        print('Operation mode starting: {}, C={}, R={}'.format(Operation_mode['Mode_name'], N_cols, N_rows))

    # Get screen resolution info
    W, H = utils.get_screen_resolution()
    if VERBOSE:
        print('Screen resolution: ({},{})'.format(W, H))
    # Set frame size
    W_frame, H_frame = int(W * 0.85), int(H * 0.85)

    # Case switch for running in selected operation mode
    match Operation_mode['Mode_name']:
        case 'Single_fps':
            # Function for single camera view with calculating FPS
            run.show_single_fps(Cam_list[0], W_frame, H_frame)
        case 'UniformCxR':
            run.show_uniform(Cam_list, W_frame, H_frame, N_cols, N_rows)
        case 'Custom1CxR':
            run.show_custom1(Cam_list, W_frame, H_frame, N_cols, N_rows, 1)
        case 'test':
            # run.show_uniform(Cam_list, W_frame, H_frame, 5, 4)
            run.show_custom1(Cam_list, W_frame, H_frame, 6, 4, 2)
        case _:
            print('Wrong operation mode (function not found).')


if __name__ == '__main__':
    # Debug and verbose flags
    DEBUG = settings.DEBUG
    VERBOSE = settings.VERBOSE
    if DEBUG:
        print('DEBUG mode: on')
    # Operating mode text may be replaced from command line args
    Operation_mode_text = settings.Operation_mode_name if len(sys.argv) <= 1 else sys.argv[1]
    if VERBOSE:
        if len(sys.argv) > 1:
            print('Try to resolve Operation mode from command line: {}'.format(Operation_mode_text))
    # Run process
    process(Operation_mode_text)
