from app.webpage_parser import WebpageParser, FileManager, DFS
from app.helpers import show_graph


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

    show_graph(parser=webparser, root_link=root)
    stat = webparser.get_webpage_statistics()
    print(stat, end='\n\n')
