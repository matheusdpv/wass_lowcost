'''
author: matheus vieira - 2021

# NEEDS:
    - OpenCV (python<=3.7):   conda install -c conda-forge opencv
    - Praat software:         sudo apt-get install praat
    
    - Set script preferences                      [lines 35-50]
    - Insert just video files inside video path   [pathname - line 35]

# DO:
    - Apply wind filter       (optional)
    - Frames extraction
    - Frames synchronization
    - Frames resampling       (optional)
    - Frames renaming         (optional)

# Tested devices
    - Smartphones:    Galaxy J5 Pro 1080/30 fps - CMOS 13MP     - VFR
    - Action cameras: GoPro HERO9 4K/30/24 or 1080p/30/24 fps   - CFR
    - DSLR Pro:       PANASONIC AG-UX 180 - 4K/50 fps           - CFR
'''

import os
import numpy as np
import subprocess
from glob import glob
import cv2
from scipy.io import wavfile
from scipy import signal
import shutil

# ############################ Input #########################################

pathname = '/media/matheus/DATA/'      # videos path
op_system = 'linux'                    # 'windows' / 'linux'
cameras = '01'                         # '0'= left/ '1'=right / '01'=left and right 
cam_type = 'gopro'                     # 'dslr' / 'smartphone' / 'gopro'
video_format_in = 'MP4'                # 'MP4' / 'mp4' / 'mov' / 'avi' ...
fps_input = 24                         # 10 / 24 / 30 / 50
resample_frames = 'yes'                # 'yes' / 'no'
fps_resampled = 12                     # 10 / 24 / 30 / 50 # if
wind_filter = 'on'                     # 'on' / 'off'
last_frame = 200                       # last synchronized frame number
rename_frames = 'yes'

# NEED EDIT ONLY FOR VariableFrameRate VIDEOS (i.e Smartphones):
video_format_out = 'mp4'               # 'MP4' / 'mp4' / 'mov' / 'avi' ...
clip_start = 0                         # start in seconds (ref clip)
clip_end =   99999                     # end   in seconds

# ############################################################################
