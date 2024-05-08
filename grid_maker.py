from node_class import *

def make_grid(graph_limits): # Initializes a standard grid with the provided graph_limits = [x_lower, x_upper, y_lower, y_upper]
    grid = {}
    x_lower = graph_limits[0]
    x_upper = graph_limits[1]
    y_lower = graph_limits[2]
    y_upper = graph_limits[3]

    # 1) Name and construct nodes 
    for i in range(x_lower, x_upper + 1):
        for j in range(y_lower, y_upper + 1):
            grid.update({(i, j): Nodes((i, j))}) # For a grid we will use an (x, y) tuple for the name

    # I'm doing this in 2 different loops because we can't link nodes to nodes that don't exist yet
    # I set the neighbors for each node by adding the node to the right and above it. If we iterate through all of the nodes, this will set all the connections.
    # 2) Set the neighbors for all the nodes 
    for i in range(x_lower, x_upper + 1):
        for j in range(y_lower, y_upper + 1):

            if j == y_upper and i == x_upper: 
                break 
            elif j == y_upper: 
                # If the node is along the top of the grid, we only add the node to the right
                grid[(i, j)].add_neighbor(grid[(i + 1, j)], 1)
            elif i == x_upper:
                # If the node is along the right side of the grid, we only add the node above it
                grid[(i, j)].add_neighbor(grid[(i, j + 1)], 1)
            else: 
                grid[(i, j)].add_neighbors([grid[(i + 1, j)], grid[(i, j + 1)]], [1, 1])

    return grid


