'''
author: matheus vieira - 2019
    last update: 15 may 2023

# HOW TO RUN:
    - Edit file 'setup_sync.py' and place in the same path of the 'wass_sync.py' file
    - Then, run:
        python wass_sync.py

# REQUIREMENTS:
    - OpenCV (python<=3.7):   conda install -c conda-forge opencv
    - Praat software:         sudo apt-get install praat
    - FFmpeg software:        sudo apt-get install ffmpeg

# DO:
    - Frames extraction
    - Frames synchronization
    - Apply audio wind filter before frame synchronization (optional)
    - Frames resampling       (optional)

# Tested devices
    - Smartphones:    Galaxy J5 Pro 1080/30 fps - CMOS 13MP     - VFR
    - Action cameras: GoPro HERO9 4K/30/24 or 1080p/30/24 fps   - CFR
    - DSLR Pro:       PANASONIC AG-UX 180 - 4K/50 fps           - CFR
    - DSLR Pro:       Canon 4K  15xzoom                         - CFR


#-------------------------------------------------------------------------------
# ps:
# - If videos has a Constant Frame Rate - CFR (i.e DLSR Pro cameras, GoPro's)
#   then the frames are straight extracted from original video, synchronized,
#   resampled and stored in cam0/cam1 paths without any new video created.
# - If videos has a Variable Frame Rate - VFR (i.e. smartphones)
#   then is created a new re-encoding synchronized video (you can choose the new
#   output fps and video format) then the synchronized frames are extracted
#   from the encoded video and stored in cam0/cam1 paths.
# - A wind noise filter can be applied for better cross-correlation of the audio
#   signal in windy conditions
#
#    If there's a corrupt MP4 video file, run:
#    ffmpeg -i cam0.MP4 -c copy cam01.MP4
#-------------------------------------------------------------------------------
'''
