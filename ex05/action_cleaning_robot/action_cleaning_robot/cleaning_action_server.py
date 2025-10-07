import math

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

    def pose_callback(self, msg):
        self.current_pose = msg

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = CleaningTask.Feedback()
        feedback_msg.current_x = self.current_pose.x
        feedback_msg.current_y = self.current_pose.y

        if goal_handle.request.task_type == 'clean_square':
            square_side = goal_handle.request.area_size
            goal_handle.publish_feedback(feedback_msg)
            rclpy.spin_once(self, timeout_sec=1.0)
        elif goal_handle.request.task_type == 'clean_circle':
            start_radius = goal_handle.request.area_size
            self.get_logger().info(f'radius {start_radius}')
            center_x = self.current_pose.x + start_radius
            center_y = self.current_pose.y 
            radius = start_radius
            angular_speed = 2.0
            linear_speed_base = 1.0
            radius_step = 0.02
            min_linear_speed = 0.1
            num_steps = int(start_radius / radius_step) * 3
            for step in range(num_steps):
                if goal_handle.is_cancel_requested:
                    result = CleaningTask.Result()
                    result.success = False
                    goal_handle.canceled()
                    return result

                radius = max(0.0, radius - radius_step)
                feedback_msg.current_x = self.current_pose.x
                feedback_msg.current_y = self.current_pose.y
                goal_handle.publish_feedback(feedback_msg)

                dx = center_x - self.current_pose.x
                dy = center_y - self.current_pose.y
                distance_to_center = math.sqrt(dx**2 + dy**2)

                if distance_to_center < 0.1 or radius < 0.1:
                    break

                twist = Twist()

                linear_speed = linear_speed_base * (radius / start_radius)
                twist.linear.x = max(min_linear_speed, linear_speed)
                twist.angular.z = angular_speed
                
                self.vel_pub.publish(twist)

                rclpy.spin_once(self, timeout_sec=0.05)
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
        result = CleaningTask.Result()
        result.success = True
        return result

def main(args=None):
    rclpy.init(args=args)
    node = ActionServerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()