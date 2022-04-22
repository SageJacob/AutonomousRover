#!/usr/bin/env python3

import cv2
import depthai as dai
import time
import math
from scipy.spatial.transform import Rotation as R
START = None
FLAG = 0
curr = None
prev = None
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

# Pipeline is defined, now we can connect to the device
with dai.Device(setup()) as device:

    # Output queue for imu bulk packets
    imuQueue = device.getOutputQueue(name="imu", maxSize=50, blocking=False)
    while True:
        imuData = imuQueue.get()  # blocking call, will wait until a new data has arrived
        imuPackets = imuData.packets
        
        for imuPacket in imuPackets:
            acceleroValues = imuPacket.acceleroMeter
            gyroValues = imuPacket.gyroscope
            rVvalues = imuPacket.rotationVector        
            r = R.from_quat([rVvalues.real, rVvalues.i, rVvalues.j, rVvalues.k]) 

            imuF = "{:.06f}"
            #print(f"Quaternion: i: {imuF.format(rVvalues.i)} j: {imuF.format(rVvalues.j)} k: {imuF.format(rVvalues.k)} real: {imuF.format(rVvalues.real)}")
            rotation = r.as_euler('zyz', degrees=True)
            if FLAG == 0:
                START = rotation[2] + 180
                FLAG = 1
                continue
            raw = rotation[2] + 180
            if raw > START:
                out = raw - START
            elif raw < START:
                out = raw + (360 - START)
            else:
                out = 0
            print(START, raw, ((out + 180) % 360) - 180)


            '''
            print(f"Accelerometer [m/s^2]: x: {imuF.format(acceleroValues.x)} y: {imuF.format(acceleroValues.y)} z: {imuF.format(acceleroValues.z)}")
            print(f"Gyroscope [rad/s]: x: {imuF.format(gyroValues.x)} y: {imuF.format(gyroValues.y)} z: {imuF.format(gyroValues.z)} ")
            '''
        if cv2.waitKey(1) == ord('q'):
            break
