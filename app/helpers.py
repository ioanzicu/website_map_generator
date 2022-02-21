import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from collections import Counter
from app.webpage_parser import WebpageParser
from app.graph import Graph


def show_graph(graph: Graph, parser: WebpageParser, root_link: str) -> None:
    '''
    Generate a html page with representation of the graph.
    '''
    if not isinstance(parser, WebpageParser):
        raise ValueError(
            f'The parser type is {type(parser)}, expected to be of type WebpageParser')

    graph_dict = graph.get_adj_list_graph()

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


def get_webpage_statistics(root_link: str, webpage_parser: WebpageParser, graph: Graph) -> str:
    '''
    Compute the basic metrics:
        - total number of web pages found
        - total number of internal links 
        - total number of external links
        - total number of dead / invalid links
        - total numner of phone links 
        - total numner of email links
        - total numner of image links
        - average number of internal links per page
        - average number of external links per page
        - average size (in bytes) per page
        - minimum incoming links count and list of pages
        - maximum incoming links count and list of pages
        - distance between the most distant subpages (longest path)
    '''

    map_dict = webpage_parser.get_map_dict()

    if not map_dict:
        return 'The map_dict is empty'

    total_webpages = len(map_dict.keys())

    total_internal_links = 0
    total_external_links = 0
    total_dead_links = 0
    total_phone_links = 0
    total_email_links = 0
    total_file_links = 0
    total_page_size_bytes = 0
    http_statuses = []
    for _, value_dict in map_dict.items():

        http_statuses.append(value_dict['HTTP_STATUS'])

        total_internal_links += len(value_dict['internal_links'])
        total_external_links += len(value_dict['external_links'])
        total_dead_links += len(value_dict['dead_links'])
        total_phone_links += len(value_dict['phone_links'])
        total_email_links += len(value_dict['email_links'])
        total_file_links += len(value_dict['file_links'])
        total_page_size_bytes += value_dict['page_size_bytes']

    longest_path = graph.get_longest_path()
    average_internal_links_per_page = total_internal_links // total_webpages
    average_external_links_per_page = total_external_links // total_webpages
    average_page_size_bytes = total_page_size_bytes // total_webpages

    statistic_info = f'\nGeneral information about                  {root_link}\n'
    statistic_info += f'\nTotal web pages found (unique links):      {total_webpages}\n'

    http_counter = Counter(http_statuses)
    for http_status, count in http_counter.items():
        statistic_info += f'HTTP {http_status}:                                  {count}\n'

    statistic_info += f'\nTotal internal links (non-unique links):   {total_internal_links}\n'
    statistic_info += f'Distance between the most distant pages:   {longest_path}\n\n'

    statistic_info += f'Total external links:                      {total_external_links}\n'
    statistic_info += f'Total dead links:                          {total_dead_links}\n'
    statistic_info += f'Total phone links:                         {total_phone_links}\n'
    statistic_info += f'Total email links:                         {total_email_links}\n'
    statistic_info += f'Total file links:                          {total_file_links}\n\n'
    statistic_info += f'Average number of internal links per page: {average_internal_links_per_page}\n'
    statistic_info += f'Average number of external links per page: {average_external_links_per_page}\n'
    statistic_info += f'Average size (in bytes) per page:          {average_page_size_bytes}\n'

    incoming_links_dict = graph.get_nodes_with_min_max_links()
    minimum_incoming_links = incoming_links_dict['minimum_incoming_links']
    min_links_len = len(minimum_incoming_links["links"])

    maximum_incoming_links = incoming_links_dict['maximum_incoming_links']
    max_links_len = len(maximum_incoming_links["links"])

    statistic_info += f'\n\nMinimum incoming links for {min_links_len} pages:       {minimum_incoming_links["incoming_links_count"]}\n\n'
    for link in incoming_links_dict['minimum_incoming_links']['links']:
        statistic_info += f'>>  HTTP: {webpage_parser.get_link_status_code(link)}   {link}\n'

    statistic_info += f'\nMaximum incoming links for {max_links_len} pages:         {maximum_incoming_links["incoming_links_count"]}\n\n'
    for link in incoming_links_dict['maximum_incoming_links']['links']:
        statistic_info += f'>>  HTTP: {webpage_parser.get_link_status_code(link)}   {link}\n'

    return statistic_info
