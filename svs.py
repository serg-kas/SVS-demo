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
def process(Operation_mode_name):
    """
    Operation_mode_name - operation mode to be run
    """
    # Reading folder configuration from settings
    model_PATH = settings.model_PATH
    out_PATH = settings.out_PATH
    # Create folders if needed
    if not (model_PATH in os.listdir('.')):
        os.mkdir(model_PATH)
    if not (out_PATH in os.listdir('.')):
        os.mkdir(out_PATH)

    # Loading Active cameras configurations from settings
    Cam_list = utils.get_cam_list()
    if DEBUG:
        print('Active cameras loaded: {0}'.format(len(Cam_list)))

    # Reading operation mode from settings
    Operation_mode = utils.get_operation_mode(Operation_mode_name)
    if DEBUG:
        print('Operation mode starting: {}'.format(Operation_mode['Mode_name']))

    # Get screen resolution info
    W, H = utils.get_screen_resolution()
    if DEBUG:
        print('Screen resolution: ({0},{1})'.format(W, H))
    # TODO: What is the minimum screen resolution to work with?
    if W < 1024 | H < 768:
        W = settings.Def_W
        H = settings.Def_H
    # Set frame size
    W_frame = int(W * 0.85)
    H_frame = int(H * 0.85)

    # Case switch for running in selected operation mode
    match Operation_mode['Mode_name']:
        case 'View1':
            # Function for single camera view with calculating FPS
            run.show_from_source_fps(Cam_list[0], W_frame, H_frame)
        case 'View2x2':
            run.show_from_source_cxr(Cam_list, W_frame, H_frame, 2, 2)
        case 'View4x4':
            run.show_from_source_cxr(Cam_list, W_frame, H_frame, 4, 4)
        case 'test':
            # run.show_from_source_cxr(Cam_list, W_frame, H_frame, 5, 4)
            run.show_from_source_custom(Cam_list, W_frame, H_frame, 7, 7, 3)
        case _:
            print('Wrong operation mode (function not found).')


if __name__ == '__main__':
    # Debugging flag
    DEBUG = settings.DEBUG
    if DEBUG:
        print('DEBUG mode: on')
    # Operating mode may be replaced from command line args
    Operation_mode_name = settings.Operation_mode_name if len(sys.argv) <= 1 else sys.argv[1]
    if DEBUG:
        if len(sys.argv) > 1:
            print('Operation mode is set by the command line parameter: {}'.format(Operation_mode_name))
    # Run process
    process(Operation_mode_name)
