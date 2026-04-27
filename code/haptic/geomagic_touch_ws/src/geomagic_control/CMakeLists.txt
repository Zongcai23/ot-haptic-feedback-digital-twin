cmake_minimum_required(VERSION 3.0.2)
project(geomagic_control)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  rosconsole
  tf
  urdf
  message_generation
  geometry_msgs
  sensor_msgs
)

add_message_files(
  FILES
  DeviceButtonEvent.msg
  DeviceFeedback.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs message_runtime geometry_msgs rosconsole tf urdf
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(device_node src/device_node.cpp)
add_dependencies(device_node ${PROJECT_NAME}_generate_messages_cpp)

target_link_libraries(device_node
  ${catkin_LIBRARIES}
  HD HL HDU rt ncurses
)

catkin_install_python(PROGRAMS
  scripts/force_pub.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
