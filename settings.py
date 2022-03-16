"""
Module for settings, options, etc.
"""

# Debugging flag to be changed here
DEBUG = True

# Program folder
PATH = '/home/serg/bin/SVS-demo'
# Model folder
model_PATH = 'models'
# Output files folder
out_PATH = 'out_files'


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
# Max event video time (sec)
N_max = 10


# Cameras configurations (list of dicts).
# You can save several cameras to use one of them.
# Put RTSP string with user:password if needed.
# The "Active" variable is intended for future use multiple cameras.
Cameras = [{'Cam': 'Cam01', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=1&subtype=0'},
           {'Cam': 'Cam02', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=2&subtype=0'},
           {'Cam': 'Cam03', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=3&subtype=0'},
           {'Cam': 'Cam06', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=6&subtype=0'},
           {'Cam': 'Cam07', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=7&subtype=0'},
           {'Cam': 'Cam11', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=11&subtype=0'},
           {'Cam': 'Cam13', 'Active': False,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=13&subtype=0'},
           {'Cam': 'Cam14', 'Active': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=14&subtype=0'},
           ]
# Default camera
Def_Cam = 'Cam11'


# Operating mode configuration
# Mode - operating mode name
# Motion - use motion detection before model
# Model - use model for object detection
# Save - save results
# Display - show video
Modes = [{'Mode': 'View', 'Motion': False, 'Model': False, 'Save': False, 'Display': True},
         {'Mode': 'MDv', 'Motion': True, 'Model': False, 'Save': False, 'Display': True},
         {'Mode': 'MDs', 'Motion': True, 'Model': False, 'Save': True, 'Display': True},
         {'Mode': 'MDODv', 'Motion': True, 'Model': True, 'Save': False, 'Display': True},
         {'Mode': 'MDODs', 'Motion': True, 'Model': True, 'Save': True, 'Display': True},
         {'Mode': 'ODv', 'Motion': False, 'Model': True, 'Save': False, 'Display': True},
         {'Mode': 'ODs', 'Motion': False, 'Model': True, 'Save': True, 'Display': True},
         {'Mode': 'MDcli', 'Motion': True, 'Model': False, 'Save': True, 'Display': False},
         {'Mode': 'MDcli', 'Motion': True, 'Model': True, 'Save': True, 'Display': False},
         {'Mode': 'ODcli', 'Motion': False, 'Model': True, 'Save': True, 'Display': False},
         ]
# Default mode
Def_Mode = 'View'