# Lane detection using opencv

# Todo:
1. Set camera parameters to reduce lighting flickering

# Algorithm:
1. Grab ROI region (around 1/3 of the frame @ y axis, and 1/2 of the frame @ the x axis, both centered)
2. Threshold color image
3. Blur to smooth image
4. Hough lines
5. Gets bounding boxes within the hough lines
6. PID via error from center
