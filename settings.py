"""
Module for storing settings, options, etc.
"""
# Debug and Verbose flags could be changed here
DEBUG = True
# VERBOSE = True

# Models folder
model_PATH = 'models'
# Output files folder
out_PATH = 'out_files'

# Cameras configurations (list of dicts).
# You can save several cameras to use some of them.
# Put RTSP string with user:password if needed.
Cameras = [{'Cam_name': 'Cam01', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=1&subtype=0'},
           {'Cam_name': 'Cam02', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=2&subtype=0'},
           {'Cam_name': 'Cam03', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=3&subtype=0'},
           {'Cam_name': 'Cam06', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=6&subtype=0'},
           {'Cam_name': 'Cam07', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=7&subtype=0'},
           {'Cam_name': 'Cam11', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=11&subtype=0'},
           {'Cam_name': 'Cam13', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=13&subtype=0'},
           {'Cam_name': 'Cam14', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=14&subtype=0'},
           ]
# Default camera name
Def_cam_name = 'Cam11'

# Operating mode configuration
"""
Mode - operating mode name
MD - use motion detection before model
Model - use model for object detection
Save - save results
Display - show video
"""
Operation_modes = [{'Mode_name': 'View1', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': ''},



         # {'Mode': 'MDv', 'MD': True, 'OD': False, 'FD': False, 'Save': False, 'Display': True},
         # {'Mode': 'MDs', 'MD': True, 'OD': False, 'FD': False, 'Save': True, 'Display': True},
         # {'Mode': 'MDODv', 'MD': True, 'OD': True, 'FD': False, 'Save': False, 'Display': True},
         # {'Mode': 'MDODs', 'MD': True, 'OD': True, 'FD': False, 'Save': True, 'Display': True},
         # {'Mode': 'ODv', 'MD': False, 'OD': True, 'FD': False, 'Save': False, 'Display': True},
         # {'Mode': 'ODs', 'MD': False, 'OD': True, 'FD': False, 'Save': True, 'Display': True},
         # {'Mode': 'MDcli', 'MD': True, 'OD': False, 'FD': False, 'Save': True, 'Display': False},
         # {'Mode': 'MDcli', 'MD': True, 'OD': True, 'FD': False, 'Save': True, 'Display': False},
         # {'Mode': 'ODcli', 'MD': False, 'OD': True, 'FD': False, 'Save': True, 'Display': False},
         ]
# Operation mode name
Operation_mode_name = 'View1'

#
# Frame size for visualization
W_frame = 1100
H_frame = 700
# Frame size for event visualization
W_event = 300
H_event = 200
# How many events to be displayed
N_event = 4
# How many frames to be buffered
N_buff = 50
# Max frames in event
N_max = 300

# Предполагаются следующие режимы рабоы программы (могут изменяться и дополняться):
# 1. Просмотр видео (без обработки). Предназначен для проверки доступности источника видео.
# 2. Просмотр видео с детекцией движения (без записи). Предназначен для оценки детекции движения.
# 3. Просмотр видео с детекцией движения (с записью роликов с обнаруженным движением).
# 4. Просмотр видео с детекцией движения и обработкой части кадра моделью для детекции объектов (без записи).
# 5. Просмотр видео с детекцией движения и обработкой части кадра моделью для детекции объектов (с записью).
# 6. Просмотр видео с обработкой полного кадра моделью для детекции объектов (без записи).
# 7. Просмотр видео с обработкой полного кадра моделью для детекции объектов (с записью).
# Режимы 4-7 могут быть реализованы в варианте только с записью (без отображения картинки на мониторе)