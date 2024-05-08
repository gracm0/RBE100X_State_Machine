# Grace Mahoney
# Due December 15, 2023
# Autonomously maneuver a WPI XRP robot around a tape grid. The path is generated using the Dijkstra's algorithm with given inputs of the coordinates of the starting node
# and the goal node. 

from XRPLib.defaults import *
import time
from node_class import *
from grid_maker import *
from dijkstra import *

# State machine for the movement of the robot. 
class State():
    TURNING = 0
    FORWARD = 1
    END = 2

class Maneuver():
    # Generates a path Dijkstra's algorithm with inputted coordinates of the goal and source node. Then runs the robot through the path by orienting the robot to the next
    # node in the path and line tracking forward one node until the goal node is reached.
    # Inputs: grid_limits {List} - lower and upper limits for x and y as integers in the order: [x_min, x_max, y_min, y_max]
    #         obstructions {List} - list of tuples of the coordinates of obstructed nodes to be removed: [(x_0,y_0), (x_1,y_2), ...]
    #         goal_node {Tuple} - coordinate of the node where the robot should end up
    #         source-node {Tuple} - coordinate of the node where the robot's starting position is
    #         robo {Robot} - a Robot object that stores the robot's current position and orientation
    def __init__(self, graph_limits, obstructions, goal_node, source_node, robo): 
        self.current_state = State.TURNING

        self.goal_node = goal_node
        self.source_node = source_node
        
        self.graph = make_grid(graph_limits)
        self.dijkstra_obj = Dijkstra(self.graph, self.source_node)
        self.dijkstra_obj.remove_nodes(obstructions)
        
        self.robo = robo
        self.path_list = []
        self.index = 0 # index for path_list
        
        self.task()
        
    def task(self):
        # Creates path using dijkstra's algorithm
        self.path_list = self.dijkstra_obj.shortest_path(self.goal_node)
        print("Dijkstra Path:\n", self.path_list)
        
        if(self.robo.get_position() == self.path_list[0]): self.path_list.pop(0) # Deletes the node the robot is starting at
        
        while not(self.current_state is State.END):
            print("\nFacing: ", self.robo.get_orientation(), "\nAt Node: ", self.robo.get_position())
        
            next_node = self.path_list[self.index]
            #print("     Index:", self.index, "=>", next_node)
            
            self.current_state = self.on_event(next_node)
            
        self.on_event()
        
    def on_event(self, node = None):
        if self.current_state == 0:
            return self.__TURNING_handler(node)
        elif self.current_state == 1:
            return self.__FORWARD_handler(node)
        elif self.current_state == 2:
            self.__END_handler()
                
    def __TURNING_handler(self, next_node):
        if(self.robo.get_position()[0] < next_node[0]): # Orients robot EAST to increase 1 node in the x direction
            face("EAST", self.robo)
        elif(self.robo.get_position()[0] > next_node[0]): # Orients robot WEST to decrease 1 node in the x direction
            face("WEST", self.robo)
        elif(self.robo.get_position()[1] < next_node[1]): # Orients robot NORTH to increase 1 node in the y direction
            face("NORTH", self.robo)
        else: # Orients robot SOUTH to decrease 1 node in the y direction
            face("SOUTH", self.robo)
        
        return State.FORWARD
    
    def __FORWARD_handler(self, next_node):
        line_track()
        self.robo.set_position(next_node)
        time.sleep(1)
        
        if not(self.robo.get_position() == self.goal_node):
            self.index += 1
            return State.TURNING
        else:
            return State.END
        
    def __END_handler(self):
        print("Arrived at goal node:", self.goal_node)




# Stores the current orientation and position of the robot on the grid
# Input: position {Tuple} - current position of the robot in (x,y) format, default value is (0,0)
#        orientation {str} - the direction the robot is currently facing: "NORTH", "EAST", "SOUTH", "WEST", default value is "NORTH"
class Robot():
    def __init__(self, position = (0,0), orientation = "NORTH"):
        self.orientation = orientation
        self.position = position
        
        
    # SETTER FUNCTIONS
    # Input: new_orientation {str} - must be "NORTH", "EAST", "SOUTH", or "WEST"
    def set_orientation(self, new_orientation):
        self.orientation = new_orientation
        #print("Facing: ", self.orientation)
        
    # Input: coord {Tuple} - coordinate of the robot's current position in the limits of the grid
    def set_position(self, coord):
        self.position = coord
        #print("At node: ", self.get_position())
        

    # GETTER FUNCTIONS
    def get_orientation(self):
        return self.orientation
        
    def get_position(self):
        return self.position




