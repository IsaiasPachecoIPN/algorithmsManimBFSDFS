from manim import *
from utils import *

root = 0
DEFAULT_GRAPH_LAYOUT = "spring"
DEFAULT_GRAPH_SCALE = 2
SHOW_LABELS = True
IS_ANIMATED = True
DEFAULT_ROOT_COLOR = "#01BEFF"
DEFAULT_VISITED_COLOR = "#FFD501"
DAFAULT_GOTO_COLOR = "#9701FF"
#Decreasing the value config.frame_width will zoom in the Mobject
DEFAULT_FRAME_WIDTH = 15

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
    global DEFAULT_GRAPH_LAYOUT
    global DEFAULT_GRAPH_SCALE
    global SHOW_LABELS

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
            elif "graph_layout" in line:
                layout_line = line.strip().split(":")
                DEFAULT_GRAPH_LAYOUT = layout_line[1]
            elif "graph_scale" in line:
                scale_line = line.strip().split(":")
                DEFAULT_GRAPH_SCALE = float(scale_line[1])
            elif "show_labels" in line:
                show_labels_line = line.strip().split(":")
                SHOW_LABELS = True if show_labels_line[1] == "true" else False
                print("SHOW_LABELS:", SHOW_LABELS)

    print("vertices:", arr_vertices)
    print("edges:", arr_edges)
    print("root:", root)
    print("show_labels:", SHOW_LABELS)
    return [arr_vertices, arr_edges]


def getShowLabels():
    """
    Function to get the show labels value
    """
    return SHOW_LABELS

def createGraph():
    """
    Function to create the graph
    """
    values = readInitData("inputdata")
    g = Graph(values[0], values[1], labels=SHOW_LABELS, layout_scale=DEFAULT_GRAPH_SCALE, layout=DEFAULT_GRAPH_LAYOUT)
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

        self.camera.frame.set(width = DEFAULT_FRAME_WIDTH)
        self.camera.frame.shift(RIGHT * (DEFAULT_FRAME_WIDTH/2) - (5))
        self.camera.frame.shift(UP * DEFAULT_GRAPH_SCALE * (DEFAULT_GRAPH_SCALE+0.5)) 

        g = createGraph()
        print("g:", g._labels)
        [ g._labels[i].scale(0.5) for i in g._labels.keys() ]
        g2 = createGraph()
        [ g2._labels[i].scale(0.5) for i in g2._labels.keys() ]
        #print("g2:", g2)

        #Create title fro graph
        title_a = Text("BFS", color=BLUE)
        title_a.next_to(g, UP)

        g2.next_to(g, RIGHT*5)

        title_b = Text("DFS", color=BLUE)
        title_b.next_to(g2, UP)

        self.play( AnimationGroup(
            Write(title_a),
            Write(g),
        ))

        self.play(
            AnimationGroup(
                Write(title_b),
                Write(g2),
            )
        )

        BFS(self, g, root)
        animateDFSAlgorithm(self, g2, root)
        self.wait(5)


