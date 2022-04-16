#!/usr/bin/env python3

# Libraries for ROS2
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# Library for GPS
import serial

# publisher class of this node
class MinimalPublisher(Node):

    # Initialize the parameters of the class
    def __init__(self):
        super().__init__('minimal_publisher')
        self.latitude_publisher_ = self.create_publisher(String, 'gps', 10) # publish to scan topic
        self.longitude_publisher_ = self.create_publisher(String, 'gps', 10) # publish to scan topic

        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
    
	gps = serial.Serial("/de/ttyACM0", baurate = 9600)

	line = gps.readline()
    	line_byte = line.decode("utf-8")
    	data = line_byte.split(",")

	    if data[0] == "$GPRMC":

		# Get Latitude
		latitude_name = data[3]
		latitude_degree = latitude_name[:2]

		if data[4] == 'S':
		    lat_degree = float(latitude_degree) * -1
		else:
		    lat_degree = float(latitude_degree)

		lat_degree = str(lat_degree).strip(.0)
		latitude_ddd = latitude_name[2:10]
		latitude_mmm = float(latitude_ddd) / 60
		latitude_mmm = str(latitude_mmm).strip('0.')[:8]
		latitude = lat_degree + "." + latitude_mmm

		# Get Longitude
		longitude_name = data[5]
		longitude_degree = longitude_name[1:3]

		if data[6] == 'W':
		    long_degree = float(longitude_degree) * -1
		else:
		    long_degree = float(longitude_degree)

		long_degree = str(long_degree).strip(.0)
		longitude_ddd = longitude_name[3:10]
		longitude_mmm = float(longitude_ddd) / 60
		longitude_mmm = str(longitude_mmm).strip('0.')[:8]
		longitude = long_degree + "." + longitude_mmm

		# print("Longitude: " + longitude)
		# print("Latitude: " + latitude)

                msg = String()
                msg.data = "lat: " + latitude
                self.latitude_publisher_.publish(msg)
                self.get_logger().info("%s" % msg.data)
                self.i += 1

                msg_2 = String()
                msg_2.data = "long: " + longitude
                self.longitude_publisher_.publish(msg_2)
                self.get_logger().info("%s" % msg_2.data)
                self.i += 1

# main function that spins the node constantly
def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
