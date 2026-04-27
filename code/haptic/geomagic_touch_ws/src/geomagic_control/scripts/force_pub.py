#!/usr/bin/env python3
import time
import numpy as np
import rospy
from geometry_msgs.msg import Twist
from tf2_msgs.msg import TFMessage
from geomagic_control.msg import DeviceFeedback


class ForceFeedbackPublisher:
    """Publish filtered haptic force cues and a smoothed twist topic.

    This script keeps the original logic from the provided package while
    exposing topic names as ROS parameters so the same package can be used for
    the left and right Geomagic devices.
    """

    def __init__(self):
        rospy.init_node('force_feedback_publisher')

        # Force model parameters (kept from the provided package).
        self.threshold_1 = rospy.get_param('~threshold_1', 0.08)
        self.threshold_2 = rospy.get_param('~threshold_2', 0.1)
        self.angular_x = rospy.get_param('~angular_x', -12000.0)
        self.angular_y = rospy.get_param('~angular_y', -16.18)
        self.linear_z = rospy.get_param('~linear_z', -1568.0)
        self.force_ratio = rospy.get_param('~force_ratio', 0.0022)
        self.damping_coefficient = rospy.get_param('~damping_coefficient', 0.0)
        self.alpha = rospy.get_param('~force_alpha', 0.05)
        self.twist_alpha = rospy.get_param('~twist_alpha', 0.05)

        # Topic contract.
        ot_topic = rospy.get_param('~ot_topic', '/secondOTposition')
        robot_topic = rospy.get_param('~robot_topic', '/robot02')
        xform_topic = rospy.get_param('~xform_topic', '/xform')
        dyna_topics = rospy.get_param(
            '~dynamic_obstacle_topics',
            ['/DynaOb01', '/DynaOb02', '/DynaOb03', '/DynaOb04']
        )
        twist_topic = rospy.get_param('~twist_topic', 'twist')
        smoothed_twist_topic = rospy.get_param('~smoothed_twist_topic', 'smoothed_twist')
        force_feedback_topic = rospy.get_param('~force_feedback_topic', 'force_feedback')

        self.filtered_force = np.array([0.0, 0.0, 0.0])
        self.filtered_linear = np.array([0.0, 0.0, 0.0])
        self.filtered_angular = np.array([0.0, 0.0, 0.0])
        self.previous_distance = None
        self.previous_time = None

        self.ot_centre1_pos = None
        self.cube1_pos = None
        self.dynaob_positions = [None] * len(dyna_topics)
        self.xform_pos = None

        rospy.Subscriber(ot_topic, TFMessage, self.ot_centre1_callback)
        rospy.Subscriber(robot_topic, TFMessage, self.cube1_callback)
        for idx, topic in enumerate(dyna_topics):
            rospy.Subscriber(topic, TFMessage, self.dynaob_callback, callback_args=idx)
        rospy.Subscriber(xform_topic, TFMessage, self.xform_callback)
        rospy.Subscriber(twist_topic, Twist, self.twist_callback)

        self.force_feedback_publisher = rospy.Publisher(force_feedback_topic, DeviceFeedback, queue_size=1)
        self.smoothed_twist_publisher = rospy.Publisher(smoothed_twist_topic, Twist, queue_size=1)

    def ot_centre1_callback(self, msg):
        for transform in msg.transforms:
            self.ot_centre1_pos = np.array([
                transform.transform.translation.x,
                transform.transform.translation.y,
                transform.transform.translation.z,
            ])
        self.calculate_and_publish_force()

    def cube1_callback(self, msg):
        for transform in msg.transforms:
            self.cube1_pos = np.array([
                transform.transform.translation.x,
                transform.transform.translation.y,
                transform.transform.translation.z,
            ])
        self.calculate_and_publish_force()

    def dynaob_callback(self, msg, index):
        for transform in msg.transforms:
            self.dynaob_positions[index] = np.array([
                transform.transform.translation.x,
                transform.transform.translation.y,
                transform.transform.translation.z,
            ])

    def xform_callback(self, msg):
        for transform in msg.transforms:
            self.xform_pos = np.array([
                transform.transform.translation.x,
                transform.transform.translation.y,
                transform.transform.translation.z,
            ])

    def calculate_force(self, distance):
        if distance < self.threshold_1:
            return -(self.angular_x * distance)
        if self.threshold_1 <= distance < self.threshold_2:
            return -(self.angular_y / (distance ** 2)) + self.linear_z
        return 0.0

    def calculate_damping_force(self, current_distance, force_direction):
        if self.previous_distance is None or self.previous_time is None:
            self.previous_distance = current_distance
            self.previous_time = time.time()
            return np.array([0.0, 0.0, 0.0])

        current_time = time.time()
        delta_time = current_time - self.previous_time
        distance_change_rate = (current_distance - self.previous_distance) / delta_time if delta_time > 0 else 0.0
        damping_force_magnitude = -self.damping_coefficient * distance_change_rate
        self.previous_distance = current_distance
        self.previous_time = current_time
        return damping_force_magnitude * force_direction

    def calculate_and_publish_force(self):
        if self.ot_centre1_pos is None or self.cube1_pos is None:
            return

        distance = np.linalg.norm(self.cube1_pos - self.ot_centre1_pos)
        if distance <= 1e-9:
            return

        force_magnitude = self.calculate_force(distance)
        force_direction = -(self.ot_centre1_pos - self.cube1_pos) / distance
        raw_force = force_magnitude * force_direction
        damping_force = self.calculate_damping_force(distance, force_direction)
        total_force = raw_force + damping_force
        self.filtered_force = self.alpha * total_force + (1 - self.alpha) * self.filtered_force

        feedback_msg = DeviceFeedback()
        feedback_msg.force.x = self.filtered_force[0] * self.force_ratio
        feedback_msg.force.y = self.filtered_force[1] * self.force_ratio
        feedback_msg.force.z = self.filtered_force[2] * self.force_ratio
        self.force_feedback_publisher.publish(feedback_msg)

    def twist_callback(self, msg):
        new_linear = np.array([msg.linear.x, msg.linear.y, msg.linear.z])
        new_angular = np.array([msg.angular.x, msg.angular.y, msg.angular.z])
        self.filtered_linear = self.twist_alpha * new_linear + (1 - self.twist_alpha) * self.filtered_linear
        self.filtered_angular = self.twist_alpha * new_angular + (1 - self.twist_alpha) * self.filtered_angular

        smoothed_msg = Twist()
        smoothed_msg.linear.x = self.filtered_linear[0]
        smoothed_msg.linear.y = self.filtered_linear[1]
        smoothed_msg.linear.z = self.filtered_linear[2]
        smoothed_msg.angular.x = self.filtered_angular[0]
        smoothed_msg.angular.y = self.filtered_angular[1]
        smoothed_msg.angular.z = self.filtered_angular[2]
        self.smoothed_twist_publisher.publish(smoothed_msg)


if __name__ == '__main__':
    try:
        ForceFeedbackPublisher()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
