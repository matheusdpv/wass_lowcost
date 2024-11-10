# WASS Low-Cost Repository

This repository provides tools and instructions for synchronizing and processing images from low-cost, consumer-grade video cameras (e.g., GoPro, Smartphones, DSLR) for use in the Wave Acquisition Stereo System (WASS) to acquire 3D sea surface elevation data. The tools support cameras equipped with built-in audio to enable time-synchronization via audio cues. 
This repository can be used with the methods presented in Vieira et al., 2020 and Vieira et al., 2024 for space-time ocean wave observation using low-cost video cameras.

### Repository Contents
1. **`wass_sync.py`, `setup_sync.py`**  
   Python scripts for synchronizing stereo images using audio time-lag cross-correlation, following the method described by Vieira et al. (2020).
   
2. **`WASS_quickstart_guide.pdf`**  
   Step-by-step tutorial for installing WASS, running the system, and post-processing 3D space-time wave data.
   
3. **`input`**  
   Example dataset with synchronized images from GoPro cameras (12 Hz, 1080x720 resolution).
   
4. **`config`**  
   Calibration files including distortion and intrinsic parameters for accurate 3D reconstruction.

### References
1. Vieira, M., Guimarães, P. V., Violante-Carvalho, N., Benetazzo, A., Bergamasco, F., Pereira, H., 2020. A low-cost stereo video system for measuring directional wind waves. Journal of Marine Science and Engineering, 8(11).
2. Vieira, M., Guedes Soares, C., Guimarães, P. V., Bergamasco, F., Campos, R. M., 2024. Nearshore space-time ocean wave observation using low-cost video cameras.



