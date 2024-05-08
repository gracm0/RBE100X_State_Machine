# RBE100X_State_Machine

Autonomously maneuver a WPI XRP robot around a tape grid. The path is generated using the Dijkstra's algorithm with given inputs of the 
coordinates of the starting node and the goal node. Then runs the robot through the generated path by orienting the robot to face the next 
node in the path and line tracking forward one node until the goal node is reached.

Source Files:
    tape_grid.py
    node_class.py
    grid_maker.py
    dijkstra.py

Compile and run:
    Open the tape_grid.py file and scroll all the way to the bottom. Update the 'Input Variables', which includes the grid's upper and 
    lower bounds, a list of obstructed nodes, the robot's starting coordinate and orientation, and the coordinates of the goal node(s).
    Add or remove goal nodes to desired number and add/remove the corresponding routes. 

    For all goal nodes under 'Input Variables': 
        goal_node_n = (x,y)
    Add to the 'Routes': 
        route_n = Maneuver(grid_lim, obstructions, goal_node_n, gary.get_position(), gary)

    Connect the XRP Robot and run the code.



Grace Mahoney
December 14, 2023
