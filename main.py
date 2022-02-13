import json
import pprint
import sys
from requests import get
from bs4 import BeautifulSoup
from httplib2 import Response
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network


pp = pprint.PrettyPrinter(depth=4, indent=2)


class ArgumentNotProvided(ValueError):
    pass


class WebpageParser():
    def __init__(self, root_link: str) -> None:

        if not isinstance(root_link, str):
            raise ValueError(
                f'root_link is of type {root_link}, expected to be str')

        self.root_link: str = root_link
        self.root_domain: str = root_link.split(
            '.')[1] if self.root_link else ''
        self.map_dict: dict = {}
        self.graph_dict: dict = {}

    def __str__(self) -> str:
        return f'WebpageParser(root_link={self.root_link})'

    def get_map_dict(self) -> dict:
        return self.map_dict

    def get_graph_dict(self) -> dict:
        return self.graph_dict

    def perform_get_request(self, url: str = ''):
        '''
        Perform HTTP get request and return response object.
        '''

        if not url:
            raise ArgumentNotProvided('url was not provided')
        response: Response = get(url=url)

        if response.status_code != 200:
            # @TODO Fix bug when code is not 200
            return ''
            # raise Exception(f'Status code is not 200: {response.status_code}')
        return response.text

    def get_links_from_web_page(self, web_page, parser='html.parser'):
        '''
        Extract all links form given html web page.
        '''

        soup: BeautifulSoup = BeautifulSoup(web_page, parser)
        return soup.find_all('a')

    def extract_hrefs(self, links: list, root: str = '') -> dict:
        '''
        Extract the links from html href attribute and return a dictionary with
        links in the format:

        {'internal_links':   Counter({'https://www.globalapptesting.com/product': 7,
                                      'https://www.globalapptesting.com/platform/integrations': 5}),
         'external_links':   Counter({'https://www.leadingqualitybook.com/': 2,
                                     'https://testathon.co/': 2}),
         'dead_links':       Counter(),
         'phone_links':      Counter(),
         'email_links':      Counter()}
        '''

        if not isinstance(links, list):
            raise ValueError(
                f'The links type is {type(links)}, expected to be of type list')

        if not links:
            return {'internal_links': Counter(), 'external_links': Counter(), 'dead_links': Counter(), 'phone_links': Counter(), 'email_links': Counter()}

        if not root:
            raise ValueError(
                f'The root was not provided: links={links}, root={root}')

        internal_links = []
        external_links = []
        dead_links = []
        phone_links = []
        email_links = []
        for link in links:
            link_host: str = link.get('href')

            if not link_host or link_host.startswith('javascript:;'):
                continue
            elif link_host.startswith('/'):
                if root.endswith('/'):
                    root = root[:-1]
                complete_link = root + link_host
                internal_links.append(complete_link)
            elif link_host == '#':
                dead_links.append(link_host)
            elif 'tel' in link_host:
                phone_links.append(link_host)
            elif 'mailto' in link_host:
                email_links.append(link_host)
            # check only if the hosts are the same
            elif len(link_host.split('.')) > 1 and link_host.startswith('https://www') and self.root_domain in link_host.split('.')[1]:
                internal_links.append(link_host)
            else:
                external_links.append(link_host)

        return {'internal_links':   Counter(internal_links),
                'external_links':   Counter(external_links),
                'dead_links':       Counter(dead_links),
                'phone_links':      Counter(phone_links),
                'email_links':      Counter(email_links)}

    def extract_links_from_counter(self, counter_obj: Counter) -> list:
        '''
        Extract links from the given Counter object in format:

        Counter({'https://www.globalapptesting.com/product': 7,
                 'https://www.globalapptesting.com/platform/integrations': 5})

        and return a list of links like:

        ['https://www.globalapptesting.com/product',
            'https://www.globalapptesting.com/platform/integrations']
        '''

        if not isinstance(counter_obj, Counter):
            raise ValueError(
                f'Argument obj is of type {type(counter_obj)}, expected obj to be of type Counter')
        return [link for link, _ in counter_obj.items()]

    def build_dict_map(self) -> dict:
        '''
        Crawl links from webpages and build dictionary map from the obtained links.

        Example of returned dict:
        {'https://www.globalapptesting.com/': {'internal_links': Counter({'https://www.globalapptesting.com/product': 7,
                                                                          'https://www.globalapptesting.com/platform/integrations': 5,
                                                                          'https://www.globalapptesting.com/resources/resource-library': 4,
                                                                          'https://www.globalapptesting.com/about-us': 4}),
                                               'external_links': Counter({'https://www.leadingqualitybook.com/': 2,
                                                                          'https://testathon.co/': 2,
                                                                          'https://www.facebook.com/globalapptesting/': 1}),
                                               'dead_links': Counter(),
                                               'phone_links': Counter(),
                                               'email_links': Counter()}
         }
        '''
        # @TODO REFACTOR

        # Perform get request
        response = self.perform_get_request(url=self.root_link)
        # Extract links from html root page
        links = self.get_links_from_web_page(web_page=response)
        # Categorize links
        clean_links = self.extract_hrefs(links=links, root=self.root_link)
        # Extract internal links
        only_internal_links = self.extract_links_from_counter(
            clean_links['internal_links'])

        # Add to the map_dict the first key value
        self.map_dict = {self.root_link: clean_links}

        # Repeat the above steps for the internal links
        for internal_link in only_internal_links:
            response = self.perform_get_request(url=internal_link)
            page_links = self.get_links_from_web_page(web_page=response)
            counter_links = self.extract_hrefs(
                links=page_links, root=internal_link)
            self.map_dict[internal_link] = counter_links

            # add the non-existing nodes from the counter links
            counter_internal_links = self.extract_links_from_counter(
                counter_links['internal_links'])
            for destination_link in counter_internal_links:
                if destination_link not in self.map_dict:
                    dest_response = self.perform_get_request(
                        url=destination_link)
                    page_links = self.get_links_from_web_page(
                        web_page=dest_response)
                    dest_counter_links = self.extract_hrefs(
                        links=page_links, root=destination_link)

                    self.map_dict[destination_link] = dest_counter_links

        return self.map_dict

    def convert_counters_to_graph_edges(self) -> dict:
        '''
        Convert Counters objects to graph edges in tuple datatype.
        '''

        if not self.map_dict:
            self.build_dict_map()

        for key_root, value_dict in self.map_dict.items():
            self.graph_dict[key_root] = [(key_root, destination_link, weight)
                                         for destination_link, weight in value_dict['internal_links'].items()]
        return self.graph_dict

    def write_to_file(self, file_name: str = 'file', format: str = 'json', data: dict = {}) -> None:
        '''
        Write data to a file.
        '''
        if not data:
            raise ValueError('The data is empty')

        with open(f'{file_name}.{format}', 'w') as fhandle:
            try:
                json.dump(data, fhandle, indent=4)
            except Exception as exc:
                print(
                    f'Exception occured when trying to write to json file with name={file_name}.{format}: {exc}')

    def write_map_dict_to_json_file(self, file_name: str = 'map_dict') -> None:
        '''
        Write / Dump the map dict into json file.
        '''

        if not self.map_dict:
            raise ValueError('The map_dict is empty')
        self.write_to_file(file_name=file_name, data=self.map_dict)

    def write_graph_dict_to_json_file(self, file_name: str = 'graph_dict') -> None:
        '''
        Write / Dump the graph dict into json file.
        '''

        if not self.graph_dict:
            raise ValueError('The graph_dict is empty')
        self.write_to_file(file_name=file_name, data=self.graph_dict)

    def load_from_json(self, file_name: str) -> dict:
        '''
        Load the dictionary from a json file.
        '''
        with open(f'{file_name}.json', 'r') as fhandle:
            try:
                return json.loads(fhandle.read())
            except Exception as exc:
                print(
                    f'Exception occured when trying to read from the json file with name={file_name}: {exc}')

        return self.graph_dict

    def load_map_dict_from_json(self, file_name: str) -> dict:
        '''
        Load the map dictionary from a json file.
        '''
        self.map_dict = self.load_from_json(file_name=file_name)
        return self.map_dict

    def load_graph_dict_from_json(self, file_name: str) -> dict:
        '''
        Load the graph dictionary from a json file.
        '''
        self.graph_dict = self.load_from_json(file_name=file_name)
        return self.graph_dict

    def get_link_info(self, link: str) -> dict:
        '''
        Return information about link like: 
            internal_links - number of internal links
            external_links - number of external links
            dead_links     - number of dead links
            phone_links    - number of phone links
            email_links    - number of email links
        '''

        if not link in self.map_dict:
            raise KeyError(f'There was not found key={link} in the map_dict')

        for key in ['internal_links', 'external_links', 'dead_links', 'phone_links', 'email_links']:
            if not key in self.map_dict[link]:
                raise KeyError(
                    f'There was not found key={key} in the map_dict[{link}]')

        return {
            'internal_links': len(self.map_dict[link]['internal_links']),
            'external_links': len(self.map_dict[link]['external_links']),
            'dead_links':  len(self.map_dict[link]['dead_links']),
            'phone_links':  len(self.map_dict[link]['phone_links']),
            'email_links':  len(self.map_dict[link]['email_links']),
        }

    def get_link_info_formatted_string(self, link: str) -> str:
        link_info: dict = self.get_link_info(link)
        # return f"<b>{link}</b>\n\nInternal links: {link_info['internal_links']} <br/>External links: {link_info['external_links']}\nDead links: {link_info['dead_links']}\nPhone links: {link_info['phone_links']}\nEmail links: {link_info['email_links']}"
        return f"<b>{link}</b><hr/><br/>Internal links: {link_info['internal_links']} <br/>External links: {link_info['external_links']} <br/>Dead links: {link_info['dead_links']} <br/>Phone links: {link_info['phone_links']} <br/>Email links: {link_info['email_links']}"


