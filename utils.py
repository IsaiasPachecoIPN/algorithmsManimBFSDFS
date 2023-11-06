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

explored = []
dfs_res = []
dfs_res.append([])
_counter = 0

def DFS( scene, graph, u , isInside = False):

    global _counter

    if u not in explored:
        #print("Node:", u)
        dfs_res[_counter].append(u)
        explored.append(u)
        for v in getIncidentNodes(graph, u):
            #print("Edge:", (u,v))
            DFS(scene, graph, v, True)
        #print("End for")
        dfs_res.append([])
        _counter += 1

def lookForAncestors( graph, dfs_res ):
    for i in range(1,len(dfs_res)):
        dfs_res[i].insert( 0, getIncidentNodes(graph, dfs_res[i][0])[0])

def showDFS( scene, graph, root):
    DFS(scene, graph, root)
    res = [ x for x in dfs_res if x != [] ]
    lookForAncestors(graph, res)    
    print("dfs_res:", res)
    return res

def crearPares(arreglo):
  pares = []
  for i in range(len(arreglo) - 1):
    pares.append((arreglo[i], arreglo[i + 1]))
  return pares

def animateDFSAlgorithm( scene, graph, root ):
    
    dfs_res = showDFS(scene, graph, root)
    print("Graph vertices: ", graph.vertices)
    vertices_coords = [ graph.vertices[key].get_center() for key in graph.vertices.keys() ]
    print("vertices_coords:", vertices_coords)

    for idx, arr_node in enumerate(dfs_res):
        edges_to_animate = crearPares(arr_node)
        print("edges_to_animate:", edges_to_animate)

        if IS_ANIMATED:
            scene.play(
                AnimationGroup(
                    #Color all nodes
                    * [ graph.vertices[j].animate.set_color(DEFAULT_VISITED_COLOR) for j in arr_node ],
                    #Color all edges
                    * [ graph.edges[getEdgeFromGraph(graph, j)].animate.set_color(DEFAULT_VISITED_COLOR) for j in edges_to_animate ],
                )
            )

            #Print initial node
            #print("arr_node[0]:", arr_node[0])
            for i, steps in enumerate(edges_to_animate):
                start_node = steps[0]
                end_node = steps[1]

                scene.play(
                    AnimationGroup(
                        Flash( graph.vertices[start_node], color=RED, line_length=0.2, flash_radius=0.5 ),
                        graph.vertices[start_node].animate.set_color(DEFAULT_ROOT_COLOR),
                        graph.vertices[start_node].animate.move_to(graph.vertices[end_node]),
                        graph.edges[getEdgeFromGraph(graph, steps)].animate.set_color(DEFAULT_ROOT_COLOR),
                    ), lag_ratio=0.5
                )
            #print("moving: {} to {}".format(arr_node[0], vertices_coords[arr_node[0]-1]))
            #graph.vertices[arr_node[0]].move_to(vertices_coords[arr_node[0]-1])
            #scene.wait(0.5)
            # arr_anim = []
            # for node in graph.vertices.keys():
            #     arr_anim.append(graph.vertices[node].move_to(vertices_coords[node-1]))

            [ graph.vertices[key].move_to(vertices_coords[key-1]) for key in arr_node ]

            # scene.play(
            #     AnimationGroup(
            #         * [ graph.vertices[key].animate.move_to(vertices_coords[key-1]) for key in arr_node ],
            #     ), lag_ratio=0.5
            # )

            # scene.play(
            #     AnimationGroup(
            #         Flash(graph.vertices[elem], color=RED, line_length=0.2, flash_radius=0.5),
            #         graph.vertices[elem].animate.set_color(DEFAULT_ROOT_COLOR),
            #         graph.vertices[key].animate.move_to(graph.vertices[elem]),
            #         graph.edges[getEdgeFromGraph(graph, (key,elem))].animate.set_color(DEFAULT_ROOT_COLOR),
            #     ),lag_ratio=0.5
            # )
            # graph.vertices[key].move_to(key_position)

        # if IS_ANIMATED: scene.play( graph.vertices[i[0]].animate.set_color(DEFAULT_ROOT_COLOR) )

        
        # animation_elems =  crearPares(i)
        # print("animation_elems:", animation_elems)
        
        