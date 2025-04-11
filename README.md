# WASS Low-Cost Repository

This repository provides tools and instructions for synchronizing and processing images from low-cost, consumer-grade video cameras (e.g., GoPro, Smartphones, DSLR) for use in the Wave Acquisition Stereo System (WASS) (https://github.com/fbergama/wass) to acquire 3D sea surface elevation data. The tools support cameras equipped with built-in audio to enable time-synchronization via audio cues. 
This repository can be used with the methods presented in Vieira et al., 2020 and Vieira et al., 2025 for space-time ocean wave observation using low-cost video cameras.

### Repository Contents
1. **`wass_sync.py`, `setup_sync.py`**  
   Python scripts for synchronizing stereo images using audio time-lag cross-correlation, following the method described by Vieira et al. (2025).
   
2. **`WASS_quickstart_guide.pdf`**  
   Step-by-step tutorial for installing WASS, running the system, and post-processing 3D space-time wave data.
   
3. **`input`**  
   Example dataset with synchronized images from GoPro cameras (12 Hz, 1080x720 resolution).
   
4. **`config`**  
   Calibration files including distortion and intrinsic parameters for accurate 3D reconstruction.


---

### Stereo Rig Deployment
For optimal results, set up the stereo rig with two cameras positioned side-by-side, ensuring their optical axes are parallel. Mount the rig at a relatively high altitude above sea level to reduce shadowing effects, with the cameras angled slightly downward toward the horizon. Accurately measuring the distance between the cameras (baseline) is crucial, as this measurement is essential for scaling sea surface elevation data.

### Recording Guidelines
- Use fixed focal length lenses, set to infinity focus.
- Adjust exposure settings to match local lighting conditions for sharper images with balanced brightness.
- Grayscale or colored images supported. 

### Image Synchronization
To synchronize images:
1. Edit `setup_sync.py` and place it in the same directory as `wass_sync.py`.
2. Run the synchronization script with: `python wass_sync.py`.

**Requirements:** OpenCV (compatible with Python <= 3.7), ffmpeg, Praat (for time-lag correlation).

---


### References
1. Vieira, M., Guedes Soares, C., Guimarães, P. V., Bergamasco, F., & Campos, R. M., 2025. Nearshore space-time ocean wave observation using low-cost video cameras. Coastal Engineering, 197, 104694. https://doi.org/10.1016/j.coastaleng.2024.104694
2.  Vieira, M., Guimarães, P. V., Violante-Carvalho, N., Benetazzo, A., Bergamasco, F., Pereira, H., 2020. A low-cost stereo video system for measuring directional wind waves. Journal of Marine Science and Engineering, 8(11).
3. Bergamasco, F., Torsello, A., Sclavo, M., Barbariol, F., Benetazzo, A., 2017. WASS: An open-source pipeline for 3D stereo reconstruction of ocean waves, Computers and Geosciences, vol. 107, pp. 28-36.



