import serial

gps= serial.Serial("/de/ttyACM0", baurate = 9600)

while True:
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

        print("Longitude: " + longitude)
        print("Latitude: " + latitude)