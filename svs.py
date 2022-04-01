"""
Программа получает видео с камер по rtsp.
Видео обрабатывается разными алгоритмами и моделями согласно заданного режима работы.
Папка models предназначена для хранения моделей.
Папка out_files предназначена для записи результатов (коротких роликов или изображений).
Параметры хранятся в файле settings.py
Функции - в файлах run.py и utils.py
Режим работы может быть задан параметром командной строки.
"""
# Settings and functions
import settings
import utils
import run
# Necessary modules
import os
import sys
import warnings
warnings.filterwarnings("ignore")


# Process function
def process(Operation_mode_text):
    """
    :param Operation_mode_text: Operation mode nick for resolving
    :return: None
    """
    # Reading folder configuration from settings
    model_PATH = settings.model_PATH
    out_PATH = settings.out_PATH
    # Create folders if needed
    if not (model_PATH in os.listdir('.')):
        os.mkdir(model_PATH)
    if not (out_PATH in os.listdir('.')):
        os.mkdir(out_PATH)

    # Loading cameras configurations from settings
    Cam_list = utils.get_cam_list()
    if DEBUG:
        print('Active cameras loaded: {0}'.format(len(Cam_list)))

    # Parsing operation mode from text
    Operation_mode, N_cols, N_rows = utils.get_operation_mode(Operation_mode_text)
    if DEBUG:
        print('Operation mode starting: {0}, C={1}, R={2}'.format(Operation_mode['Mode_name'], N_cols, N_rows))

    # Get screen resolution info
    W, H = utils.get_screen_resolution()
    if DEBUG:
        print('Screen resolution: ({0},{1})'.format(W, H))
    # Set frame size
    W_frame, H_frame = int(W * 0.85), int(H * 0.85)

    # Case switch for running in selected operation mode
    match Operation_mode['Mode_name']:
        case 'View1':
            # Function for single camera view with calculating FPS
            run.show_from_source_fps(Cam_list[0], W_frame, H_frame)
        case 'ViewCxR':
            run.show_from_source_cxr(Cam_list, W_frame, H_frame, N_cols, N_rows)
        case 'test':
            # run.show_from_source_cxr(Cam_list, W_frame, H_frame, 5, 4)
            run.show_from_source_custom(Cam_list, W_frame, H_frame, 6, 4, 2)
        case _:
            print('Wrong operation mode (function not found).')


if __name__ == '__main__':
    # Debugging flag
    DEBUG = settings.DEBUG
    if DEBUG:
        print('DEBUG mode: on')
    # Operating mode text may be replaced from command line args
    Operation_mode_text = settings.Operation_mode_name if len(sys.argv) <= 1 else sys.argv[1]
    if DEBUG:
        if len(sys.argv) > 1:
            print('Try to resolve Operation mode from command line: {}'.format(Operation_mode_text))
    # Run process
    process(Operation_mode_text)
