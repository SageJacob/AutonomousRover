from pathlib import Path
import blobconverter
import cv2
import depthai as dai
import numpy as np

# 300x300 is default 
window_size = 300
detection_confidence_threshold = 0.05

def createPipeline():
    return dai.Pipeline()

def createCamera(pipeline):
    camera = pipeline.createColorCamera()
    camera.setPreviewSize(window_size, window_size)
    camera.setInterleaved(False)
    return camera

def createDetectionNN(pipeline):
    global detection_confidence_threshold
    detection_network = pipeline.createMobileNetDetectionNetwork()
    detection_network.setBlobPath(str(blobconverter.from_zoo(name='mobilenet-ssd', shaves=6)))
    detection_network.setConfidenceThreshold(detection_confidence_threshold)
    return detection_network

def createXLinkOut(pipeline, name):
    link = pipeline.createXLinkOut()
    link.setStreamName(name)
    return link

def establishPipeline():
    # Create pipeline
    pipeline = createPipeline()
    # Create instance of camera
    camera = createCamera(pipeline)
    # Create instance of detection NN
    detection_network = createDetectionNN(pipeline)
    # Link camera output to detection NN input
    camera.preview.link(detection_network.input)
    # Create instance of XLinkOut for camera
    camera_xlink = createXLinkOut(pipeline, 'camera')
    # Link XLinkOut and Camera to send frames to host
    camera.preview.link(camera_xlink.input)
    # Create instance of XLinkOut for detection NN
    detection_network_xlink = createXLinkOut(pipeline, 'nn')
    # Link XLinkOut and detection NN to send data to host
    detection_network.out.link(detection_network_xlink.input)

    return pipeline, camera, detection_network

def normalizeFrame(frame, bounding_box):
    normalized_values = np.full(len(bounding_box), frame.shape[0])
    normalized_values[::2] = frame.shape[1]
    return (np.clip(np.array(bounding_box), 0, 1) * normalized_values).astype(int)

def main():
    pipeline, camera, detection_network = establishPipeline()
    # Context manager terminates device if process is ever ended during the mission
    with dai.Device(pipeline) as device:
        camera_output = device.getOutputQueue('camera')
        detection_network_output = device.getOutputQueue('nn')
        # frame not none if camera frames are being captured
        # detections is a list provided by detection_network
        frame, detections = None, []  
        while True:
            # Capute camera and detection network incoming data
            camera_in = camera_output.tryGet()
            detection_network_in = detection_network_output.tryGet()

            if camera_in:
                frame = camera_in.getCvFrame()

            if detection_network_in:
                detections = detection_network_in.detections

            if frame is not None:
                for detection in detections:
                    bounding_box = normalizeFrame(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                    cv2.rectangle(frame, (bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3]), (255, 0, 0), 2)
                cv2.imshow('preview', frame)     

            if cv2.waitKey(1) == ord('q'):
                break 


    


if __name__ == "__main__":
    main()