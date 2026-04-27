# Build and Run the Haptic Interface

This is the fastest actionable path for bringing up the Geomagic ROS side.

## Step 1 — enter the workspace
```bash
cd code/haptic/geomagic_touch_ws
```

## Step 2 — build
```bash
catkin_make
source devel/setup.bash
```

## Step 3 — start ROS core
Open a new terminal:
```bash
roscore
```

## Step 4 — launch the left device
Open another terminal:
```bash
cd code/haptic/geomagic_touch_ws
source devel/setup.bash
roslaunch geomagic_control left_device.launch
```

## Step 5 — launch the right device
Open a third terminal:
```bash
cd code/haptic/geomagic_touch_ws
source devel/setup.bash
roslaunch geomagic_control right_device.launch
```

## Step 6 — or launch both together
If both devices are available on the same ROS machine:
```bash
cd code/haptic/geomagic_touch_ws
source devel/setup.bash
roslaunch geomagic_control dual_device_demo.launch
```

## Step 7 — inspect topics
```bash
rostopic list | grep Geomagic
```

Typical namespace-local topics include:
- `/GeomagicLeft/twist`
- `/GeomagicLeft/smoothed_twist`
- `/GeomagicLeft/force_feedback`
- `/GeomagicRight/twist`
- `/GeomagicRight/smoothed_twist`
- `/GeomagicRight/force_feedback`

## Step 8 — quick feedback message test
After the nodes are running, you can manually send a small test force:

```bash
rostopic pub -1 /GeomagicLeft/force_feedback geomagic_control/DeviceFeedback "{force: {x: 0.0, y: 0.0, z: 0.03}, position: {x: 0.0, y: 0.0, z: 0.0}, lock: [false, false, false]}"
```

If your local Geomagic driver setup is correct, the device should respond to the command.