# Moves robot forward along line and stops at the next node
def line_track():
    
    base_effort = 0.7
    KP = 0.9
        
    avgR = (reflectance.get_left() + reflectance.get_right())/2
    #print(avgR)
    while (avgR < 0.9): # Table reflectance is about 0.83
        #print("L:", reflectance.get_left(), "R:", reflectance.get_right())
        avgR = (reflectance.get_left() + reflectance.get_right())/2
        
        error = reflectance.get_left() - reflectance.get_right()
        drivetrain.set_effort(base_effort - error * KP, base_effort + error * KP)
        
    # Centers robot at node
    error = reflectance.get_left() - reflectance.get_right()
    drivetrain.set_effort(0.5 - error * KP, 0.5 + error * KP)
    time.sleep(0.4)

    drivetrain.set_effort(0,0)
    time.sleep(0.1)

    print("     Moves forward 1 node...")


# Turns robot right or left, or turns the robot 180 degrees by turning left twice.
# Input: direction {int} - '1' turns right, '-1' turns left, 0 turns 180 degrees
#        robo {Robot} - robot that will be turning
def turn(direction):
    # Turn right
    if(direction > 0):
        drivetrain.set_effort(0.8, -0.8)
        time.sleep(0.5)
        
        while(reflectance.get_right() < 0.9):
            drivetrain.set_effort(0.8,-0.8)
        
        # Centers robot on line
        drivetrain.set_effort(0.4,-0.4)
        time.sleep(0.1)
        
        drivetrain.set_effort(0.0,0.0)

        print("     Turns Right...")
    # Turn left
    elif(direction < 0):
        drivetrain.set_effort(-0.8,0.8)
        time.sleep(0.5)
        
        while(reflectance.get_left() < 0.9):
            drivetrain.set_effort(-0.8,0.8)
         
        # Centers robot on line
        drivetrain.set_effort(-0.4,0.4)
        time.sleep(0.1)
            
        drivetrain.set_effort(0.0,0.0)

        print("     Turns Left...")
    # Turn 180 degrees
    else:
        turn(-1)
        turn(-1)

    time.sleep(.5)
    

# Orients the robot to face the inputted cardinal direction.
# Input: direction {str} - goal direction: "NORTH", "EAST", "SOUTH", or "WEST"
#        robo {Robot} - robot that will be turning
def face(direction, robo):
    COMPASS = ["NORTH", "EAST", "SOUTH", "WEST"]
    facing = robo.get_orientation()
    for x in range(0,4):
        if(facing == COMPASS[x]): f_index = x
        if(direction == COMPASS[x]): d_index = x

    # Turn 180 degrees if the goal direction is opposite the current orientation
    if(COMPASS[f_index] == COMPASS[d_index - 2] or COMPASS[f_index - 2] == COMPASS[d_index]):
        turn(0)
        robo.set_orientation(COMPASS[f_index - 2])
    # Turn left if the goal direction is one direction to the left of the current orientation
    elif(COMPASS[f_index] == COMPASS[d_index - 3]):
        turn(-1)
        robo.set_orientation(COMPASS[f_index - 1])
    # Turn right if the goal direction is one direction to the right of the current orientation
    elif(COMPASS[f_index] == COMPASS[d_index - 1]):
        turn(1)
        robo.set_orientation(COMPASS[f_index - 3])
    

# ----- Input Variables (Edit) --------------------------------------------------------------------------------
# Edit the values below

grid_lim = [-3,6,0,5] # [x_min, x_max, y_min, y_max]
obstructions = [(-1, 1), (0, 1), (1, 2), (2, 2), (3, 0), (4, 4), (4, 2), (1, 1)]

source_node = (-3,0) # (x,y) - current position of robot
orientation = "EAST" # robot's current orientation: "NORTH", "EAST", "SOUTH", "WEST"

goal_node_0 = (4,1) # (x,y) - end position of robot
goal_node_1 = (0,2)
goal_node_2 = (5,4)
# If goal nodes are added or removed, do the same to the corresponding routes:
# goal_node_n = (x,y)


# ----- Do not edit -------------------------------------------------------------------------------------------
# 'gary' holds the position and orientation of the robot
gary = Robot(source_node, orientation)


# ----- Routes (Edit) -----------------------------------------------------------------------------------------
# Add or remove routes depending on the desired number of goal nodes

route_0 = Maneuver(grid_lim, obstructions, goal_node_0, gary.get_position(), gary)
route_1 = Maneuver(grid_lim, obstructions, goal_node_1, gary.get_position(), gary)
route_2 = Maneuver(grid_lim, obstructions, goal_node_2, gary.get_position(), gary)
# If goal nodes are added or removed, do the same to the corresponding routes:
# route_n = Maneuver(grid_lim, obstructions, goal_node_n, gary.get_position(), gary)

