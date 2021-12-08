'''
author: matheus vieira - 2021

NEEDS:
    - OpenCV (python<=3.7):   conda install -c conda-forge opencv
    - Praat software:         sudo apt-get install praat
    
    - Set script preferences                      [lines 35-50]
    - Insert just video files inside video path   [pathname - line 35]

DO:
    - Apply wind filter
    - Frames extraction
    - Frames synchronization
    - Frames resampling
    - Frames renaming 

Tested devices
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

############################# Input #########################################

pathname = '/media/matheus/DATA/sv_caparica_26052021/run/run01/' # videos path
op_system = 'linux'                    # 'windows' / 'linux'
cameras = '01'                         # '0'= left/ '1'=right / '01'=left and right 
cam_type = 'gopro'                     # 'dslr' / 'smartphone' / 'gopro'
video_format_in = 'MP4'                # 'MP4' / 'mp4' / 'mov' / 'avi' ...
fps_input = 24                         # 10 / 24 / 30 / 50
resample_frames = 'yes'                # 'yes' / 'no'
fps_resampled = 12                     # 10 / 24 / 30 / 50 # if
wind_filter = 'on'                     # 'on' / 'off'
last_frame = 999999                    # last synchronized frame number


# NEED EDIT ONLY FOR VariableFrameRate VIDEOS (i.e Smartphones):
video_format_out = 'mp4'               # 'MP4' / 'mp4' / 'mov' / 'avi' ...
clip_start = 0                         # start in seconds (ref clip)
clip_end =   99999                     # end   in seconds

#############################################################################






print ('---------------------------------------------------')
print ('Creating Directories for frame storage:')
print ('---------------------------------------------------')
try:
    os.makedirs(pathname + 'cam0/')
    os.makedirs(pathname + 'cam1/')
    if resample_frames == 'yes':
        os.makedirs(pathname + 'cam0_resampled/')
        os.makedirs(pathname + 'cam1_resampled/')
except FileExistsError:
    pass




print ('---------------------------------------------------')
print ('Creating/Reading cross-correlation file:')
print ('---------------------------------------------------')

if os.path.isfile(pathname + 'crosscorrelate.praat'):
    print ("crosscorrelate.praat file exist")
else:
    with open(pathname +'crosscorrelate.praat', "a") as f:
        print('form Cross Correlate two Sounds',file=f)
        print('    sentence Input_sound_1',file=f)
        print('    sentence Input_sound_2',file=f)
        print('    real start_time 0',file=f)
        print('    real end_time 30',file=f)
        print('endform',file=f)
        print("Open long sound file... 'input_sound_1$'",file=f)
        print('Extract part: 0,30,"no"',file=f)
        print('Extract one channel... 1',file=f)
        print('sound1 = selected("Sound")',file=f)
        print("Open long sound file... 'input_sound_2$'",file=f)
        print('Extract part: 0,30,"no"',file=f)
        print('Extract one channel... 1',file=f)
        print('sound2 = selected("Sound")',file=f)
        print('select sound1',file=f)
        print('plus sound2',file=f)
        print('Cross-correlate: "peak 0.99", "zero"',file=f)
        print('offset = Get time of maximum: 0, 0, "Sinc70"',file=f)
        print("writeInfoLine: 'offset'",file=f)



clip_list = glob(pathname + '*.'+video_format_in)
count=0
for video in clip_list:
    name_ini = video
    name_fin = pathname + "cam" + str(count) +'.'+ video_format_in
    os.rename(name_ini, name_fin)
    count += 1
clip_list = glob(pathname + '*.'+video_format_in)
print('Video files renamed to cam0/cam1.FORMAT')


## APPLYING TLCC - TIME LAG CROSS-CORRELATION
print ('---------------------------------------------------')
print ('Starting TLCC - TIME LAG CROSS-CORRELATION PROCESS:')
print ('---------------------------------------------------')


# Extract audio from video
os.chdir(pathname)
ref_clip_index = 0                   # first clip used as reference
ref_clip = clip_list[ref_clip_index]
clip_list.pop(ref_clip_index)        # remove the reference clip from the list
# extract the reference audio, which is the audio of the reference clip
os.system("ffmpeg -i {} -vn -acodec pcm_s16le -ar 48000 -ac 2 {}".format(ref_clip,"ref.wav")) #-ar 44100
results = []
results.append((ref_clip, 0)) #the reference clip has an offset of 0

# Apply Wind filter
if wind_filter == 'on':
    sr, x = wavfile.read("ref.wav")      # 16-bit mono 44.1 khz
    b = signal.firwin(101, cutoff=1000, fs=sr, pass_zero=False) # Wind Noise filter - 1000 Hz
    x1 = signal.lfilter(b, [1.0], x[:,0])
    x2 = signal.lfilter(b, [1.0], x[:,1])
    x_new = np.array([x1,x2]).T
    wavfile.write("ref.wav", sr, x_new.astype(np.int16))

for clip in clip_list:
    clipfile = clip.split(".")[0] + ".wav"
    os.system("ffmpeg -i {0} -vn -acodec pcm_s16le -ar 48000 -ac 2 {1}".format(clip,clipfile))
    if wind_filter== 'on':
        sr, x = wavfile.read(clipfile)      # 16-bit mono 44.1 khz
        b = signal.firwin(101, cutoff=1000, fs=sr, pass_zero=False)
        x1 = signal.lfilter(b, [1.0], x[:,0])
        x2 = signal.lfilter(b, [1.0], x[:,1])
        x_new = np.array([x1,x2]).T
        wavfile.write(clipfile, sr, x_new.astype(np.int16))
    if op_system == 'linux':
        command = "/usr/bin/praat --run crosscorrelate.praat ref.wav {}".format(clipfile)
        # command = "praat crosscorrelate.praat ref.wav {}".format(clipfile)
        result = subprocess.check_output(command, shell=True)
        results.append((clip, result.decode("utf-8").split("\n")[0]))# (clip, result.split("\n")[0])
    else:
        command = '"C:\\Program Files\\Praat.exe" --run crosscorrelate.praat ref.wav {}'.format(clipfile)
        result = subprocess.check_output(command)
        results.append((clip, result.decode("utf-16").split("\n")[0]))
for result in results:
    offset = round(float(result[1]),3)
    print('offset:'+str(offset)+' seconds')

    if cam_type == 'smartphone':
        in_name = result[0]
        out_name = in_name.split('.')[0] + '_sync_'+str(fps_resampled)+'.'+video_format_out
        clip_start += offset # new t_0
        os.system("ffmpeg -i {0} -c:a copy -c:v libx264 -crf 0 -vsync vfr -r {1} -ss {2} -to {3} {4} ".format(in_name,str(fps_resampled),str(clip_start),str(clip_end),out_name))

#Print offset
lag = abs(round(offset * fps_input))
print ('number of frames to be removed:' + str(lag))



### EXTRACTING FRAMES
print ('---------------------------------------------------')
print ('Starting frames extraction:')
print ('---------------------------------------------------')

for i in cameras: #0 and 1
    pathname_fig = pathname + 'cam'+i+'/'
    if cam_type == 'smartphone':
        filename = 'cam'+i+'_sync_'+str(fps_resampled)+'.'+video_format_out
    else:
        filename = 'cam'+i+'.'+video_format_in
    # capture video object
    cap = cv2.VideoCapture(pathname + filename)
    count = 0
    while(cap.isOpened()):

        ret, frame = cap.read()
        if ret == False:
            break
        # frame = cv2.flip(frame,0) # flip frame vertically
        # frame = cv2.flip(frame,1) # flip frame honrizontally
        cv2.imwrite(pathname_fig + "%06d.tif" % count, frame)
        print (count)
        count += 1
        if count + 1 == last_frame:
            break
    cap.release()
    cv2.destroyAllWindows()


## SYNCHRONIZATION - removing frames
print ('---------------------------------------------------')
print ('Starting frames synchronization - removing frames:')
print ('---------------------------------------------------')


if cam_type == 'smartphone':
    pass
else:
    if float(results[1][1]) < 0: # if offset is <0 cam_lag=cam0 as cam0 is  the ref clip
        cam_lag = pathname + 'cam0/'
    else:
        cam_lag = pathname + 'cam1/'
    if cameras == '01':
        files = np.sort(glob(cam_lag + '*.tif'))
        for file in files[:lag]:
            os.remove(file)
            print ('removing frame : ' + file)


## RESAMPLING
if cam_type == 'smartphone':
    pass
else:
    if resample_frames == 'yes':
        print ('---------------------------------------------------')
        print ('Starting frames resampling ')
        print ('---------------------------------------------------')
    
        resample_factor = int(fps_input/fps_resampled)
        for i in cameras: #0 and 1
            pathname_fig = pathname + 'cam'+i+'/'
            pathname_to = pathname + 'cam'+i+'_resampled/'
            os.chdir(pathname_fig)
            images = np.sort(glob('*.tif'))
            for file in images[::resample_factor]:
                shutil.copy(pathname_fig + file, pathname_to + file)
                print ('copy image : ' + file)
                os.remove(pathname_fig + file)
                print ('removing image : ' + file) 
            shutil.rmtree(pathname_fig)



## RENAME IMAGE FILES TO WASS INPUT
print ('---------------------------------------------------')
print ('Renaming files to a 06%d sequence [WASS input]')
print ('---------------------------------------------------')

cameras='0'
if cam_type == 'smartphone':
    pass
else:
    for i in cameras: #0 and 1
        if resample_frames == 'yes':
            pathname_renamed = pathname + 'cam'+i+'_resampled/'
        else:
            pathname_renamed = pathname + 'cam'+i+'/'
        files = np.sort(glob(pathname_renamed + '*.tif'))
        count=0
        for file in files:
            name_fin = pathname_renamed + "%06d.tif" % count
            os.rename(file, name_fin)
            print ('renaming : ' + file[-10:] + '   to    ' + name_fin[-10:])
            count += 1



#-----------------------------------------------------------------------------
# ps:
# - If videos has a Constant Frame Rate - CFR (i.e DLSR Pro cameras, GoPro's)
#   then the frames are straight extracted from original video, synchronized, resampled and
#   stored in cam0_resampled and cam1_resampled paths without any new video created.
# - If videos has a Variable Frame Rate - VFR (i.e. smartphones)
#   then is created a new re-encoding synchronized video (you can choose the new
#   output FPS and video format) then the synchronized frames are extracted
#   from the encoded video and stored in cam0 and cam1 paths.
# - A wind noise filter can be applied for better cross-correlation of the audio
#   signal in windy conditions   
#
#
#    If there's a corrupt MP4 video file, run:
#    ffmpeg -i cam0.MP4 -c copy cam01.MP4
#-----------------------------------------------------------------------------


