import math

from geometry_msgs.msg import TransformStamped

import rclpy
from rclpy.node import Node

from tf2_ros import TransformBroadcaster


class DynamicFrameBroadcaster(Node):

    def __init__(self):
        super().__init__('dynamic_frame_tf2_broadcaster')
        self.declare_parameter('radius', 2.0)
        self.declare_parameter('direction_of_rotation', 1)

        self.radius = self.get_parameter('radius').get_parameter_value().double_value
        self.direction = self.get_parameter('direction_of_rotation').get_parameter_value().integer_value

        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.broadcast_timer_callback)
        self.start_time = self.get_clock().now()

    def broadcast_timer_callback(self):
        seconds, _ = self.get_clock().now().seconds_nanoseconds() 
        # angle = self.direction * seconds * math.pi
        # elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
        angle = self.direction * seconds * math.pi

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'turtle1'
        t.child_frame_id = 'carrot1'
        t.transform.translation.x = self.radius * math.sin(angle)
        t.transform.translation.y = self.radius * math.cos(angle)
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = DynamicFrameBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
