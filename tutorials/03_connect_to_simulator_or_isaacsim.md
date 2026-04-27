# Connect to a Simulator or Isaac Sim

The haptic package is useful only when the simulator side provides the state topics expected by the force-rendering node.

## Topic contract used in this repository
The cleaned launch files are configured as follows:

### Left-hand loop
- OT topic: `/firstOTposition`
- robot topic: `/robot01`
- namespace: `/GeomagicLeft`

### Right-hand loop
- OT topic: `/secondOTposition`
- robot topic: `/robot02`
- namespace: `/GeomagicRight`

### Shared simulator topic
- `/xform`

## Message type
The current `force_pub.py` subscribes to simulator state as:
- `tf2_msgs/TFMessage`

That means the simulator should publish TF-style transforms for the trap and robot positions.

## What the haptic node outputs
Within each Geomagic namespace, the ROS side publishes:
- `smoothed_twist` for filtered operator commands
- `force_feedback` for the rendered haptic cue

## Minimal integration checklist
1. Make sure your simulator publishes `TFMessage` transforms on `/firstOTposition` or `/secondOTposition`.
2. Make sure the corresponding robot state is published on `/robot01` or `/robot02`.
3. Launch `left_device.launch` and `right_device.launch`.
4. Confirm that the topics are alive:
   ```bash
   rostopic hz /firstOTposition
   rostopic hz /robot01
   rostopic hz /GeomagicLeft/smoothed_twist
   ```
5. If required, modify topic names directly in:
   - `geomagic_headless.launch`
   - `left_device.launch`
   - `right_device.launch`
   - `scripts/force_pub.py`

## Practical note for Isaac Sim users
If you already publish TF-style state from Isaac Sim, the quickest path is usually:
- keep Isaac Sim responsible for OT / robot state publishing
- keep this ROS package responsible for device-side input and haptic feedback
- bridge the two using the topic contract above
