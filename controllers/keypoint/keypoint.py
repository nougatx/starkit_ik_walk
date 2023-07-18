"""ik_walk2 controller."""

#to help us read the json code
import math
import json
from controller import Robot

def deg2rad(deg):
    return deg/180*math.pi

def rad2deg(rad):
    return rad/math.pi*180
    
#a fn that reads our file
def read_json(file_path):
    #we open the file and and name the 
    #that contains the contents of the
    #file as 'file'
    with open(file_path, 'r') as file:
        #do smth w the file
        data = json.load(file) 
    return data

#interpolation function
#introdusing 100 points between our keypoints
#earlier there was only 32ms which wasnt enough for the robot to do the motion
def interpolate_points(start, end):
    interpolated_points = []
    for i in range(steps):
        #eqn to caculate the exact point
        point = start + (end - start) / steps * i
        interpolated_points.append(point)
    print(interpolated_points)
    return interpolated_points
    
    
    

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

motion = read_json("move.json")

left_elbow = robot.getDevice("left_elbow")
left_elbow_sensor = robot.getDevice("left_elbow_sensor")
left_elbow_sensor.enable(timestep)

##3to assign degree manually:
#left_elbow.setPosition(deg2rad(-45))

##2for each point inside left_elbow in move.json file
# for point in motion("left_elbow"):
    # left_elbow.setPosition(deg2rad(point[1]))
    
    
#1 motion = read_json("move.json")
#1 print(motion)

current_point = 0
current_sub_point = 0
steps = 10
target = 0
# Main loop:
# - perform simulation steps until Webots is stopping the controller
robot.step(timestep)
interpolated_points = interpolate_points(left_elbow_sensor.getValue(), deg2rad(motion["left_elbow"][0][1]))

while robot.step(timestep) != -1:
    if current_point < motion["over"][1][0]:
        if current_sub_point < steps-1:
            #print(current_sub_point)
            # target = interpolated_points[current_sub_point]
            # current_sub_point +=1  
            current_sub_point = 0
            current_point +=1
            interpolated_points = interpolated_points(deg2rad(motion["left_elbow"][current_point-1][1]), 
                                    deg2rad(motion["left_elbow"][current_point][1]))

    target = interpolated_points[current_sub_point]
    current_sub_point +=1 
    if current_sub_point >steps-1:
        current_sub_point = steps-1
         
    left_elbow.setPosition(target)
    #left_elbow.setPosition(deg2rad(motion["left_elbow"][current_point][1]))
    #print(current_point, deg2rad(motion["left_elbow"][current_point][1]),rad2deg(left_elbow_sensor.getValue()))

    pass

# Enter here exit cleanup code.
