#!/usr/bin/env python3

# Libraries for OAK-D camera
import cv2
import depthai as dai
import time
import math

# Libraries for ROS2
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# function for IMU data conversion (from depthai docs)
def timeDeltaToMilliS(delta) -> float:
    return delta.total_seconds()*1000

# setup to recieve IMU data (from depthai docs)
def setup():
    pipeline = dai.Pipeline()
    imu = pipeline.create(dai.node.IMU)
    xlinkOut = pipeline.create(dai.node.XLinkOut)
    xlinkOut.setStreamName("imu")

    # enable ACCELEROMETER_RAW at 500 hz rate
    imu.enableIMUSensor(dai.IMUSensor.ACCELEROMETER_RAW, 500)
    # enable GYROSCOPE_RAW at 400 hz rate
    imu.enableIMUSensor(dai.IMUSensor.GYROSCOPE_RAW, 400)
    # enable MAGNETOMETER_RAW at 400 hz rate
    imu.enableIMUSensor(dai.IMUSensor.MAGNETOMETER_RAW, 400)
    # enable ROTATION_VECTOR at 400 hz rate
    imu.enableIMUSensor(dai.IMUSensor.ROTATION_VECTOR, 400)


    # it's recommended to set both setBatchReportThreshold and setMaxBatchReports to 20 when integrating in a pipeline with a lot of input/output connections
    # above this threshold packets will be sent in batch of X, if the host is not blocked and USB bandwidth is available
    imu.setBatchReportThreshold(1)
    # maximum number of IMU packets in a batch, if it's reached device will block sending until host can receive it
    # if lower or equal to batchReportThreshold then the sending is always blocking on device
    # useful to reduce device's CPU load  and number of lost packets, if CPU load is high on device side due to multiple nodes
    imu.setMaxBatchReports(10)

    # Link plugins IMU -> XLINK
    imu.out.link(xlinkOut.input)
    return pipeline


# publisher class of this node
class MinimalPublisher(Node):

    # Initialize the parameters of the class
    def __init__(self):
        super().__init__('minimal_publisher')
        self.acceleration_publisher_ = self.create_publisher(String, 'test', 10) # publish to scan topic
        self.gyroscope_publisher_ = self.create_publisher(String, 'test', 10) # publish to scan topic
        self.rotation_publisher_ = self.create_publisher(String, 'test', 10) # publish to scan topic
        self.quarternion_publisher_ = self.create_publisher(String, 'test', 10) # publish to scan topic
        self.accuracy_publisher_ = self.create_publisher(String, 'test', 10) # publish to scan topic
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):

        # loop through IMU data packets
        with dai.Device(setup()) as device:

            # Output queue for imu bulk packets
            imuQueue = device.getOutputQueue(name="imu", maxSize=50, blocking=False)
            
            # Output queue for imu bulk packets
            baseTs = None
            
            #while True:
            imuData = imuQueue.get()  # blocking call, will wait until a new data has arrived
            imuPackets = imuData.packets
            
            for imuPacket in imuPackets:
                acceleroValues = imuPacket.acceleroMeter
                gyroValues = imuPacket.gyroscope
                rotateValues = imuPacket.rotationVector          

                imuF = "{:.06f}"

                # print(f"Accelerometer [m/s^2]: x: {imuF.format(acceleroValues.x)} y: {imuF.format(acceleroValues.y)} z: {imuF.format(acceleroValues.z)}")
                # print(f"Gyroscope [rad/s]: x: {imuF.format(gyroValues.x)} y: {imuF.format(gyroValues.y)} z: {imuF.format(gyroValues.z)} ")

                msg = String()
                msg.data = f"Accelerometer [m/s^2]: x: {imuF.format(acceleroValues.x)} y: {imuF.format(acceleroValues.y)} z: {imuF.format(acceleroValues.z)}"
                self.acceleration_publisher_.publish(msg)
                self.get_logger().info("%s" % msg.data)
                self.i += 1

                msg_2 = String()
                msg_2.data = f"Gyroscope [rad/s]: x: {imuF.format(gyroValues.x)} y: {imuF.format(gyroValues.y)} z: {imuF.format(gyroValues.z)}"
                self.gyroscope_publisher_.publish(msg_2)
                self.get_logger().info("%s" % msg_2.data)
                self.i += 1

                rVvalues = imuPacket.rotationVector

                rvTs = rVvalues.timestamp.get()
                if baseTs is None:
                    baseTs = rvTs
                rvTs = rvTs - baseTs

                imuF = "{:.06f}"
                tsF  = "{:.03f}"

                # print(f"Rotation vector timestamp: {tsF.format(timeDeltaToMilliS(rvTs))} ms")
                # print(f"Quaternion: i: {imuF.format(rVvalues.i)} j: {imuF.format(rVvalues.j)}" f"k: {imuF.format(rVvalues.k)} real: {imuF.format(rVvalues.real)}")
                # print(f"Accuracy (rad): {imuF.format(rVvalues.rotationVectorAccuracy)}")

                msg_3 = String()
                msg_3.data = f"Rotation vector timestamp: {tsF.format(timeDeltaToMilliS(rvTs))} ms"
                self.rotation_publisher_.publish(msg_3)
                self.get_logger().info("%s" % msg_3.data)
                self.i += 1

                msg_4 = String()
                msg_4.data = f"Quaternion: i: {imuF.format(rVvalues.i)} j: {imuF.format(rVvalues.j)}" f"k: {imuF.format(rVvalues.k)} real: {imuF.format(rVvalues.real)}"
                self.quarternion_publisher_.publish(msg_4)
                self.get_logger().info("%s" % msg_4.data)
                self.i += 1

                msg_5 = String()
                msg_5.data = f"Accuracy (rad): {imuF.format(rVvalues.rotationVectorAccuracy)}"
                self.accuracy_publisher_.publish(msg_5)
                self.get_logger().info("%s" % msg_5.data)
                self.i += 1

        # msg = String()
        # msg.data = 'Hello World: %d' % self.i
        # self.publisher_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        # self.i += 1


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
