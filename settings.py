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
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=1&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=1&subtype=1'},
           {'Cam_name': 'Cam02', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=2&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=2&subtype=1'},
           {'Cam_name': 'Cam03', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=3&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=3&subtype=1'},
           {'Cam_name': 'Cam04', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=4&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=4&subtype=1'},
           {'Cam_name': 'Cam05', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=5&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=5&subtype=1'},
           {'Cam_name': 'Cam06', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=6&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=6&subtype=1'},
           {'Cam_name': 'Cam07', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=7&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=7&subtype=1'},
           {'Cam_name': 'Cam08', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=8&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=8&subtype=1'},
           {'Cam_name': 'Cam09', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=9&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=9&subtype=1'},
           {'Cam_name': 'Cam10', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=10&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=10&subtype=1'},
           {'Cam_name': 'Cam11', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=11&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=11&subtype=1'},
           {'Cam_name': 'Cam12', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=12&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=12&subtype=1'},
           {'Cam_name': 'Cam13', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=13&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=13&subtype=1'},
           {'Cam_name': 'Cam14', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=14&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=14&subtype=1'},
           {'Cam_name': 'Cam15', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=15&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=15&subtype=1'},
           {'Cam_name': 'Cam16', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=16&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=16&subtype=1'},
           ]

# Default camera name
Def_cam_name = 'Cam11'
# Def_cam_name = 'Cam01'


# Operating mode configuration
"""
Mode_name - operating mode name
Pipeline - list of models that process the image
Save - save results
Display - show video
"""
Operation_modes = [{'Mode_name': 'View1', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': 'Single camera view with calculating FPS'},
                   {'Mode_name': 'View2x2', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': '4 cameras view'},
                   {'Mode_name': 'View4x4', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': '16 cameras view'},
                   {'Mode_name': 'test', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': 'Test 16 cameras view'},
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
# Operation_mode_name = 'View2x2'
# Operation_mode_name = 'View4x4'
Operation_mode_name = 'test'


# Screen resolution by default
Def_W = 1200
Def_H = 800

# Now many errors to reset video capture
N_errors_to_reset = 10
