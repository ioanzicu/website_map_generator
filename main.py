from webpage_parser import WebpageParser
from helpers import show_graph


if __name__ == '__main__':

    local_data = False

    root: str = 'https://www.globalapptesting.com'
    webparser = WebpageParser(root_link=root)

    if not local_data:
        # Geather data from the internet
        response, status_code = webparser.perform_get_request(url=root)
        links = webparser.get_links_from_web_page(web_page=response)
        hrefs = webparser.extract_hrefs(links=links)
        map_dict = webparser.build_dict_map()
        graph_dict = webparser.convert_counters_to_graph_edges()

        webparser.write_graph_dict_to_json_file()
        webparser.write_map_dict_to_json_file()

    else:
        # Load data from local files
        graph_dict = webparser.load_graph_dict_from_json('graph_dict')
        webparser.load_map_dict_from_json('map_dict')

    show_graph(graph_dict=graph_dict, root_link=root, parser=webparser)
    stat = webparser.get_webpage_statistics()
    print(stat, end='\n\n')
