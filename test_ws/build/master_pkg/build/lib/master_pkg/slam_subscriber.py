import string
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'location_topic',
            self.listener_callback,
            10)

        self.subscription2 = self.create_subscription(
            String,
            'direction_topic',
            self.listener_callback2,
            10)

        self.subscription3 = self.create_subscription(
            String,
            'object_detection_topic',
            self.listener_callback3,
            10)

        self.subscription
        self.subscription2
        self.subscription3

    def listener_callback(self, msg):
        self.get_logger().info('GPS Data received: "%s"' % msg.data)

    def listener_callback2(self, msg):
        self.get_logger().info('IMU Data received: "%s"' % msg.data)

    def listener_callback3(self, msg):
        self.get_logger().info('CV Data received: "%s"' % msg.data)




def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
