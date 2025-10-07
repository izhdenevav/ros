import math

import rclpy
from rclpy.node import Node 
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class MyNode(Node):
    def __init__(self):
        super().__init__('move_to_goal')
        self.declare_parameter('x', 0.0)
        self.declare_parameter('y', 0.0)
        self.declare_parameter('theta', 0.0)

        self.x = self.get_parameter('x').get_parameter_value().double_value
        self.y = self.get_parameter('y').get_parameter_value().double_value
        self.theta = math.radians(self.get_parameter('theta').get_parameter_value().double_value)

        self.get_logger().info(f'Params: {self.x}, {self.y}, {self.theta}')

        self.current_pose = Pose()
        self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        self.vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.timer = self.create_timer(0.1, self.move_to_goal)

    def pose_callback(self, msg):
        self.current_pose = msg
    
    def move_to_goal(self):
        dx = self.x - self.current_pose.x
        dy = self.y - self.current_pose.y
        distance = math.sqrt(dx**2 + dy**2)
        angle_to_goal = math.atan2(dy, dx)
        angle_error = angle_to_goal - self.current_pose.theta

        while angle_error > math.pi:
            angle_error -= 2 * math.pi
        while angle_error < -math.pi:
            angle_error += 2 * math.pi

        self.get_logger().info(f'Current: x={self.current_pose.x:.2f}, y={self.current_pose.y:.2f}, theta={self.current_pose.theta:.2f}')
        self.get_logger().info(f'Distance: {distance:.2f}, Angle error: {angle_error:.2f}')

        twist = Twist()

        if distance > 0.1:
            if math.fabs(angle_error) > 0.1:
                twist.angular.z = 1.0 if angle_error > 0 else -1.0
            else:
                twist.linear.x = 1.0 * distance
        else:
            theta_error = self.theta - self.current_pose.theta

            while theta_error > math.pi:
                angle_error -= 2 * math.pi
            while angle_error < -math.pi:
                angle_error += 2 * math.pi

            if math.fabs(theta_error) > 0.1:
                twist.angular.z = 1.0 if theta_error > 0 else -1.0
            else:
                self.get_logger().info('Goal reached!')
                self.timer.cancel()

        self.vel_pub.publish(twist)

def main():
    rclpy.init()
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()