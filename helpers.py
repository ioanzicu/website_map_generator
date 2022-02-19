import webbrowser
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from webpage_parser import WebpageParser


def show_graph(parser: WebpageParser, root_link: str) -> None:
    '''
    Generate a html page with representation of the graph.
    '''
    if not isinstance(parser, WebpageParser):
        raise ValueError(
            f'The parser type is {type(parser)}, expected to be of type WebpageParser')

    graph_dict = parser.get_graph_dict()

    if not isinstance(graph_dict, dict):
        raise ValueError(
            f'The graph_dict type is {type(graph_dict)}, expected to be of type dict')

    # VISUALISATION
    plt.rcParams.update({'font.size': 5})
    G = nx.Graph()
    nt = Network(height='1000px', width='100%', directed=True)

    nx_graph = nx.Graph()
    nx_graph.add_node(root_link)
    for key_root, value_edges in graph_dict.items():
        edges_len = len(value_edges) if len(value_edges) > 20 else 20
        nx_graph.add_node(key_root, label=f'{parser.get_link_status_code(link=key_root)}',
                          title=f'{parser.get_link_info_formatted_string(key_root)}',
                          size=2.1 * edges_len, width=20, group=key_root)

        nx_graph.add_weighted_edges_from([(src, dest, weight*5)
                                          for (src, dest, weight) in value_edges], arrowStrikethrough=True)

    nx.draw_shell(G, with_labels=False, font_size=4, font_weight='bold')
    nt.from_nx(nx_graph)
    nt.show_buttons(filter_=['nodes', 'edges', 'physics'])
    nt.barnes_hut(gravity=-20000000, central_gravity=0, spring_length=4000,
                  spring_strength=0.001, damping=0.75, overlap=0.75)
    nt.show(f'{root_link.split(".")[1]}_map.html')