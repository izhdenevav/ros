import math
import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

from custom_action_interfaces.action import CleaningTask

class ActionServerNode(Node):
    def __init__(self):
        super().__init__('action_server')
        self._action_server = ActionServer(self, CleaningTask, 'cleaning_task', self.execute_callback)
        self.current_pose = Pose()
        self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # self.timer = self.create_timer(0.1, self.move_to_goal)
        self.cleaned_points = 0.0

    def pose_callback(self, msg):
        self.current_pose = msg

    def update_cleaned_points(self, last_x, last_y):
        rclpy.spin_once(self, timeout_sec=0.01)
        dx = self.current_pose.x - last_x
        dy = self.current_pose.y - last_y
        dist = math.sqrt(dx**2 + dy**2)
        self.cleaned_points += dist

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = CleaningTask.Feedback()
        result = CleaningTask.Result()

        task_type = goal_handle.request.task_type

        if goal_handle.request.task_type == 'clean_square':
            square_side = goal_handle.request.area_size
            goal_handle.publish_feedback(feedback_msg)
            rclpy.spin_once(self, timeout_sec=1.0)
        elif goal_handle.request.task_type == 'clean_circle':         
            radius = goal_handle.request.area_size
            speed = 1.5
            twist = Twist()
            start_radius = 0.1
            ang_speed = speed / start_radius
            twist = Twist()
        
            while start_radius <= radius:
                center_x = self.current_pose.x
                center_y = self.current_pose.y
                twist.linear.x = speed
                twist.angular.z = ang_speed
                self.vel_pub.publish(twist)

                time.sleep(1)
                self.update_cleaned_points(center_x, center_y)
                feedback_msg.progress_percent = min(int((start_radius / radius) * 100), 100)
                feedback_msg.current_cleaned_points = int(self.cleaned_points)
                feedback_msg.current_x = self.current_pose.x 
                feedback_msg.current_y = self.current_pose.y
                goal_handle.publish_feedback(feedback_msg)

                start_radius += 0.05
                ang_speed = speed / start_radius

            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.vel_pub.publish(twist)
        elif goal_handle.request.task_type == 'return_home':
            target_x = goal_handle.request.target_x
            target_y = goal_handle.request.target_y
            dx = target_x - self.current_pose.x
            dy = target_y - self.current_pose.y
            distance = math.sqrt(dx**2 + dy**2)
            while distance > 0.1:
                feedback_msg.current_x = self.current_pose.x
                feedback_msg.current_y = self.current_pose.y
                goal_handle.publish_feedback(feedback_msg)
                twist = Twist()
                dx = target_x - self.current_pose.x
                dy = target_y - self.current_pose.y
                distance = math.sqrt(dx**2 + dy**2)
                angle_to_target = math.atan2(dy, dx)
                angle_diff = angle_to_target - self.current_pose.theta
                twist.linear.x = 1.0 * distance
                twist.angular.z = 4.0 * angle_diff
                self.vel_pub.publish(twist)
                rclpy.spin_once(self, timeout_sec=0.1)
        else:
            self.get_logger().info('I dunno this type of task...')
            goal_handle.abort()
            result = CleaningTask.Result()
            result.success = False
            return result

        goal_handle.succeed()
        result.success = True
        result.total_distance = self.cleaned_points
        result.cleaned_points = int(self.cleaned_points)
        return result

def main(args=None):
    rclpy.init(args=args)
    node = ActionServerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()