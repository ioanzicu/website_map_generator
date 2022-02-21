import sys
import heapq
from app.file_manager import FileManager


class Graph:
    def __init__(self, adj_list_graph: dict, file_manager: FileManager) -> None:
        self.adj_list_graph = adj_list_graph
        self.file_manager = file_manager
        self.visited: dict = {}
        self.node_dependencies: dict = {}

    def get_adj_list_graph(self) -> dict:
        return self.adj_list_graph

    def get_nodes_with_min_max_links(self):
        '''
        Returns a list of node(s) with minimum and maximum number of links.
        '''

        incoming_links_counter = self.count_incoming_edges()

        min = sys.maxsize
        max = 0
        for key_link, incoming_count in incoming_links_counter.items():
            if min > incoming_count:
                min = incoming_count
            if max < incoming_count:
                max = incoming_count

        min_links = []
        max_links = []

        for key_link, incoming_count in incoming_links_counter.items():
            if min == incoming_count:
                min_links.append(key_link)
            elif max == incoming_count:
                max_links.append(key_link)

        return {
            'minimum_incoming_links': {'links': min_links, 'incoming_links_count': min},
            'maximum_incoming_links': {'links': max_links, 'incoming_links_count': max}
        }

    def count_incoming_edges(self) -> dict:
        '''
        Count the number of incoming (inbound or backlinks) edges for each node.
        '''

        if not self.adj_list_graph:
            raise ValueError('The adj_list_graph is empty')

        incoming_links_counter = dict.fromkeys(self.adj_list_graph, 0)

        for _, value_list in self.adj_list_graph.items():
            for (_, destination, _) in value_list:
                incoming_links_counter[destination] = incoming_links_counter.get(
                    destination, 0) + 1

        return incoming_links_counter

    def load_adj_list_graph_from_json(self, file_name: str) -> dict:
        '''
        Load the adj_list_graph dictionary from a json file.
        '''
        self.adj_list_graph = self.file_manager.load_from_json(
            file_name=file_name)
        return self.adj_list_graph

    def write_adj_list_graph_to_json_file(self, file_name: str = 'adj_list_graph') -> None:
        '''
        Write / Dump the adj_list_graph dict into json file.
        '''

        if not self.adj_list_graph:
            raise ValueError('The adj_list_graph is empty')
        self.file_manager.write_to_file(
            file_name=file_name, data=self.adj_list_graph)

    def dijsktra(self, start_node: str, target_node: str):
        '''Shortest path, iterative version - dijsktra algorithm'''
        if not self.adj_list_graph:
            raise ValueError('The adj_list_graph is empty')

        node_dependencies = {start_node: 0}
        parent = {start_node: None}
        priority_queue = [(0, start_node)]
        visited = set()
        while priority_queue:
            distance, current_node = heapq.heappop(priority_queue)
            if current_node in visited:
                continue
            if current_node == target_node:
                break
            visited.add(current_node)
            for _, neighbor_node, _ in self.adj_list_graph[current_node]:
                if neighbor_node not in node_dependencies or node_dependencies[neighbor_node] > distance + 1:
                    node_dependencies[neighbor_node] = distance + 1
                    parent[neighbor_node] = current_node
                    heapq.heappush(
                        priority_queue, (node_dependencies[neighbor_node], neighbor_node))

        return parent, node_dependencies

    def get_longest_path(self) -> int:
        '''Get the longest path in the graph using Depth First Search algorithm, recursive version'''

        if not self.adj_list_graph:
            raise ValueError('The adj_list_graph is empty')

        self.visited = dict.fromkeys(self.adj_list_graph, False)
        # node connections
        self.node_dependencies = dict.fromkeys(self.adj_list_graph, 0)

        # Iterate over each node
        for current_node in self.adj_list_graph.keys():
            # call dfs if it was not visited yet
            if not self.visited[current_node]:
                self.__dfs(current_node=current_node)

        longest_path = 0
        # find the longest path
        for dependency in self.node_dependencies.values():
            longest_path = max(dependency, longest_path)
        return longest_path

    def __dfs(self, current_node: str) -> None:
        '''Depth First Search - recursive version'''

        # recursion base case
        if self.visited[current_node]:
            return

        self.visited[current_node] = True

        # recurrently check each neighbor
        for _, neighbor_node, _ in self.adj_list_graph[current_node]:
            if not self.visited[neighbor_node]:
                self.__dfs(current_node=neighbor_node)

            # get the maximum value - the longest path between current and neighbor node
            self.node_dependencies[current_node] = max(self.node_dependencies[current_node],
                                                       self.node_dependencies[neighbor_node] + 1)
