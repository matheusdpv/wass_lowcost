#-------------------------------------------------------------------------------------#
# SETUP FILE TO CONFIGURE IMAGE EXTRACTION AND SYNCHRONIZATION FROM VIDEO FILES       #
# HOW TO RUN:                                                                         #
#    - Edit file 'setup_sync.py' and place in the same path of 'wass_sync.py' file    #
#    - Change to directory where 'setup_sync.py' and 'wass_sync.py' are then, run:    #
#        python wass_sync.py                                                          #
#-------------------------------------------------------------------------------------#


# INPUT VIDEO FILES PATHNAME
pathname = '/home/matheus/Desktop/test_caparica_19072022_run02/'

# OPERATIONAL SYSTEM
op_system = 'linux'                   # 'windows' / 'linux'

# CHOOSE ONE OR MORE CAMERAS FOR FRAME EXTRACTION
camera_id = '01'                      # '0'= left/ '1'=right / '01'=left and right

# CAMERA TYPE
camera_type = 'gopro'                 # 'dslr' / 'smartphone' / 'gopro'

# INPUT VIDEO FORMAT
video_format_input = 'mp4'            # 'MP4' / 'mp4' / 'mov' / 'avi'

# INPUT VIDEO ACQUISITION RATE
video_fps_input = 24                  # 10 / 24 / 30 / 50

# OUTPUT VIDEO ACQUISITION RATE (set equal to video_fps_input if no resample needed)
video_fps_output= 12                  # 10 / 24 / 30 / 50

# OUTPUT IMAGE FORMAT
image_format_output = 'jpg'           # 'jpg' / 'tif' / 'png'

# FIRST IMAGE TO BE EXTRACTED BEFORE SYNC -
image_extracted_first = 3000          # i.e: 3600 = 1st image before 2min of video in 30fps [2*60*30=3600]

# LAST IMAGE TO BE EXTRACTED BEFORE SYNC
image_extracted_last  = 3100          # if needed the entire video, set this value to 999999

# FIRST TIME WINDOW IN SECONDS TO FIND THE AUDIO PEAK SIGNAL TO CALCULATE CROSS-CORRELATION
audio_sync_cc_window_ini = 0

# LAST TIME WINDOW IN SECONDS TO FIND THE AUDIO PEAK SIGNAL TO CALCULATE CROSS-CORRELATION
audio_sync_cc_window_fin = 30

# WIND FILTER FOR NOISY ENVIRONMENTS - [OPTIONAL]
audio_wind_filter = 'on'              # 'on' / 'off' [on: need stereo audio with 2 channels -> audio_stereo = 'on']

# SET STEREO AUDIO TYPE (DATA IN 1 OR 2 CHANNELS)
audio_stereo = 'on'                   # 'on' / 'off' [off: stereo audio with data just in 1 channel]



#-------------------------------------------------------------------------
# NEED EDIT ONLY FOR VariableFrameRate() VIDEOS (i.e Smartphones):
video_format_output = 'mp4'            # 'MP4' / 'mp4' / 'mov' / 'avi' ...
clip_start = 0                         # start in seconds (ref clip)
clip_end =   1000                      # end   in seconds
#-------------------------------------------------------------------------
