#!/usr/bin/env python
#
# three_point_turn.py-  a dead reckoning  attempt
# at the three point turn for PiWars. Very simple
# idea, very difficult to perfect! Describes a T-
# shape with the robot and attempts to  get  back
# to where the robot began, facing the other way.
#
# Created Nov 2015 by Finley Watson.

import Lobsang
import time

wheels_direction_left  = (16,    8,  16, -16,  16,   8, 16,    0)
wheels_direction_right = (16,   -8,  16, -16,  16,  -8, 16,    0)
wheels_movement_time   = (3.0, 0.8, 0.7, 1.7, 1.0, 0.8, 3.0, 0.1)

Lobsang.begin(False)
Lobsang.wheels.calibrate_speeds(-0.15)

for i in range(len(wheels_movement_time)):
	Lobsang.wheels.both(wheels_direction_left[i], wheels_direction_right[i])
	time.sleep(wheels_movement_time[i])
