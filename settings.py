#
# Module for storing settings, options, etc.
#
# Verbose and Debug flags
VERBOSE = True
DEBUG = True


# Models folder
model_PATH = 'models'
# Output files folder
out_PATH = 'out_files'


# Cameras configuration.
# You can save several cameras to use some of them by using Is_active parameter
# Put RTSP url string with user:password if needed.
Cameras = [{'Cam_name': 'Cam01', 'Is_active': True, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=1&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=1&subtype=1'},
           {'Cam_name': 'Cam02', 'Is_active': True, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=2&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=2&subtype=1'},
           {'Cam_name': 'Cam03', 'Is_active': True, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=3&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=3&subtype=1'},
           {'Cam_name': 'Cam04', 'Is_active': True, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=4&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=4&subtype=1'},
           {'Cam_name': 'Cam05', 'Is_active': True, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=5&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=5&subtype=1'},
           {'Cam_name': 'Cam06', 'Is_active': True, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=6&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=6&subtype=1'},
           {'Cam_name': 'Cam07', 'Is_active': True, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=7&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=7&subtype=1'},
           {'Cam_name': 'Cam08', 'Is_active': False, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=8&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=8&subtype=1'},
           {'Cam_name': 'Cam09', 'Is_active': False, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=9&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=9&subtype=1'},
           {'Cam_name': 'Cam10', 'Is_active': False, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=10&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=10&subtype=1'},
           {'Cam_name': 'Cam11', 'Is_active': True, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=11&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=11&subtype=1'},
           {'Cam_name': 'Cam12', 'Is_active': False, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=12&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=12&subtype=1'},
           {'Cam_name': 'Cam13', 'Is_active': True, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=13&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=13&subtype=1'},
           {'Cam_name': 'Cam14', 'Is_active': True, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=14&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=14&subtype=1'},
           {'Cam_name': 'Cam15', 'Is_active': True, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=15&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=15&subtype=1'},
           {'Cam_name': 'Cam16', 'Is_active': False, 'MD_enabled': True,
            'RTSP': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=16&subtype=0',
            'RTSP_sub': 'rtsp://admin:daH_2019@192.168.5.44:554/cam/realmonitor?channel=16&subtype=1'},
           ]


# Default camera name
Def_cam_name = 'Cam11'
# Def_cam_name = 'Cam01'


# Operating mode configuration
# Mode_name - operating mode name
# Pipeline - list of models that process the image
# Save - save results (events)
# Display - show video
Operation_modes = [{'Mode_name': 'Single', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': 'Single camera view'},
                   {'Mode_name': 'UniformCxR', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': 'Uniform template with CхR cells'},
                   {'Mode_name': 'Custom_CxR', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': 'Scaled Def_cam view and some other cameras with event row(s)'},
                   {'Mode_name': 'test', 'Pipeline': [], 'Save': False, 'Display': True,
                    'Description': 'For testing purpose'},
                   ]


# Operation mode string
# Operation_mode_string = 'single'
# Operation_mode_string = 'uniform4x4'
# Operation_mode_string = 'custom_5x4'
Operation_mode_string = 'test'


# Columns and rows by default
Def_cols = 4
Def_rows = 4


# Screen resolution by default
Def_W = 1280
Def_H = 800


# Options for Custom_CxR template
Events_line = True
Faces_line = True


# Option for Single and UniformCxR templates
FPS_calc = True


# Frame buffer size for each cam
N_buff = 100
# After how many errors reset video capture
N_errors_to_reset = 10
