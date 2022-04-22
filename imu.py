#!/usr/bin/env python3
import depthai as dai
from scipy.spatial.transform import Rotation as R

def setup():
    pipeline = dai.Pipeline()
    imu = pipeline.create(dai.node.IMU)
    xlinkOut = pipeline.create(dai.node.XLinkOut)
    xlinkOut.setStreamName("imu")
    imu.enableIMUSensor(dai.IMUSensor.ROTATION_VECTOR, 400)
    imu.setBatchReportThreshold(1)
    imu.setMaxBatchReports(10)
    imu.out.link(xlinkOut.input)
    return pipeline

START = None
FLAG = 0
curr = None
prev = None

with dai.Device(setup()) as device:

    imuQueue = device.getOutputQueue(name="imu", maxSize=50, blocking=False)
    while True:
        imuData = imuQueue.get()
        imuPackets = imuData.packets
        
        for imuPacket in imuPackets:
            rVvalues = imuPacket.rotationVector        
            r = R.from_quat([rVvalues.real, rVvalues.i, rVvalues.j, rVvalues.k]) 
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
            out = int(((out + 180) % 360) - 180)
            print(out)
