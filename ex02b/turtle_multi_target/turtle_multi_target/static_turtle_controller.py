import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class StaticTurtleController(Node):
    def __init__(self):
        super().__init__('static_turtle_controller')
        
        topic = f'/turtle3/cmd_vel'
        
        self.publisher = self.create_publisher(Twist, topic, 10)
        self.timer = self.create_timer(0.05, self.publish_zero_velocity)

    def publish_zero_velocity(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = StaticTurtleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()