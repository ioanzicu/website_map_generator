from app.webpage_parser import WebpageParser, FileManager
from app.graph import Graph
from app.helpers import show_graph, get_webpage_statistics


if __name__ == '__main__':

    local_data = True

    root: str = 'https://www.globalapptesting.com'
    webparser = WebpageParser(root_link=root, file_manager=FileManager())
    webpage_graph = {}
    if not local_data:
        print('Geather data from the internet...')
        adj_list_graph = webparser.generate_and_save_map_dict()
        webpage_graph = Graph(adj_list_graph=adj_list_graph,
                              file_manager=FileManager())
        webpage_graph.write_adj_list_graph_to_json_file()
    else:
        print('Load data from local files...')
        webpage_graph = Graph(adj_list_graph={},
                              file_manager=FileManager())
        webpage_graph.load_adj_list_graph_from_json('adj_list_graph')
        webparser.load_map_dict_from_json('map_dict')

    show_graph(graph=webpage_graph, parser=webparser, root_link=root)
    stat = get_webpage_statistics(root_link=root,
                                  webpage_parser=webparser,
                                  graph=webpage_graph)
    print(stat, end='\n\n')

    start_node = 'https://www.globalapptesting.com'
    target_node = 'https://www.globalapptesting.com/customers/facebook'
    parent, node_dependencies = webpage_graph.dijsktra(start_node=start_node,
                                                       target_node=target_node)

    print('Shortest path between:', start_node, ' to ', target_node,
          ' are ',  node_dependencies[target_node], ' pages.')
