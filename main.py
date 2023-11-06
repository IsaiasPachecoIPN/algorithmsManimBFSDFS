from manim import *
from utils import *

root = 0

import sys
sys.setrecursionlimit(1500)

def readInitData( file ):
    """
    Function to load inputdata 
    (param) file : file to read
    """
    
    arr_edges = []
    arr_vertices = []
    global root

    with open(file, 'r') as f:
        data = f.readlines()
        for line in data:
            line = line.strip()
            if "vertices" in line:
                vertices_line = line.split(":")
                [arr_vertices.append(int(x)) for x in vertices_line[1].split(",")]
            elif "edges" in line:
                edges_line = line.strip().split(":")
                aux_edges = edges_line[1].split(",")
                for edge in aux_edges:
                    _edge = edge.split("-")
                    #print(type((int(aux_edge[0]), int(aux_edge[1]))))
                    arr_edges.append((int(_edge[0]), int(_edge[1])))
            elif "root" in line:
                root_line = line.strip().split(":")
                root = int(root_line[1])

    print("vertices:", arr_vertices)
    print("edges:", arr_edges)
    print("root:", root)
    return [arr_vertices, arr_edges]


def createGraph():
    """
    Function to create the graph
    """
    values = readInitData("inputdata")
    g = Graph(values[0], values[1], layout_config={"seed": 0}, labels=SHOW_LABELS)
    return g


def addBFSAnimation( scene, graph, root ):
    """
    Function to add BFS animation
    """
    bfs_tree = BFS(graph, root)
    for edge in bfs_tree:
        edge_key = getEdgeFromGraph(graph, edge)
        if edge_key != None : scene.play(graph.edges[edge_key].animate.set_color(RED)) 

def createScene( scene ):
    """
    Function to create the scene
    """
    g = createGraph()
    scene.play(Write(g))
    BFS( scene, g, root )

class CreateScene(MovingCameraScene):
    def construct(self):

        #Create the graph
        #createScene(self)

        g = createGraph()
        g2 = createGraph()
        self.play(Write(g))
        self.play( g2.animate.shift(RIGHT*5) )
        animateDFSAlgorithm(self, g, root)
        BFS(self, g2, root)
        #print(readInitData("inputdata"))
        # try:

        # except:
        #     print("Error al leer el archivo")


