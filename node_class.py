# This class is used for nodes connected on a general graph 
class Nodes():

    def __init__(self, name):
        self.name = name
        self.neighbors = {} # dict where {neighbor_name : distance}

    # You have to use a string to "type hint" a class used inside of itself 
    def add_neighbor(self, neighbor_node: 'Nodes', dist):
        self.neighbors.update({neighbor_node.name : dist})
        neighbor_node.neighbors.update({self.name : dist})

    # Inputs are list of neighbor_nodes and list of distances
    def add_neighbors(self, neighbor_nodes, distance_list):
        for i in range(0, len(neighbor_nodes)):
            self.add_neighbor(neighbor_nodes[i], distance_list[i])

    def remove_neighbor(self, neighbor_node: 'Nodes'):
        self.neighbors.pop(neighbor_node.name)
        neighbor_node.neighbors.pop(self.name)

    def remove_neighbors(self, neighbor_nodes):
        for node in neighbor_nodes:
            self.remove_neighbor(node)

# A = Nodes('A')
# B = Nodes('B')
# C = Nodes('C')

# A.add_neighbors([B, C], [2, 4])
# A.remove_neighbors([B, C])

# # To make a graph, we first generate a dictionary of node objects
# graph = {'A' : Nodes('A'),
#         'B' : Nodes('B'),
#         'Frog' : Nodes('Frog'),
#         'Cat' : Nodes('Cat')}

# # We then add all of the edges/connections between the nodes
# graph['A'].add_neighbors([graph['B'], graph['Frog']], [1, 5])
# graph['B'].add_neighbor(graph['Frog'], 1)
# graph['Frog'].add_neighbor(graph['Cat'], 2)

# print("A: ", graph['A'].neighbors)
# print("B: ", graph['B'].neighbors)
# print("Frog: ", graph['Frog'].neighbors)
# print("Cat: ", graph['Cat'].neighbors)