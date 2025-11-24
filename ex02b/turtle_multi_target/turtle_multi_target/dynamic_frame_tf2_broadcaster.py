import math

from geometry_msgs.msg import TransformStamped

import rclpy
from rclpy.node import Node

from tf2_ros import TransformBroadcaster

class DynamicFrameBroadcaster(Node):

    def __init__(self):
        super().__init__('dynamic_frame_tf2_broadcaster')

        self.turtlename = self.declare_parameter('turtlename', 'turtle').value
        self.carrot = self.declare_parameter('carrot', 'carrot').value

        self.direction = self.declare_parameter('direction', 1).value
        self.radius = self.declare_parameter('radius', 2.0).value

        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.broadcast_timer_callback)
        self.start_time = self.get_clock().now()

    def broadcast_timer_callback(self):
        time = self.get_clock().now()
        seconds = (time - self.start_time).nanoseconds / 1e9
        angle = self.direction * seconds * 1.0

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = self.turtlename
        t.child_frame_id = self.carrot
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

    rclpy.shutdown()