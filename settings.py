"""
Module for storing settings, options, etc.
"""
# Debug flag could be changed here
DEBUG = True

# Models folder
model_PATH = 'models'
# Output files folder
out_PATH = 'out_files'

# Cameras configurations (list of dicts).
# You can save several cameras to use some of them
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
# Def_cam_name = 'Cam07'

# Operating mode configuration
"""
Mode_name - operating mode name
Pipeline - list of models that process the image
Save - save results
Display - show video
"""
Operation_modes = [{'Mode_name': 'View1', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': 'Single camera view'},
                   {'Mode_name': 'View1_fps', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': 'Single camera view with FPS count'},
                   {'Mode_name': 'View2x2', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': 'Four cameras view'},
                   ]

         # {'Mode': 'MD', 'MD': True, 'OD': False, 'FD': False, 'Save': False, 'Display': True},
         # {'Mode': 'MDs', 'MD': True, 'OD': False, 'FD': False, 'Save': True, 'Display': True},
         # {'Mode': 'MDOD', 'MD': True, 'OD': True, 'FD': False, 'Save': False, 'Display': True},
         # {'Mode': 'MDODs', 'MD': True, 'OD': True, 'FD': False, 'Save': True, 'Display': True},
         # {'Mode': 'OD', 'MD': False, 'OD': True, 'FD': False, 'Save': False, 'Display': True},
         # {'Mode': 'ODs', 'MD': False, 'OD': True, 'FD': False, 'Save': True, 'Display': True},
         # {'Mode': 'MDcli', 'MD': True, 'OD': False, 'FD': False, 'Save': True, 'Display': False},

# Operation mode name
# Operation_mode_name = 'View1'
# Operation_mode_name = 'View1_fps'
Operation_mode_name = 'View2x2'

# Screen resolution by default
Def_W = 1200
Def_H = 800
