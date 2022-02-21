from app.webpage_parser import WebpageParser, FileManager, DFS
from app.helpers import show_graph, dijsktra


if __name__ == '__main__':

    local_data = True

    root: str = 'https://www.globalapptesting.com'
    webparser = WebpageParser(
        root_link=root, file_manager=FileManager(), DFS=DFS)

    if not local_data:
        print('Geather data from the internet...')
        webparser.generate_and_save_graph()

    else:
        print('Load data from local files...')
        graph_dict = webparser.load_graph_dict_from_json('graph_dict')
        webparser.load_map_dict_from_json('map_dict')

    # show_graph(parser=webparser, root_link=root)
    stat = webparser.get_webpage_statistics()
    print(stat, end='\n\n')

    start_node = 'https://www.globalapptesting.com'
    target_node = 'https://www.globalapptesting.com/customers/facebook'
    parent, node_dependencies = dijsktra(adj_list_graph=graph_dict,
                                         start_node=start_node,
                                         target_node=target_node)

    print('Shortest path between:', start_node, ' to ', target_node,
          ' are ',  node_dependencies[target_node], ' pages.')
