from typing import Callable
from app.webpage_parser import WebpageParser
from app.graph import Graph
from app.helpers import get_webpage_statistics


def test_get_webpage_statistics(root_link: str, web_parser_without_root: WebpageParser, build_path: Callable[[], str], initialized_graph: Graph):
    '''
    Validate the webpage statistic values and format.
    '''

    web_parser_without_root.load_map_dict_from_json(
        file_name=build_path('test_map_dict_full'))
    initialized_graph.load_adj_list_graph_from_json(
        file_name=build_path('test_adj_list_graph_full'))
    expected_statistic = '\nGeneral information about                  https://www.globalapptesting.com\n\nTotal web pages found (unique links):      361\nHTTP 200:                                  354\nHTTP 404:                                  7\n\nTotal internal links (non-unique links):   17409\nDistance between the most distant pages:   379\n\nTotal external links:                      5207\nTotal dead links:                          86\nTotal phone links:                         25\nTotal email links:                         183\nTotal file links:                          36\n\nAverage number of internal links per page: 48\nAverage number of external links per page: 14\nAverage size (in bytes) per page:          97343'
    obtained_statistic = get_webpage_statistics(
        root_link=root_link, webpage_parser=web_parser_without_root, graph=initialized_graph)
    assert expected_statistic == obtained_statistic[:689]
