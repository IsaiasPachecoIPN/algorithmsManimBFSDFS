from main import *

IS_ANIMATED = True
DEFAULT_ROOT_COLOR = "#01BEFF"
DEFAULT_VISITED_COLOR = "#FFD501"
DAFAULT_GOTO_COLOR = "#9701FF"
SHOW_LABELS = False

def crear_tonos_color(color, cantidad_tonos):
  """
  Crea un arreglo de colores en diferentes tonalidades para el color especificado.

  Args:
    color: El color a partir del cual se crearán los tonos.
    cantidad_tonos: La cantidad de tonos que se crearán.

  Returns:
    Un arreglo de colores.
  """

  colores = []

  for i in range(cantidad_tonos):
    # Obtenemos el valor del tono actual.
    tono = i / (cantidad_tonos - 1)

    # Ajustamos el valor del tono para cada componente del color.
    rojo = int(color[0] + (255 - color[0]) * tono)
    verde = int(color[1] + (255 - color[1]) * tono)
    azul = int(color[2] + (255 - color[2]) * tono)

    # Creamos el nuevo color con los valores ajustados.
    nuevo_color = "#%02x%02x%02x" % (rojo, verde, azul)

    colores.append(nuevo_color)

  return colores

def getEdgeFromGraph(graph, key):
    """
    Function to get the edge from the graph
    (param) graph : graph to consider
    (param) key : key to consider
    """
    if key in graph.edges.keys() or (key[1], key[0]) in graph.edges.keys():
        return key if key in graph.edges.keys() else (key[1], key[0])

def getIncidentNodes(graph, node):
    """
    Function to get the incident nodes to a node
    (param) graph : graph to consider
    (param) node : node to consider
    """
    incident_nodes = []
    for edge in graph.edges.keys():
        if node in edge:
            incident_nodes.append(edge[0] if edge[0] != node else edge[1])
    #print("incident_nodes:", incident_nodes)
    return incident_nodes


def animteNodeMovement( scene, graph, key, bfs_tree_dic ):
    """
    Function to animate the node movement
    """

    animations = []
    for i in bfs_tree_dic[key]:
        #Clone the key node and then move it to the i node
        new_node = graph.vertices[key].copy()
        scene.add(new_node)
        animations.append(new_node.move_to(graph.vertices[i]))
    
    return animations

def animateBFSAlgorithm(scene, graph, bfs_tree_dic):
    """
    Function to animate the BFS for the graph
    """
    for key in bfs_tree_dic.keys():
        if bfs_tree_dic[key] != []:
            scene.play(
                AnimationGroup(
                    * [ graph.vertices[i].animate.set_color(DEFAULT_VISITED_COLOR) for i in bfs_tree_dic[key] ],
                    * [ graph.edges[getEdgeFromGraph(graph, (key,i))].animate.set_color(DEFAULT_VISITED_COLOR) for i in bfs_tree_dic[key] ],
                )
            )

            key_position = graph.vertices[key].get_center()
            for elem in bfs_tree_dic[key]:
                scene.play(
                    AnimationGroup(
                        Flash(graph.vertices[elem], color=RED, line_length=0.2, flash_radius=0.5),
                        graph.vertices[elem].animate.set_color(DEFAULT_ROOT_COLOR),
                        graph.vertices[key].animate.move_to(graph.vertices[elem]),
                        graph.edges[getEdgeFromGraph(graph, (key,elem))].animate.set_color(DEFAULT_ROOT_COLOR),
                    ),lag_ratio=0.5
                )
                graph.vertices[key].move_to(key_position)


def BFS( scene, graph, root ):

    visited = []
    layers = []

    visited.append(root)
    layers.append([root])

    if IS_ANIMATED: scene.play(graph.vertices[root].animate.set_color(DEFAULT_ROOT_COLOR))

    layer_count = 0
    bfs_tree = []
    bfs_tree_dic = {}

    while len(layers[layer_count]) > 0:
        #new_layer = [layer_count+1]
        layers.append([])
        #print("layers:", layers)
        for node in layers[layer_count]:
            #consider each node (node,v) incident to node
            bfs_tree_dic[node] = []
            for v in getIncidentNodes(graph, node):
                if v not in visited:
                    visited.append(v)
                    layers[layer_count+1].append(v)
                    bfs_tree_dic[node].append(v)
                    bfs_tree.append((node,v))
        layer_count += 1
    print("bfs_tree:", bfs_tree)
    print("bfs_tree_dic:", bfs_tree_dic)
    if IS_ANIMATED: animateBFSAlgorithm(scene, graph, bfs_tree_dic)
    return bfs_tree

