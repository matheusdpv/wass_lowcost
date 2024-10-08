'''
author: matheus vieira - 2019
    last update: 2024

# HOW TO RUN:
    - Edit file 'setup_sync.py' and place in the same path of 'wass_sync.py' file
    - Change to directory where 'setup_sync.py' and 'wass_sync.py' are then, run:
        python wass_sync.py

# REQUIREMENTS:
    - OpenCV (python<=3.7):   conda install -c conda-forge opencv
    - Praat software:         sudo apt-get install praat
    - FFmpeg software:        sudo apt-get install ffmpeg

# DO:
    - Frames extraction
    - Frames synchronization (using audio recorded from video)
    - Apply audio wind filter before frame synchronization      (optional)
    - Frames resampling                                         (optional)

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


import os
import numpy as np
import subprocess
from glob import glob
import cv2
from scipy.io import wavfile
from scipy import signal
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from setup_sync import *


print ('---------------------------------------------------')
print ('Creating Directories for frame storage:')
print ('---------------------------------------------------')
try:
    os.makedirs(pathname + 'cam0/')
    os.makedirs(pathname + 'cam1/')
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
        print('    real start_time '+ str(audio_sync_cc_window_ini), file=f)
        print('    real end_time '+ str(audio_sync_cc_window_fin), file=f)
        print('endform',file=f)
        print("Open long sound file... 'input_sound_1$'",file=f)
        print('Extract part: ' + str(audio_sync_cc_window_ini) + ',' + str(audio_sync_cc_window_fin) + ',"no"', file=f)
        print('Extract one channel... 1',file=f)
        print('sound1 = selected("Sound")',file=f)
        print("Open long sound file... 'input_sound_2$'",file=f)
        print('Extract part: ' + str(audio_sync_cc_window_ini) + ',' +str(audio_sync_cc_window_fin)+',"no"', file=f)
        print('Extract one channel... 1',file=f)
        print('sound2 = selected("Sound")',file=f)
        print('select sound1',file=f)
        print('plus sound2',file=f)
        print('Cross-correlate: "peak 0.99", "zero"',file=f)
        print('offset = Get time of maximum: 0, 0, "Sinc70"',file=f)
        print("writeInfoLine: 'offset'",file=f)


print ('---------------------------------------------------')
print('Rename video files to cam0/cam1.FORMAT')
print ('---------------------------------------------------')

# List and rename video files
clip_list_original = np.sort(glob(pathname + '*.'+video_format_input))

for video in clip_list_original:
    name_ini = video
    name_fin = pathname + "cam" + str(count) +'.'+ video_format_input
    os.rename(name_ini, name_fin)
    
clip_list = np.sort(glob(pathname + '*.'+video_format_input))


## APPLYING TLCC - TIME LAG CROSS-CORRELATION
print ('---------------------------------------------------')
print ('Starting TLCC - TIME LAG CROSS-CORRELATION PROCESS:')
print ('---------------------------------------------------')


# Extract audio from video [tested in smartphones,gopros, dslr cameras_id]
os.chdir(pathname)
count=0
for wav_file in clip_list:
  if audio_stereo == 'off':
      os.system("ffmpeg -i {} -map_channel 0.1.1 {}".format(wav_file,"wav_file_"+str(count)+".wav")) #-ar 48000
  if audio_stereo == 'on':
      os.system("ffmpeg -i {} -vn -acodec pcm_s16le -ar 48000 -ac 2 {}".format(wav_file,"wav_file_"+str(count)+".wav"))
      count += 1

wav_list = np.sort(glob(pathname + '*.wav'))
results = []
results.append((wav_list[0], 0)) #the reference clip has an offset of 0


# Apply wind filter in the two audio series
count=0
for wav_file in wav_list:
  if audio_wind_filter == 'on':
    sr, x = wavfile.read("wav_file_"+str(count)+".wav")      # 16-bit mono 44.1 khz
    b = signal.firwin(101, cutoff=1000, fs=sr, pass_zero=False) # Wind Noise filter - 1000 Hz
    x1 = signal.lfilter(b, [1.0], x[:,0])
    x2 = signal.lfilter(b, [1.0], x[:,1])
    x_new = np.array([x1,x2]).T
    wavfile.write("wav_file_"+str(count)+".wav", sr, x_new.astype(np.int16))
    count += 1

# Apply cross-correlation and find the time delay between audio series
if op_system == 'linux' or 'mac':
  command = "/usr/bin/praat --run crosscorrelate.praat wav_file_0.wav {} 0.99 0".format(wav_list[1])
  # command = "praat crosscorrelate.praat ref.wav {}".format(clipfile)
  result = subprocess.check_output(command, shell=True)
  # result = subprocess.run(command, shell=True, capture_output=True)
  results.append((wav_file, result.decode("utf-8").split("\n")[0]))# (clip, result.split("\n")[0])
if op_system == 'windows':
  command = '"C:\\Program Files\\Praat.exe" --run crosscorrelate.praat wav_file_0.wav {}'.format(wav_file[1])
  result = subprocess.check_output(command)
  results.append((wav_file, result.decode("utf-16").split("\n")[0]))

offset = round(float(results[1][1]),3)


if camera_type == 'smartphone':
  in_name = result[0]
  out_name = in_name.split('.')[0] + '_sync_'+str(video_fps_output)+'.'+video_format_output
  clip_start += offset # new t_0
  os.system("ffmpeg -i {0} -c:a copy -c:v libx264 -crf 0 -vsync vfr -r {1} -ss {2} -to {3} {4} ".format(in_name,str(video_fps_output),str(clip_start),str(clip_end),out_name))

#Print offset
resample_factor = int(video_fps_input/video_fps_output)
if abs(offset) < 1/video_fps_input:
    lag = 0
    print ('number of frames to be removed: 0')
else:
    lag = round(offset * video_fps_input)
    print ('----------------------------------------------------------------------------')
    print('offset:'+str(offset) +' seconds')
    print ('number of non sychronized frames recorded in ' +str(video_fps_input)+ ' fps: ' + str(abs(lag)))
    print ('number of non sychronized frames after resampling to ' +str(video_fps_input/resample_factor) + ' fps: ' + str(abs(lag/resample_factor)) )
    print ('----------------------------------------------------------------------------')


### EXTRACTING FRAMES
print ('---------------------------------------------------')
print ('Starting frames extraction:')
print ('---------------------------------------------------')

# READ VIDEO FILE
for i in camera_id: #0 and 1
    pathname_fig = pathname + 'cam'+i+'/'
    if camera_type == 'smartphone':
        filename = 'cam'+i+'_sync_'+str(video_fps_output)+'.'+video_format_output
        resample_factor = 1
    else:
        filename = 'cam'+i+'.'+video_format_input
        cap = cv2.VideoCapture(pathname + filename)
        count = 0
    print (pathname_fig, filename)


    if lag > 0 and filename == 'cam0.'+ str(video_format_output):
      image_extracted_first_plot = image_extracted_first
    if lag > 0 and filename == 'cam1.'+ str(video_format_output):
      image_extracted_first_plot = image_extracted_first + lag
    if lag < 0 and filename == 'cam0.'+ str(video_format_output):
      image_extracted_first_plot = image_extracted_first + np.abs(lag)
    if lag < 0 and filename == 'cam1.'+ str(video_format_output):
      image_extracted_first_plot = image_extracted_first
    if np.abs(lag) < 1/video_fps_input:
      print ('VIDEO FILES ARE ALREADY SYNCHRONIZED')
      pass


    for ii in range(image_extracted_first_plot, image_extracted_last,resample_factor):
        cap.set(1, ii)
        ret, frame = cap.read()
        if ret == False:
            break
        if image_format_output == 'jpg':
            cv2.imwrite(pathname_fig + "%06d.jpg"  % count, frame)
        if image_format_output == 'tif':
            cv2.imwrite(pathname_fig + "%06d.tif"  % count, frame)
        if image_format_output == 'png':
            cv2.imwrite(pathname_fig + "%06d.png"  % count, frame)
        print ('Extracting frame from camera ' +str(i)+': ' +str(count))
        count += 1
    cap.release()
    # cv2.destroyAllWindows()

# Rename the files to original filename
for i in range(len(clip_list)):
    name_ini = clip_list[i]
    name_fin = clip_list_original[i]
    os.rename(name_ini, name_fin)
    

if op_system == 'linux':    
    with open(pathname +f'sync_log.txt', "a") as f:
        print('Frames extracted: ' + str(image_extracted_last-image_extracted_first),file=f)
        print ('video_format_input: '+video_format_input,file=f)    
        if camera_type == 'smartphone':
          print ('video_format_output: '+video_format_output,file=f)    
        print ('camera_type = ' + camera_type, file=f)
        print ('video_fps_input: ' + str(video_fps_input), file=f)
        print ('video_fps_output: ' + str(video_fps_output), file=f) 
        print ('image_format_output: ' + image_format_output, file=f) 
        print ('offset in seconds: ' + str(offset),file=f)
        print ('offset in number of frames before resampling: ' + str(lag),file=f)
        print ('offset in number of frames after resampling: ' + str(lag/resample_factor),file=f)
        if lag > 0:
          print ('frames removed from cam1 [lag > 0]',file=f)
        if lag < 0:
          print ('frames removed from cam0 [lag < 0]',file=f)   
        print ('audio_sync_cc_window_ini: ' +str(audio_sync_cc_window_ini),file=f)
        print ('audio_sync_cc_window_fin: ' +str(audio_sync_cc_window_fin),file=f)
        print ('audio_wind_filter: ' + audio_wind_filter,file=f)

print ('----------------------------')
print ('sync_log.txt file created')
print ('----------------------------')


print('RUN: COMPLETE')
