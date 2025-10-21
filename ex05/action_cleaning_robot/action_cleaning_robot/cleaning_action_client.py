import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from custom_action_interfaces.action import CleaningTask

class ActionClientNode(Node):
    def __init__(self):
        super().__init__('action_client')
        self._action_client = ActionClient(self, CleaningTask, 'cleaning_task')
        self.step = 0

    def send_goal(self, task_type, area_size, target_x, target_y):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()
        
        goal_msg = CleaningTask.Goal()
        goal_msg.task_type = task_type
        goal_msg.area_size = area_size
        goal_msg.target_x = target_x
        goal_msg.target_y = target_y

        self.get_logger().info('Sending goal...')
        future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(
            f'Feedback: percent {feedback_msg.feedback.progress_percent}%, '
            f'cleaned {feedback_msg.feedback.current_cleaned_points}, '
            f'pos ({feedback_msg.feedback.current_x:.2f}, {feedback_msg.feedback.current_y:.2f})')

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.success}')
        self.get_logger().info(f'\tCleaned_points: {result.cleaned_points}')
        self.get_logger().info(f'\tTotal_distance: {result.total_distance}')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = ActionClientNode()
    node.send_goal(task_type='clean_circle', area_size=3.0, target_x=10.0, target_y=10.0)  
    rclpy.spin(node)

if __name__ == '__main__':
    main()