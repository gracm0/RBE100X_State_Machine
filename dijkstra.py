# This file contains our Dijkstra Class
# We pass the constructor a graph and the name of the source node
# We can then either call dijkstra_alg() or shortest_path() to do the computation

from node_class import *

class Dijkstra():

    # Variables: 
        # graph = {name: Nodes(name)}
        # source_node_name
        # to_visit = {}
        # distance_table = {name: dist}
        # paths = {name: [path]}

    # Methods: 
        # update_tables()
        # update_list()
        # remove_node(node_name)
        # remove_nodes([node_name])
        # remove_edge(node_name_1, node_name_2)
        # dijkstra_alg()
        # shortest_path(node_name)
        # print_table()

    def __init__(self, graph, source_node_name = (0, 0)):

        self.graph = graph
        self.source_node_name = source_node_name

        self.to_visit = set(graph.keys()) - {source_node_name} # Set of node names that we need to visit

        # Building the distance and path dictionaries
        self.distance_table = {source_node_name : 0} # {node_name : distance}
        self.paths = {source_node_name : [source_node_name]} # {node_name : [path]}

        for node_name in self.to_visit: # This iterates over the keys
            self.distance_table.update({node_name : float('inf')})
            self.paths.update({node_name : [source_node_name]})



    def update_tables(self):
        # Check all nodes that are on the current shortest path
        visited = set(self.graph.keys()) - self.to_visit
        for node_name in visited:
            neighbor_list = self.graph[node_name].neighbors

            # If a node visited we check the distance to all of it's neighbors 
            for neighbor_name in neighbor_list:

                # We're doing length = distance to current node + distance to next node
                # We'll get the distance to the current node from our distance table
                # We can get the distance to the next node from our list of neighbors 

                path_length = self.distance_table[node_name] + neighbor_list[neighbor_name]

                if path_length < self.distance_table[neighbor_name]:
                    self.distance_table[neighbor_name] = path_length

                    # Our path is a list of names. Be carefull, lists are MUTABLE objects!
                    # new path = path to the current node + name of the next node
                    # Without a copy, setting two elements equal will set their pointers to be equal
                    # That means they would be literally the same object
                    self.paths[neighbor_name] = self.paths[node_name].copy()
                    self.paths[neighbor_name].append(neighbor_name)

    def update_list(self):

        visited_node_name = ''
        shortest_distance = float('inf')
    
        # We iterate through all the unvisited nodes to find the minimum distance
        for node_name in self.to_visit:

            node_dist = self.distance_table[node_name]

            if node_dist < shortest_distance:

                # Candidate node
                visited_node_name = node_name 
                shortest_distance = node_dist 

        # Once we find the closest node, we remove it from our to_visit set
        self.to_visit.remove(visited_node_name)
    

    # When we remove a node from our graph, we need to cut it's connections with the other nodes
    def remove_node(self, node_name):

        # We cannot remove the source node
        if node_name == self.source_node_name:
            print("Warning: Cannot remove the source node!")
            return 
        
        # We also cannot remove a node that does not exist
        if node_name in self.graph:

            node = self.graph[node_name]

            for neighbor_name in node.neighbors.copy():
                node.remove_neighbor(self.graph[neighbor_name])

            self.to_visit.remove(node_name)
            self.graph.pop(node_name)

    def remove_nodes(self, node_name_list):
        for node_name in node_name_list:
            self.remove_node(node_name)

    # If we want to remove the connections but leave the node
    def remove_edge(self, node_name_1, node_name_2):
        node_1 = self.graph[node_name_1]
        node_2 = self.graph[node_name_2]
        node_1.remove_neighbor(node_2)

    def remove_edges(self, node_name_list_1, node_name_list_2): # List one contains a nodes names. List 2 are the coressponding node neighbors
        for i in range(0, len(node_name_list_1)):
        
            self.remove_edge(node_name_list_1[i], node_name_list_2[i])


    # We have separated our algorithm into two functions: one that updates our tables and one that updates our to_visit set
    def dijkstra_alg(self):

        # Given "N" nodes, the number of total iterations will be N-1
        N = len(self.graph.keys())
        for i in range(0, N-1):
            self.update_tables()
            self.update_list()


    def shortest_path(self, goal_node_name):

        # If we want the shortest path to a specific node, we can stop execution when we visit it
        while goal_node_name in self.to_visit:
            self.update_tables()
            self.update_list()

        return self.paths[goal_node_name]


    # This is just a utility to make the output more readable
    def print_table(self):

        print("\nDistance Table")
        print('-----------------------------')
        print("Name | Distance | Path")

        for name in self.graph:
            output = str(name) + "    |     " + str(self.distance_table[name]) + "    |    " + str(self.paths[name])
            print(output)


"""
# Numeric example ------------------------------------------------------------------
# To make a graph, we first generate a dictionary of node objects
graph = {'0' : Nodes('0'),
    '1' : Nodes('1'),
    '2' : Nodes('2'),
    '3' : Nodes('3'),
    '4' : Nodes('4'),
    '5' : Nodes('5'),
    '6' : Nodes('6')}


# We then add all of the edges/connections between the nodes
graph['0'].add_neighbors([graph['1'], graph['2']], [2, 6])
graph['3'].add_neighbors([graph['1'], graph['2'], graph['4'], graph['5']], [5, 8, 10, 15])
graph['5'].add_neighbors([graph['4'], graph['6']], [6, 6])
graph['4'].add_neighbor(graph['6'], 2)


# Here we create our dijkstra object 
dijkstra_object = Dijkstra(graph, '0')
# dijkstra_object.remove_nodes(['1', '4'])
dijkstra_object.remove_edges(['3', '3'], ['4', '1'])
# We need to make sure all changes to the graph are done before we call the algorithm
# dijkstra_object.dijkstra_alg()
# dijkstra_object.print_table()

print(dijkstra_object.shortest_path('3'))
"""
