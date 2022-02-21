
class DFS():
    def __init__(self, adj_list_graph: dict) -> None:
        self.adj_list_graph: dict = adj_list_graph
        self.visited: dict = {}
        self.node_dependencies: dict = {}

    def get_longest_path(self) -> int:

        if not self.adj_list_graph:
            raise ValueError('The graph_dict is empty')

        self.visited = dict.fromkeys(self.adj_list_graph, False)
        # node connections
        self.node_dependencies = dict.fromkeys(self.adj_list_graph, 0)

        # Iterate over each node
        for current_node in self.adj_list_graph.keys():
            # call dfs if it was not visited yet
            if not self.visited[current_node]:
                self.dfs(current_node=current_node)

        longest_path = 0
        # find the longest path
        for dependency in self.node_dependencies.values():
            longest_path = max(dependency, longest_path)
        return longest_path

    def dfs(self, current_node: str) -> None:
        '''Depth First Search'''

        # recursion base case
        if self.visited[current_node]:
            return

        self.visited[current_node] = True

        # recurrently check each neighbor
        for _, neighbor_node, _ in self.adj_list_graph[current_node]:
            if not self.visited[neighbor_node]:
                self.dfs(current_node=neighbor_node)

            # get the maximum value - the longest path between current and neighbor node
            self.node_dependencies[current_node] = max(self.node_dependencies[current_node],
                                                       self.node_dependencies[neighbor_node] + 1)
