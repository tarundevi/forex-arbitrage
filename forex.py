# Python3 program for Bellman-Ford's single source
# shortest path algorithm with negative cycle detection.

class Graph:

    def __init__(self, vertices):
        self.V = vertices  # Number of vertices
        self.graph = []  # List to store graph edges

    # Function to add an edge to the graph
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    # Utility function to print the negative weight cycle and its weight
    def printNegativeCycle(self, parent, start):
        cycle = []
        cycle_weight = 0
        current = start

        # Traverse the parent chain to get the cycle
        while True:
            cycle.append(current)
            prev = parent[current]
            # Find the edge weight from prev to current
            for u, v, w in self.graph:
                if u == prev and v == current:
                    cycle_weight += w
                    break
            current = prev
            if current in cycle:  # Cycle detected
                cycle.append(current)
                cycle_start = cycle.index(current)
                cycle = cycle[cycle_start:]  # Only print the cycle part
                break

        print("Negative weight cycle found:", " -> ".join(map(str, cycle)))
        print("Weight of the cycle:", cycle_weight)


    def BellmanFord(self, src):

        # Step 1: Initialize distances from src to all other vertices as infinite
        dist = [float("Inf")] * self.V
        parent = [-1] * self.V  # Array to store the parent of each vertex
        dist[src] = 0

        # Step 2: Relax all edges |V| - 1 times
        for _ in range(self.V - 1):
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u

        # Step 3: Check for negative-weight cycles
        for u, v, w in self.graph:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                print("Graph contains a negative weight cycle.")
                # Call function to print the negative weight cycle and its weight
                self.printNegativeCycle(parent, v)
                return  # Exit after finding one cycle

        # Print all distances if there is no negative weight cycle
        self.printArr(dist)

    # Utility function used to print the solution
    def printArr(self, dist):
        print("Vertex Distance from Source")
        for i in range(self.V):
            print("{0}\t\t{1}".format(i, dist[i]))



# Driver's code
if __name__ == '__main__':
    g = Graph(5)
    g.addEdge(0, 1, -1)
    g.addEdge(0, 2, 4)
    g.addEdge(1, 2, 3)
    g.addEdge(1, 3, 2)
    g.addEdge(1, 4, 2)
    g.addEdge(3, 2, 5)
    g.addEdge(3, 1, 1)
    g.addEdge(4, 3, -3)

    # Function call
    g.BellmanFord(0)
