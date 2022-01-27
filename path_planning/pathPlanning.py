# Importing the required module
from random import seed
from random import random
import matplotlib.pyplot as plt

# Constants
seed(30)

step = .00001
sim_history = []
max_moves = 20000

simulations = []
num_simulations = 50
min_lat, max_lat = 35.348, 35.361
min_lon, max_lon = -117.835, -117.78

road_exit = (35.348122, -117.807827)
launch_site = (35.347113, -117.808956)
road_entrance = (35.350753, -117.807827)

red = (35.351471, 35.353303, -117.830429, -117.825695,"red")
blue = (35.348190, 35.350753, -117.808041, -117.80500,"blue")
green = (35.353303, 35.360876, -117.830429, -117.825695,"green")
yellow = (35.349466, 35.350753, -117.80500, -117.785487,"yellow")
orange = (35.351471, 35.353303, -117.825695, -117.819414,"orange")
purple = (35.349986, 35.353303, -117.819414, -117.816652,"purple")
rectangular_zone_list = [green, red, orange, purple, yellow, blue]

def inZone(coords):
    red = (35.351471, 35.353303, -117.830429, -117.825695,"red")
    blue = (35.348190, 35.350753, -117.808041, -117.80500,"blue")
    green = (35.353303, 35.360876, -117.830429, -117.825695,"green")
    yellow = (35.349466, 35.350753, -117.80500, -117.785487,"yellow")
    orange = (35.351471, 35.353303, -117.825695, -117.819414,"orange")
    purple = (35.349986, 35.353303, -117.819414, -117.816652,"purple")
    rectangular_zone_list = [green, red, orange, purple, yellow, blue]
    for zone in rectangular_zone_list:
        if coords[0] > zone[0] and coords [0] < zone [1] and coords[1] > zone [2] and coords[1] < zone [3]:
            return zone[4]
    if coords[0] > road_entrance[0]:
        return "pink"
    return "none"

def getTarget(coords, zone):
  ignore_zones = False
  offset = .00025
  if zone == "none" or ignore_zones == True:
    return launch_site
  elif zone == "green" or zone == "purple":
    # Go East
    return (coords[0], coords[1] + offset)
  elif zone == "orange" or zone == "yellow":
    # Go North
    return (coords[0] + offset, coords[1])
  elif zone == "red":
    # Go Northeast
    return (coords[0] + offset, coords[1] + offset)
  elif zone == "pink":
    # Go to Entry Point
    return road_entrance
  elif zone == "blue":
    # Go to End of Road
    return road_exit

def overrideAreas(latitude, longitude):
    coords = (latitude, longitude)
    zone = inZone(coords)
    target = getTarget(coords, zone)
    return target

def arrived(coords):
    dest_accuracy = .0001
    if abs(coords[0]-launch_site[0]) < dest_accuracy and abs(coords[1]-launch_site[1]) < dest_accuracy:
        return True
    else:
        return False

def runSimulation():
    for sim in range(num_simulations):
        scaled_lat = min_lat + (random() * (max_lat-min_lat))
        scaled_lon = min_lon + (random() * (max_lon-min_lon))
        simulations.append([ scaled_lat, scaled_lon ])

    for sim_number, simulation in enumerate(simulations):
        history = []
        sim_history.append(history)
        pos = simulation
        moves = 0
        while not(arrived(pos)):
            target = overrideAreas(pos[0], pos[1])
            lat_away = abs(pos[0]-target[0])
            lon_away = abs(pos[1]-target[1])
            lat_ratio = (lat_away + .00000001) / (lat_away + lon_away + .00000001)
            lon_ratio = 1-lat_ratio
            if pos[0] - target[0] < 0:
                pos[0] += step * lat_ratio
            elif pos[0] - target[0] > 0:
                pos[0] -= step * lat_ratio
            if pos[1] - target[1] < 0:
                pos[1] += step * lon_ratio
            elif pos[1] - target[1] > 0:
                pos[1] -= step * lon_ratio

            history.append([pos[0],pos[1]])
            moves += 1
            if moves > max_moves:
                print("Froze")
                break

    print(str(len(simulations)) + " simulations arrived at Launch Site")

    for simulation in sim_history:
        lat_history = []
        lon_history = []
        for record in simulation:
            lat_history.append(record[0])
            lon_history.append(record[1])
        # plotting the points
        plt.plot(lon_history, lat_history)
        plt.plot(lon_history[0], lat_history[0], marker = 'x')


    # plotting the zones
    plt.plot(-117.808956,35.347113,  marker = 'o')
    for color in rectangular_zone_list:
        x = [color[2],color[2],color[3],color[3],color[2]]
        y = [color[0],color[1],color[1],color[0],color[0]]
        plt.plot(x,y)
    
    # naming the x axis
    plt.xlabel('Longitude')
    # naming the y axis
    plt.ylabel('Latitude')
    # giving a title to my graph
    plt.title('Adiona Recovery Path Simulation')
    # Adjusting the margins to fit the data
    plt.margins(.05)
    plt.rcParams['figure.figsize'] = [10, 6]
    # function to show the plot
    plt.show()

runSimulation()