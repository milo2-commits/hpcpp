'''
Madhur Jaripatke
Roll No. 50
BE A Computer
RMDSSOE, Warje, Pune

Problem Statement: Design and implement Parallel Breadth First Search and Depth First Search based on existing 
algorithms using OpenMP. Use a Tree or an undirected graph for BFS and DFS.
'''

from collections import deque
import multiprocessing as mp
from multiprocessing import Pool

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]
    
    def add_edge(self, v1, v2):
        self.graph[v1].append(v2)
        self.graph[v2].append(v1)
    
    def sequential_bfs(self, start):
        visited = [False] * self.V
        queue = deque([start])
        visited[start] = True
        
        print(f"Sequential BFS starting from vertex {start}:", end=" ")
        while queue:
            vertex = queue.popleft()
            print(vertex, end=" ")
            
            for neighbor in self.graph[vertex]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        print()

    def process_level(self, args):
        vertex, visited = args
        neighbors = []
        for neighbor in self.graph[vertex]:
            if not visited[neighbor]:
                neighbors.append(neighbor)
        return neighbors

    def parallel_bfs(self, start):
        visited = mp.Manager().list([False] * self.V)
        visited[start] = True
        current_level = [start]
        
        print(f"Parallel BFS starting from vertex {start}:", end=" ")
        
        pool = Pool(processes=4)
        while current_level:
            print(*current_level, end=" ")
            
            # Process next level in parallel
            args = [(v, visited) for v in current_level]
            next_level = []
            
            for neighbors in pool.map(self.process_level, args):
                for n in neighbors:
                    if not visited[n]:
                        visited[n] = True
                        next_level.append(n)
            
            current_level = next_level
        print()
        pool.close()

def main():
    g = Graph(8)
    
    # Create the same test graph
    edges = [(0,1), (0,2), (1,3), (1,4), (2,5), (2,6), (6,7)]
    for v1, v2 in edges:
        g.add_edge(v1, v2)
    
    # Test both implementations
    g.sequential_bfs(0)
    g.parallel_bfs(0)

if __name__ == "__main__":
    main()
