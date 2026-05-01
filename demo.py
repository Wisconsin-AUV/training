import cv2
import numpy as np

# the goal of this task is to compute a waypoint (x, y, z)
# in the plane of the gate such that the sub can pass through it
# coordinates are relative to the camera (which is at 0, 0, 0)
# and are computed using the pinhole camera model and a depth map
#
# you are provided with all:
# - camerae intrinsics
# - a single marker detection
# - a depth map
# - our subs dimensions
# -


# synthetic depth map ( not noisy )
# In competition this comes from the ZED X mini stereo depth cam
# Here we build a plausible scene so the numbers are realistic.
depth_raw = cv2.imread("images/depth_map.png", cv2.IMREAD_GRAYSCALE)  # shape (718, 1278), uint8
scale = 2.75 / 38   # 0.07237 m/pixel
depth_map = depth_raw * scale
# the depth map is a 2d array image
# with each pixel corresponding to distance from camera in meters
print("Z = ", depth_map[385, 749])
#camera intrinsics(these are estimated values which will suffice for this training):
IMAGE_W, IMAGE_H = 1278, 718
fx, fy = 460.0, 460.0
cx, cy = 639.0, 359.0

# these are the coordinates of the right marker which our perception pipeline has detected
# it is a circular detection represented by the center (x,y) and its radius (r)
# the marker is 30cm by 30cm
marker = (749, 385, 35) # (x , y , r) in pixels

# dimensions of the sub (meters)
sub_height = 0.7
sub_width = 0.8
sub_length = 0.5

# something to note in general:
# Camera frame: X left-right, Y up-down, Z - the depth (forward - backward)

# Pinhole formula:
#   X = (u - cx) * Z / fx
#   Y = (v - cy) * Z / fy
#   Z = depth value fetched above


# --- what people would have to write to compute depth

marker_edge = (385+35 - cy) * depth_map[385, 749] / fy

target_y = marker_edge + sub_height/2 + 0.15

v = (target_y * fy / depth_map[385, 749] ) + cy


# visualization of code (you don't need to change anything here)
# do look through this tho it works on the pinhole camera model
img = cv2.imread("images/gate_img.png")

u_marker, v_marker, r_px = marker
Z = depth_map[v_marker, u_marker]

sub_h_px = int(sub_height * fy / Z)
sub_w_px = int(sub_width  * fx / Z)

top_left     = (u_marker - sub_w_px // 2, int(v) - sub_h_px // 2)
bottom_right = (u_marker + sub_w_px // 2, int(v) + sub_h_px // 2)

cv2.circle(img, (u_marker, int(v)), 4, (0, 255, 0), -1)
cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

cv2.imshow("gate_img", img)
cv2.waitKey(0)