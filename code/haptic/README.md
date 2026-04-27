# Haptic Module

This folder contains the ROS1 Geomagic Touch interface used in the visuo-haptic digital-twin framework.

## Important files
- `geomagic_touch_ws/src/geomagic_control/src/device_node.cpp` — low-level device bridge
- `geomagic_touch_ws/src/geomagic_control/scripts/force_pub.py` — filtered haptic rendering node
- `geomagic_touch_ws/src/geomagic_control/launch/left_device.launch` — left-hand entry
- `geomagic_touch_ws/src/geomagic_control/launch/right_device.launch` — right-hand entry
- `geomagic_touch_ws/src/geomagic_control/launch/dual_device_demo.launch` — launch both devices
- `geomagic_touch_ws/src/geomagic_control/msg/DeviceFeedback.msg` — force-feedback message
- `geomagic_touch_ws/src/geomagic_description/urdf/geomagic.urdf` — Geomagic URDF asset

## Dependency note
The repository does not redistribute proprietary Geomagic / OpenHaptics drivers. Those must be installed locally on the target machine.
