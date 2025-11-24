import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

class SwitchTarget(Node):
    def __init__(self):
        super().__init__('switch_target')

        self.turtle_name = 'turtle2'
        self.targets = ['carrot1', 'carrot2', 'static_target']
        self.current_idx = 0
        self.switch_threshold = self.declare_parameter('switch_threshold', 1.0).value

        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.publisher = self.create_publisher(Twist, f'/{self.turtle_name}/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

        listener = keyboard.Listener(on_press=self._on_press)
        listener.daemon = True
        listener.start()

    def timer_callback(self):
        target = self.targets[self.current_idx]

        try:
            trans = self.buffer.lookup_transform(
                self.turtle_name, target, rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.1))
        except TransformException as ex:
            return

        x = trans.transform.translation.x
        y = trans.transform.translation.y
        distance = math.hypot(x, y)
        angle = math.atan2(y, x)

        msg = Twist()
        msg.linear.x = min(2.0, distance * 1.5)
        msg.angular.z = 4.0 * angle
        self.publisher.publish(msg)

        if distance < self.switch_threshold:
            self.current_idx = (self.current_idx + 1) % len(self.targets)
            new_target = self.targets[self.current_idx]

def main():
    rclpy.init()
    node = SwitchTarget()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()