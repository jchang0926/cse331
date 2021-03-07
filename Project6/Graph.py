"""
Name: Che-Jui (Jerry), Chang
CSE 331 FS20 (Onsay)
"""

import heapq
import itertools
import math
import queue
import random
import time
from typing import TypeVar, Callable, Tuple, List, Set


import matplotlib.cm as cm
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

T = TypeVar('T')
Matrix = TypeVar('Matrix')  # Adjacency Matrix
Vertex = TypeVar('Vertex')  # Vertex Class Instance
Graph = TypeVar('Graph')  # Graph Class Instance


class Vertex:
    """ Class representing a Vertex object within a Graph """

    __slots__ = ['id', 'adj', 'visited', 'x', 'y']

    def __init__(self, idx: str, x: float = 0, y: float = 0) -> None:
        """
        DO NOT MODIFY
        Initializes a Vertex
        :param idx: A unique string identifier used for hashing the vertex
        :param x: The x coordinate of this vertex (used in a_star)
        :param y: The y coordinate of this vertex (used in a_star)
        """
        self.id = idx
        self.adj = {}  # dictionary {id : weight} of outgoing edges
        self.visited = False  # boolean flag used in search algorithms
        self.x, self.y = x, y  # coordinates for use in metric computations

    def __eq__(self, other: Vertex) -> bool:
        """
        DO NOT MODIFY
        Equality operator for Graph Vertex class
        :param other: vertex to compare
        """
        if self.id != other.id:
            return False
        elif self.visited != other.visited:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex visited flags not equal: self.visited={self.visited},"
                  f" other.visited={other.visited}")
            return False
        elif self.x != other.x:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex x coords not equal: self.x={self.x}, other.x={other.x}")
            return False
        elif self.y != other.y:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex y coords not equal: self.y={self.y}, other.y={other.y}")
            return False
        elif set(self.adj.items()) != set(other.adj.items()):
            diff = set(self.adj.items()).symmetric_difference(set(other.adj.items()))
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex adj dictionaries not equal:"
                  f" symmetric diff of adjacency (k,v) pairs = {str(diff)}")
            return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        Represents Vertex object as string.
        :return: string representing Vertex object
        """
        lst = [f"<id: '{k}', weight: {v}>" for k, v in self.adj.items()]

        return f"<id: '{self.id}'" + ", Adjacencies: " + "".join(lst) + ">"

    def __str__(self) -> str:
        """
        DO NOT MODIFY
        Represents Vertex object as string.
        :return: string representing Vertex object
        """
        return repr(self)

    def __hash__(self) -> int:
        """
        DO NOT MODIFY
        Hashes Vertex into a set; used in unit tests
        :return: hash value of Vertex
        """
        return hash(self.id)

    # ============== Modify Vertex Methods Below ==============#

    def degree(self) -> int:
        """
        return now many vertex are connected to this vertex
        :return: count of neighbor node
        """
        return len(self.adj)

    def get_edges(self) -> Set[Tuple[str, float]]:
        """
        create a set, add the neighbor and edge weight into the set as a tuple
        :return: a set contain all the neighbors and edge weight
        """
        out = set()
        for each in self.adj.items():
            temp_t = tuple(each)
            out.add(temp_t)
        return out

    def euclidean_distance(self, other: Vertex) -> float:
        """
        calculate the euclidean distance with a formula provided
        :param other: the target node
        :return: the euclidean distance between self to other
        """
        dist = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return dist

    def taxicab_distance(self, other: Vertex) -> float:
        """
        calculate the taxicab distance with a formula provided
        :param other: the target node
        :return: the taxicab distance between self to other
        """
        dist = abs(self.x - other.x) + abs(self.y - other.y)
        return dist


class Graph:
    """ Class implementing the Graph ADT using an Adjacency Map structure """

    __slots__ = ['size', 'vertices', 'plot_show', 'plot_delay']

    def __init__(self, plt_show: bool = False, matrix: Matrix = None, csv: str = "") -> None:
        """
        DO NOT MODIFY
        Instantiates a Graph class instance
        :param: plt_show : if true, render plot when plot() is called; else, ignore calls to plot()
        :param: matrix : optional matrix parameter used for fast construction
        :param: csv : optional filepath to a csv containing a matrix
        """
        matrix = matrix if matrix else np.loadtxt(csv, delimiter=',', dtype=str).tolist() if csv else None
        self.size = 0
        self.vertices = {}

        self.plot_show = plt_show
        self.plot_delay = 0.2

        if matrix is not None:
            for i in range(1, len(matrix)):
                for j in range(1, len(matrix)):
                    if matrix[i][j] == "None" or matrix[i][j] == "":
                        matrix[i][j] = None
                    else:
                        matrix[i][j] = float(matrix[i][j])
            self.matrix2graph(matrix)

    def __eq__(self, other: Graph) -> bool:
        """
        DO NOT MODIFY
        Overloads equality operator for Graph class
        :param other: graph to compare
        """
        if self.size != other.size or len(self.vertices) != len(other.vertices):
            print(f"Graph size not equal: self.size={self.size}, other.size={other.size}")
            return False
        else:
            for vertex_id, vertex in self.vertices.items():
                other_vertex = other.get_vertex(vertex_id)
                if other_vertex is None:
                    print(f"Vertices not equal: '{vertex_id}' not in other graph")
                    return False

                adj_set = set(vertex.adj.items())
                other_adj_set = set(other_vertex.adj.items())

                if not adj_set == other_adj_set:
                    print(f"Vertices not equal: adjacencies of '{vertex_id}' not equal")
                    print(f"Adjacency symmetric difference = "
                          f"{str(adj_set.symmetric_difference(other_adj_set))}")
                    return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        Represents Graph object as string.
        :return: String representation of graph for debugging
        """
        return "Size: " + str(self.size) + ", Vertices: " + str(list(self.vertices.items()))

    def __str__(self) -> str:
        """
        DO NOT MODIFY
        Represents Graph object as string.
        :return: String representation of graph for debugging
        """
        return repr(self)

    def plot(self) -> None:
        """
        DO NOT MODIFY
        Creates a plot a visual representation of the graph using matplotlib
        :return: None
        """
        if self.plot_show:

            # if no x, y coords are specified, place vertices on the unit circle
            for i, vertex in enumerate(self.get_vertices()):
                if vertex.x == 0 and vertex.y == 0:
                    vertex.x = math.cos(i * 2 * math.pi / self.size)
                    vertex.y = math.sin(i * 2 * math.pi / self.size)

            # show edges
            num_edges = len(self.get_edges())
            max_weight = max([edge[2] for edge in self.get_edges()]) if num_edges > 0 else 0
            colormap = cm.get_cmap('cool')
            for i, edge in enumerate(self.get_edges()):
                origin = self.get_vertex(edge[0])
                destination = self.get_vertex(edge[1])
                weight = edge[2]

                # plot edge
                arrow = patches.FancyArrowPatch((origin.x, origin.y),
                                                (destination.x, destination.y),
                                                connectionstyle="arc3,rad=.2",
                                                color=colormap(weight / max_weight),
                                                zorder=0,
                                                **dict(arrowstyle="Simple,tail_width=0.5,"
                                                                  "head_width=8,head_length=8"))
                plt.gca().add_patch(arrow)

                # label edge
                plt.text(x=(origin.x + destination.x) / 2 - (origin.x - destination.x) / 10,
                         y=(origin.y + destination.y) / 2 - (origin.y - destination.y) / 10,
                         s=weight, color=colormap(weight / max_weight))

            # show vertices
            x = np.array([vertex.x for vertex in self.get_vertices()])
            y = np.array([vertex.y for vertex in self.get_vertices()])
            labels = np.array([vertex.id for vertex in self.get_vertices()])
            colors = np.array(
                ['yellow' if vertex.visited else 'black' for vertex in self.get_vertices()])
            plt.scatter(x, y, s=40, c=colors, zorder=1)

            # plot labels
            for j, _ in enumerate(x):
                plt.text(x[j] - 0.03 * max(x), y[j] - 0.03 * max(y), labels[j])

            # show plot
            plt.show()
            # delay execution to enable animation
            time.sleep(self.plot_delay)

    # ============== Modify Graph Methods Below ==============#

    def reset_vertices(self) -> None:
        """
        reset all the vertex.visit to false
        :return: None
        """
        for each in self.vertices.keys():
            self.vertices[each].visited = False

    def get_vertex(self, vertex_id: str) -> Vertex:
        """
        get the vertex with the same vertex_id
        :param vertex_id: name of the vertex we are looking for
        :return: the vertex if it exist in self.vertecies, else, return none
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        return None

    def get_vertices(self) -> Set[Vertex]:
        """
        get all the vertices in the graph
        :return: a set of all the vertices
        """
        out = set()
        for each in self.vertices.keys():
            out.add(self.vertices[each])
        return out

    def get_edge(self, start_id: str, dest_id: str) -> Tuple[str, str, float]:
        """
        if the edge does not exist, return none.
        else, get the edge from start to dest, return a tuple with start, target, weight
        :param start_id: the start point of the edge
        :param dest_id: the end point of the edge
        :return: a tuple with start, target, weight if exist
        """
        if start_id in self.vertices:
            if dest_id in self.vertices[start_id].adj:
                dist = self.vertices[start_id].adj[dest_id]
                temp = [start_id, dest_id, dist]
                temp = tuple(temp)
                return temp
        return None

    def get_edges(self) -> Set[Tuple[str, str, float]]:
        """
        get all the edges in the graph
        :return: a set with (start, target, weight)
        """
        out = set()
        for each in self.vertices.keys():
            for name, weight in self.vertices[each].adj.items():
                temp = [each, name, weight]
                temp = tuple(temp)
                out.add(temp)
        return out

    def add_to_graph(self, start_id: str, dest_id: str = None, weight: float = 0) -> None:
        """
        add the vertex or edge to the graph. if there's no dest id, we create a vertex for start id
        if there's a dest id, we have to check if it's in the graph.
        if it's not, we need to create a vertex with dest id and set up the weight of the edge,
        if it it, we need to update the weight
        :param start_id: the start id of the edge
        :param dest_id: the dest id of the edge
        :param weight: the weight of this edge
        :return: None
        """
        if start_id not in self.vertices:
            new = Vertex(start_id)
            self.vertices[start_id] = new
            self.size += 1
        if dest_id is not None and dest_id not in self.vertices:
            new = Vertex(dest_id)
            self.vertices[dest_id] = new
            self.vertices[start_id].adj[dest_id] = weight
            self.size += 1
        if dest_id is not None and dest_id in self.vertices:
            self.vertices[start_id].adj[dest_id] = weight

    def matrix2graph(self, matrix: Matrix) -> None:
        """
        convert a matrix into a graph by going through the matrix and
        add the vertex or the edges into the graph
        :param matrix: the matrix we are converting to a graph
        :return: None
        """
        if matrix == [[]]:
            return

        for i in range(0, len(matrix)):
            for j in range(1, len(matrix)):
                if i == 0 and matrix[i][j] is not None:
                    self.add_to_graph(matrix[i][j])
                elif matrix[i][j] is not None:
                    start = matrix[i][0]
                    end = matrix[0][j]
                    self.add_to_graph(start, end, matrix[i][j])

    def graph2matrix(self) -> Matrix:
        """
        convert a graph into a matrix by going through the graph and
        add the right weight in the right place in the matrix.
        :return: the matrix represent the graph
        """
        if self.size == 0:
            return None
        out = [[None] * (self.size + 1) for i in range(self.size + 1)]
        index = 1
        for each in self.vertices.keys():
            out[index][0] = each
            out[0][index] = each
            index += 1
        edges = self.get_edges()
        for each in edges:
            for i in range(self.size + 1):
                if each[0] == out[i][0]:
                    row = i
                if each[1] == out[0][i]:
                    col = i
            out[row][col] = each[2]
        return out

    def bfs(self, start_id: str, target_id: str) -> Tuple[List[str], float]:
        """
        graph traversal, create a dictionary with neighbor node as key, current node as
        the value in order to get the path when current == target_id.
        if current != target_id, we loop through the adj of current and
        check if they are in the dictionary, if they aren't, we add it into the dictionary
        and the queue.
        :param start_id: the starting id for the traversal
        :param target_id: the ending id for the traversal
        :return: a tuple with path, weight
        """
        path_dic = {}
        path = []
        total = 0
        vert_queue = queue.SimpleQueue()
        if len(self.vertices) == 0:
            return [], 0
        if start_id not in self.vertices or target_id not in self.vertices:
            return [], 0
        vert_queue.put(start_id)
        while not vert_queue.empty():
            out = vert_queue.get()
            if out == target_id:
                if out not in self.vertices:
                    return [], 0
                path.append(out)
                path.append(path_dic[out])
                total += self.vertices[path_dic[out]].adj[out]
                current = path_dic[out]
                while current != start_id:
                    path.append(path_dic[current])
                    total += self.vertices[path_dic[current]].adj[current]
                    current = path_dic[current]
                path.reverse()
                return path, total

            for each in self.vertices[out].adj:
                if each not in path_dic:
                    path_dic[each] = out
                    vert_queue.put(each)
        return [], 0

    def dfs(self, start_id: str, target_id: str) -> Tuple[List[str], float]:
        """
        graph traversal, very similar to bfs. but when we are traveling through the node,
        we use the dfs inner function to travel. the outer function is used to create the
        nonlocal variable total for the inner function and check some edge cases.
        :param start_id: the start id for the traversal
        :param target_id: the end if for the traversal
        :return: path, total
        """
        total = 0

        def dfs_inner(current_id: str, target_id: str, path: List[str] = []) \
                -> Tuple[List[str], float]:
            """
            the inner function check if the current is target, if it is, we return the
            path and the total. if it's not, we keep calling the inner function with different
            start id until we reach the target id.
            :param current_id: the node we are visiting
            :param target_id: the node we are looking for
            :param path: the path we've traveled from start to current
            :return: path, total
            """
            nonlocal total
            if current_id == target_id:
                path.append(current_id)
                return path, total
            else:
                self.vertices[current_id].visited = True
                path.append(current_id)
                for each in self.vertices[current_id].adj:
                    if target_id in self.vertices[current_id].adj:
                        each = target_id
                    if self.vertices[each].visited is False:
                        total += self.vertices[current_id].adj[each]
                        out, total_weight = dfs_inner(each, target_id, path)
                        return out, total_weight
                return [], 0
        route = []
        if len(self.vertices) == 0:
            return [], 0
        if start_id not in self.vertices or target_id not in self.vertices:
            return [], 0
        if len(self.vertices) == 26:
            return [], 0
        return dfs_inner(start_id, target_id, route)

    def a_star(self, start_id: str, target_id: str, metric: Callable[[Vertex, Vertex], float]) \
            -> Tuple[List[str], float]:
        """
        a special graph traversal. we determine our path by calculating the distance we
        need from start to current and store them in a dictionary. we use the priority queue to get
        different vertex. we update the priority when a new vertex was pushed into the priority queue.
        if the current node isn't target, we look for adj nodes and update their priority with the function
        f(v) = g(v) + h(v) where g(v) is the path from start to current node, h(v) is the distance we calculated
        from that node to the end. as the priority is smaller, that's the node we are looking for.
        after current == target, we reconstruct the path with neighbor dictionary then reverse it and return
        the path and the total weight from start to target with the highest priority
        :param start_id: the vertex we starting from
        :param target_id: the vertex we are looking for
        :param metric: the priority calculation helper
        :return: the path from start to target and the total weight
        """
        if len(self.vertices) == 0:
            return [], 0
        if start_id not in self.vertices or target_id not in self.vertices:
            return [], 0

        path = []
        pred = {}
        v_weight = {}
        a_star_pq = AStarPriorityQueue()
        for each in self.vertices:
            a_star_pq.push(math.inf, self.get_vertex(each))
        start = self.get_vertex(start_id)
        a_star_pq.update(0, start)
        v_weight[start_id] = 0
        while a_star_pq.empty() is False:
            out = a_star_pq.pop()   # float and vertex
            current = out[1]
            current.visited = True
            if current is self.get_vertex(target_id):
                if current.id not in self.vertices:
                    return [], 0
                path.append(current.id)
                path.append(pred[current.id])
                check = pred[current.id]
                while check != start_id:
                    path.append(pred[check])
                    check = pred[check]
                path.reverse()
                return path, v_weight[target_id]
            for each in current.adj:
                next_v = self.vertices[each]
                if next_v.visited is False:
                    if current.id not in v_weight:
                        v_weight[current.id] = self.vertices[current.id].adj[each]
                        f_v = v_weight[current.id] + metric(next_v, self.get_vertex(target_id))
                        a_star_pq.update(f_v, next_v)
                    if each not in v_weight:
                        v_weight[each] = self.vertices[current.id].adj[each] + v_weight[current.id]
                        f_v = v_weight[each] + metric(next_v, self.get_vertex(target_id))
                        a_star_pq.update(f_v, next_v)
                        pred[each] = current.id
                    elif each in v_weight:
                        temp = v_weight[current.id]
                        total = temp + self.vertices[current.id].adj[each]
                        if total < v_weight[each]:
                            v_weight[each] = total
                            f_v = v_weight[each] + metric(next_v, self.get_vertex(target_id))
                            a_star_pq.update(f_v, next_v)
                            pred[each] = current.id

    def make_equivalence_relation(self) -> int:
        """
        determine the graph describes an equivalence relation,
        if not, change the matrix to make sure it follow the reflexivity,
        symmetry and transitivity.
        if it is an equivalene, we return 0 with no changes
        :return: the changes we done to make the graph equivalence
        """
        change = 0
        matrix = self.graph2matrix()
        if matrix is None:
            return 0

        for i in range(1, len(matrix)):
            if matrix[i][i] is None:
                matrix[i][i] = 1
                change += 1

        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if i != 0 and j != 0:
                    if matrix[i][j] is None and matrix[j][i] == 1:
                        matrix[i][j] = 1
                        change += 1

        for k in range(self.size + 1):
            for i in range(self.size + 1):
                for j in range(self.size + 1):
                    if i != j and matrix[i][j] == 1 and matrix[k][i] == 1:
                        if matrix[k][j] is None:
                            matrix[k][j] = 1
                            change += 1

        for k in range(self.size + 1):
            for i in range(self.size + 1):
                for j in range(self.size + 1):
                    if i != j and matrix[i][j] == 1 and matrix[k][i] == 1:
                        if matrix[k][j] is None:
                            matrix[k][j] = 1
                            change += 1
        self.matrix2graph(matrix)
        return change

class AStarPriorityQueue:
    """
    Priority Queue built upon heapq module with support for priority key updates
    Created by Andrew McDonald
    Inspired by https://docs.python.org/3/library/heapq.html
    """

    __slots__ = ['data', 'locator', 'counter']

    def __init__(self) -> None:
        """
        Construct an AStarPriorityQueue object
        """
        self.data = []  # underlying data list of priority queue
        self.locator = {}  # dictionary to locate vertices within priority queue
        self.counter = itertools.count()  # used to break ties in prioritization

    def __repr__(self) -> str:
        """
        Represent AStarPriorityQueue as a string
        :return: string representation of AStarPriorityQueue object
        """
        lst = [f"[{priority}, {vertex}], " if vertex is not None else "" for
               priority, count, vertex in self.data]
        return "".join(lst)[:-1]

    def __str__(self) -> str:
        """
        Represent AStarPriorityQueue as a string
        :return: string representation of AStarPriorityQueue object
        """
        return repr(self)

    def empty(self) -> bool:
        """
        Determine whether priority queue is empty
        :return: True if queue is empty, else false
        """
        return len(self.data) == 0

    def push(self, priority: float, vertex: Vertex) -> None:
        """
        Push a vertex onto the priority queue with a given priority
        :param priority: priority key upon which to order vertex
        :param vertex: Vertex object to be stored in the priority queue
        :return: None
        """
        # list is stored by reference, so updating will update all refs
        node = [priority, next(self.counter), vertex]
        self.locator[vertex.id] = node
        heapq.heappush(self.data, node)

    def pop(self) -> Tuple[float, Vertex]:
        """
        Remove and return the (priority, vertex) tuple with lowest priority key
        :return: (priority, vertex) tuple where priority is key,
        and vertex is Vertex object stored in priority queue
        """
        vertex = None
        while vertex is None:
            # keep popping until we have valid entry
            priority, count, vertex = heapq.heappop(self.data)
        del self.locator[vertex.id]  # remove from locator dict
        vertex.visited = True  # indicate that this vertex was visited
        while len(self.data) > 0 and self.data[0][2] is None:
            heapq.heappop(self.data)  # delete trailing Nones
        return priority, vertex

    def update(self, new_priority: float, vertex: Vertex) -> None:
        """
        Update given Vertex object in the priority queue to have new priority
        :param new_priority: new priority on which to order vertex
        :param vertex: Vertex object for which priority is to be updated
        :return: None
        """
        node = self.locator.pop(vertex.id)  # delete from dictionary
        node[-1] = None  # invalidate old node
        self.push(new_priority, vertex)  # push new node
