from rplidar import RPLidar
import rplidar
import random

'''

degrees_to_turn = 13, rover turns to 13, drives straight, once the lidar at 13 degrees is open, straighten out
once straightened out, check if object is in rear, turn -13 degrees, straigthen out


'''


def process(angle_to_distance, ranges):
    distances = []
    for i in range(315, 360):
        distances.append(angle_to_distance[str(i)])
    for i in range(0, 46):
        distances.append(angle_to_distance[str(i)])
    print(distances)

    min_dis = 1219.2
    binaries = [0] * len(distances)

    num_scan = 20

    for j in range(len(distances)):
        if distances[j] < min_dis:
            binaries[j] += 1
    print(binaries)

    open_path = {}

    counter = 0
    one = False
    index = -1
    for i in range(len(binaries)):
        if binaries[i] == 1:
            one = True
        else:
            one = False
            if index == -1:
                index = i
        if one:
            if index > -1:
                open_path[str(index)] = counter
            index = -1
            counter = 0
        else:
            counter += 1
    if index > -1:
        open_path[str(index)] = counter
    print(open_path)
    max_key, max_value = None, None
    for i in open_path:
        if not max_value or open_path[i] > max_value:
            max_key, max_value = i, open_path[i]
            continue
    degrees_to_turn = ranges[int((int(max_key) + (int(max_key) + max_value)) / 2)]
    return degrees_to_turn

def run_lidar():

    lidar = RPLidar('/dev/ttyUSB0')

    info = lidar.get_info()
    lidar.motor_speed = rplidar.MAX_MOTOR_PWM
    print(info)

    health = lidar.get_health()
    print(health)

    min_lidar_delta = 15.0

    ranges = [i for i in range(315, 360)]
    ranges = ranges + [i for i in range(0, 46)]
    angle_to_distance = {str(i): None for i in ranges}
    for i, scan in enumerate(lidar.iter_scans(scan_type='express',min_len=100,max_buf_meas=500)):
        for val in scan:
            if str(int(val[1])) in angle_to_distance:
                angle_to_distance[str(int(val[1]))] = int(val[2])

        flag = False
        for j in angle_to_distance:
            if angle_to_distance[j] == None:
                flag = True
                break
        if not flag:
            print(process(angle_to_distance, ranges))

    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

run_lidar()