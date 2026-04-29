# Prerequisites

This repository is organised for a **standard GitHub code release**, not a standalone installer. Before running the haptic module, prepare the host machine as follows.

## Operating system
- Ubuntu 20.04/22.04 is recommended.

## Core ROS packages
Install ROS and common dependencies first:

```bash
sudo apt update
sudo apt install -y   ros-noetic-desktop-full   ros-noetic-tf   ros-noetic-robot-state-publisher   ros-noetic-urdf   ros-noetic-sensor-msgs   ros-noetic-geometry-msgs   ros-noetic-std-msgs   python3-catkin-tools
```

## Geomagic / OpenHaptics
This repository does **not** redistribute proprietary drivers. You still need a working local installation of:
- Geomagic Touch device drivers
- OpenHaptics SDK or equivalent local dependency expected by your workstation

## Optional simulator side
If you want to reproduce the paper-style loop, you also need a simulator or digital twin that can publish the OT / robot state topics expected by `force_pub.py`.