if __name__ == '__main__':

    local_data = True

    root: str = 'https://www.globalapptesting.com/'
    webparser = WebpageParser(root_link=root)

    if not local_data:
        # Geather data from the internet
        response = webparser.perform_get_request(url=root)
        links = webparser.get_links_from_web_page(web_page=response)
        hrefs = webparser.extract_hrefs(links=links, root=root)
        map_dict = webparser.build_dict_map()
        graph_dict = webparser.convert_counters_to_graph_edges()

        webparser.write_graph_dict_to_json_file()
        webparser.write_map_dict_to_json_file()

    else:
        # Load data from local files
        graph_dict = webparser.load_graph_dict_from_json('graph_dict')
        webparser.load_map_dict_from_json('map_dict')

    # VISUALISATION
    plt.rcParams.update({'font.size': 5})
    G = nx.Graph()
    nt = Network(height='1000px', width='100%', directed=True)
    nx_graph = nx.Graph()
    nx_graph.add_node(root)
    for key_root, value_edges in graph_dict.items():
        edges_len = len(value_edges) if len(value_edges) > 20 else 20
        nx_graph.add_node(key_root, label=key_root, width=20,
                          title=f'{webparser.get_link_info_formatted_string(key_root)}',  size=0.9 * edges_len, group=key_root)

        nx_graph.add_weighted_edges_from([(src, dest, weight*5)
                                          for (src, dest, weight) in value_edges], arrowStrikethrough=True)

    nx.draw_shell(G, with_labels=False, font_size=4, font_weight='bold')
    nt.from_nx(nx_graph)
    nt.show_buttons(filter_=['nodes', 'edges', 'physics'])
    nt.barnes_hut(gravity=-200000, central_gravity=0, spring_length=400,
                  spring_strength=0.001, damping=0.49, overlap=0)
    nt.show(f'{root.split(".")[1]}_map.html')
