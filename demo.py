# Simulating a PID depth controller for an underwater robot
import numpy as np
import matplotlib.pyplot as plt

# simulation settings
dt          = 0.05          # time step (seconds)
t_end       = 20.0          # total simulation time (seconds)
time        = np.arange(0, t_end, dt)

# plant (1D, simplified)
# mass * a = thrust - damping * velocity
mass        = 30.0   # kg
damping     = 15.0    # N·s/m  (drag)
max_thrust  = 67.0   # N      (thruster limit) *this is the real value

# target depth in meters, 0 at surface
target_depth = -2.0



########### ADD CODE HERE ##########################################
# This task involves implementing a PID controller for an AUV
# that must hold a target depth. Fill in the lines below using
# the comments and the PID formula:
#   output = Kp*error + Ki*integral + Kd*derivative
# Reference: https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller

# PID params (tune them)
Kp = ?
Ki = ?
Kd = ?

# State variables
depth       = 0.0           # start at the surface
velocity    = 0.0           # vertical velocity (m/s)

# PID memory
integral    = 0.0
prev_error  = 0.0

# Storage for plotting
depths      = []
targets     = []
thrusts     = []
errors      = []

# sim loop
for t in time:

    # compute error
    error = ?

    # compute integral and derivative of error
    integral   = ?
    derivative = ?

    # use PID control law to calculate input thrust
    input_thrust = ?

    # clip thrust to thruster limits so we don't exceed hardware   
    ???

    # update previous error for next iteration
    prev_error = error

    # forward dynamics (Euler integration)
    acceleration = ?
    velocity     = velocity + acceleration * dt
    depth        = depth    + velocity    * dt

    # record state for plotting
    depths.append(depth)
    targets.append(target_depth)
    thrusts.append(input_thrust)
    errors.append(error)

####################################################################
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

axes[0].plot(time, depths,  label='Actual depth',  color='steelblue')
axes[0].plot(time, targets, label='Target depth',  color='tomato', linestyle='--')
axes[0].set_title('Depth Response')
axes[0].set_xlabel('Time (s)')
axes[0].set_ylabel('Depth (m)')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(time, errors, color='darkorange')
axes[1].axhline(0, color='black', linewidth=0.8, linestyle='--')
axes[1].set_title('Depth Error Over Time')
axes[1].set_xlabel('Time (s)')
axes[1].set_ylabel('Error (m)')
axes[1].grid(True)

axes[2].plot(time, thrusts, color='seagreen')
axes[2].axhline( max_thrust, color='red', linewidth=0.8, linestyle='--', label='Thrust limit')
axes[2].axhline(-max_thrust, color='red', linewidth=0.8, linestyle='--')
axes[2].set_title('Thruster Output')
axes[2].set_xlabel('Time (s)')
axes[2].set_ylabel('Thrust (N)')
axes[2].legend()
axes[2].grid(True)

plt.suptitle('AUV PID Depth Controller Simulation', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()