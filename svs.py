"""
Программа получает видео с камер по rtsp.
Видео обрабатывается разными алгоритмами и моделями согласно заданного режима работы.
Папка models предназначена для хранения моделей.
Папка out_files предназначена для записи результатов (коротких роликов или изображений).
Параметры хранятся в файле settings.py
Функции - в файле utils.py
Режим работы может быть задан параметром командной строки.
"""

# Necessary modules
import os
import sys
import warnings
warnings.filterwarnings("ignore")

# Settings and functions
import settings
import utils

# Process function
def process(Operation_mode_name):
    """
    operating_MODE - selected operating mode
    """

    # Reading folder configuration from settings
    model_PATH = settings.model_PATH
    out_PATH = settings.out_PATH
    # Create folders if needed
    if not (model_PATH in os.listdir('.')):
        os.mkdir(model_PATH)
    if not (out_PATH in os.listdir('.')):
        os.mkdir(out_PATH)

    # Reading Active cams configuration from settings
    Cam_list = []
    Def_cam = None
    for cam in settings.Cameras:
        if cam['Active']:
            Cam_list.append(cam)
            if cam['Cam_name'] == settings.Def_cam_name:
                Def_cam = cam  # default camera assignment
                if DEBUG:
                    print('Default camera is: {}'.format(Def_cam['Cam_name']))
    if DEBUG:
        print('Total cameras loaded: {0}'.format(len(Cam_list)))
    assert Def_cam is not None, 'Must have Def_cam assigned'

    # Reading operation mode from settings
    Operation_mode = None
    for mode in settings.Operation_modes:
        if mode['Mode_name'] == settings.Operation_mode_name:
            Operation_mode = mode  # operation mode assignment
            if DEBUG:
                print('Operation mode is: {}'.format(Operation_mode['Mode_name']))
    assert Operation_mode is not None, 'Operation_mode is not assigned'

    # Case switch
    match Operation_mode['Mode_name']:
        case 'View1':
            print('Запускаем режим {}'.format('View1'))
            utils.show_from_source(Def_cam['RTSP'], settings.W_frame, settings.H_frame)
        case _:
            print('Нужной функции пока нет')


if __name__ == '__main__':
    # Debugging flag
    DEBUG = settings.DEBUG
    if DEBUG:
        print('DEBUG mode: on')
    # Operating mode may be replaced from command line args
    Operation_mode_name = settings.Operation_mode_name if len(sys.argv) <= 1 else sys.argv[1]
    if DEBUG:
        print('Operating mode pre-selected: {}'.format(Operation_mode_name))
    # Run process
    process(Operation_mode_name)
