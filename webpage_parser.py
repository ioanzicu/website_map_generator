import json
from requests import get, head
from bs4 import BeautifulSoup
from httplib2 import Response
from collections import Counter
from collections import deque


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

    def perform_get_request(self, url: str = '') -> Response:
        '''
        Perform HTTP get request and return response object.
        returns a tuple with:
            - webpage text, 
            - HTTP status code, 
            - content length (in bytes)
        '''
        # len(response.content) - size in bytes
        # len(response.text)    - size in characters 

        if not url:
            raise ArgumentNotProvided('url was not provided')
        response: Response = get(url=url)
        
        return (response.text, response.status_code, len(response.content))

    def get_links_from_web_page(self, web_page, parser='html.parser'):
        '''
        Extract all links form given html web page.
        '''

        soup: BeautifulSoup = BeautifulSoup(web_page, parser)
        return soup.find_all('a')

    def extract_hrefs(self, links: list) -> dict:
        '''
        Extract the links from html href attribute and return a dictionary with
        links in the format:

        {'internal_links':  Counter({'https://www.globalapptesting.com/product': 7,
                                     'https://www.globalapptesting.com/platform/integrations': 5}),
         'external_links':  Counter({'https://www.leadingqualitybook.com/': 2,
                                     'https://testathon.co/': 2}),
         'dead_links':      Counter(),
         'phone_links':     Counter(),
         'email_links':     Counter(),
         'image_links':     Counter()}
        '''

        if not isinstance(links, list):
            raise ValueError(
                f'The links type is {type(links)}, expected to be of type list')

        if not links:
            return {'internal_links': Counter(),
                    'external_links': Counter(),
                    'dead_links': Counter(),
                    'phone_links': Counter(),
                    'email_links': Counter(),
                    'image_links': Counter()}

        if not self.root_link:
            raise ValueError(
                f'The root was not provided at the object construction: root_link={self.root_link}')

        internal_links = []
        external_links = []
        dead_links = []
        phone_links = []
        email_links = []
        image_links = []
        for link in links:
            link_host: str = link.get('href')


            if not link_host or link_host.startswith('javascript:;'):
                continue
            elif link_host.endswith('.png'):
                image_links.append(link_host)
            elif link_host.startswith('/'):
                root = self.root_link
                if self.root_link.endswith('/'):
                    root = self.root_link[:-1] 
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
                'email_links':      Counter(email_links),
                'image_links':      Counter(image_links)}

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
                                               'email_links': Counter(),
                                               'image_links': Counter(),
                                               'HTTP_STATUS': 200,
                                               'page_size_bytes': 116577}
        }
        '''
        return self.build_dict_helper_iterative(self.root_link)
    
    def build_dict_helper_recursive(self, link) -> dict:
        '''
        Does the same thing as iterative version but using recurion.
        '''

        # Perform get request
        response, status_code, page_size_bytes = self.perform_get_request(url=link)
        
        # Extract links from html root page
        links = self.get_links_from_web_page(web_page=response)
        # Categorize links
        clean_links = self.extract_hrefs(links=links)
        clean_links.__setitem__('HTTP_STATUS', status_code)
        clean_links.__setitem__('page_size_bytes', page_size_bytes)

        # Extract internal links
        internal_links_only = self.extract_links_from_counter(
            clean_links['internal_links'])

        # Add to the map_dict the first key value
        self.map_dict[link] = clean_links

        # Repeat the above steps for the internal links
        for internal_link in internal_links_only:
            if internal_link not in self.map_dict:
                self.build_dict_helper_recursive(internal_link)

        return self.map_dict

    def build_dict_helper_iterative(self, link) -> dict:
        '''
        The iterative implementation uses a stack to track links that were not queried yet.
        At each iteration a new link (key) is popped from the stack, the links (value) are extracted and added to map_dict
        '''

        stack = deque()
        # Start with the given link
        stack.append(link)

        while stack:
            # pop the top element
            element_link = stack.pop()

            # Perform get request
            response, status_code, page_size_bytes = self.perform_get_request(url=element_link)
            
            # Extract links from html root page
            links = self.get_links_from_web_page(web_page=response)
            # Categorize links
            clean_links = self.extract_hrefs(links=links)
            clean_links.__setitem__('HTTP_STATUS', status_code)
            clean_links.__setitem__('page_size_bytes', page_size_bytes)
            
            self.map_dict[element_link] = clean_links
            
            # Extract internal links
            internal_links_only = self.extract_links_from_counter(
                clean_links['internal_links'])
            
            # Add to the stack links that were not queried yet
            for internal_link in internal_links_only:
                if internal_link not in self.map_dict:
                    stack.append(internal_link)
            
        return self.map_dict

    def convert_counters_to_graph_edges(self) -> dict:
        '''
        Convert Counters objects to graph edges in tuple datatype.
        '''

        if not self.map_dict:
            self.build_dict_map()

        for key_root, value_dict in self.map_dict.items():
            if key_root == 'HTTP_STATUS':
                continue
            self.graph_dict[key_root] = [(key_root, destination_link, weight)
                                         for destination_link, weight in value_dict['internal_links'].items()]
        return self.graph_dict

    def write_to_file(self, file_name: str = 'file', format: str = 'json', data: dict = {}) -> None:
        '''
        Write data to a file.
        '''
        if not data:
            raise ValueError('The data is empty')

        with open(f'{file_name}.{format}', mode='w', encoding="utf8") as fhandle:
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
        with open(f'{file_name}.json', mode='r', encoding="utf8") as fhandle:
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
            image_links    - number of image links
            HTTP_STATUS    - HTTP status code
        '''

        if link not in self.map_dict:
            raise KeyError(f'There was not found key={link} in the map_dict')

        for key in ['internal_links', 'external_links', 'dead_links', 'phone_links', 'email_links']:
            if key not in self.map_dict[link]:
                raise KeyError(
                    f'There was not found key={key} in the map_dict[{link}]')

        return {
            'internal_links': len(self.map_dict[link]['internal_links']),
            'external_links': len(self.map_dict[link]['external_links']),
            'dead_links':  len(self.map_dict[link]['dead_links']),
            'phone_links':  len(self.map_dict[link]['phone_links']),
            'email_links':  len(self.map_dict[link]['email_links']),
            'image_links': len(self.map_dict[link]['image_links']),
            'HTTP_STATUS': self.map_dict[link]['HTTP_STATUS']
        }

    def get_link_info_formatted_string(self, link: str) -> str:
        link_info: dict = self.get_link_info(link)
        return f"<b>{link}</b><br/>HTTP STATUS: <b>{link_info['HTTP_STATUS']}</b><hr/><br/>Internal links: {link_info['internal_links']} <br/>External links: {link_info['external_links']} <br/>Dead links: {link_info['dead_links']} <br/>Phone links: {link_info['phone_links']} <br/>Email links: {link_info['email_links']} <br/>Image links: {link_info['image_links']}"

    def get_link_status_code(self, link: str) -> int:
        if not self.map_dict:
            raise ValueError('The map_dict is empty')

        if link not in self.map_dict:
            raise KeyError(f'There was not found key={link} in the map_dict')

        return self.map_dict[link].get('HTTP_STATUS', 0)

    def get_webpage_statistics(self) -> str:
        if not self.map_dict:
            return 'The map_dict is empty'

        total_webpages = len(self.map_dict.keys())

        total_internal_links = 0
        total_external_links = 0
        total_dead_links = 0
        total_phone_links = 0
        total_email_links = 0
        total_image_links = 0
        total_page_size_bytes = 0
        http_statuses = []
        for key, value in self.map_dict.items():
            if key == 'HTTP_STATUS':
                continue

            http_statuses.append(value['HTTP_STATUS'])

            total_internal_links += len(value['internal_links'])
            total_external_links += len(value['external_links'])
            total_dead_links += len(value['dead_links'])
            total_phone_links += len(value['phone_links'])
            total_email_links += len(value['email_links'])
            total_image_links += len(value['image_links'])
            total_page_size_bytes += value['page_size_bytes']

        average_internal_links_per_page = total_internal_links // total_webpages
        average_external_links_per_page = total_external_links // total_webpages
        average_page_size_bytes = total_page_size_bytes // total_webpages

        statistic_info = f'\nGeneral information about                  {self.root_link}\n'
        statistic_info += f'\nTotal web pages found:                     {total_webpages}\n'

        http_counter = Counter(http_statuses)
        for http_status, count in http_counter.items():
            statistic_info += f'HTTP {http_status}:                                  {count}\n'

        statistic_info += f'\nTotal internal links:                      {total_internal_links}\n'
        statistic_info += f'Total external links:                      {total_external_links}\n'
        statistic_info += f'Total dead links:                          {total_dead_links}\n'
        statistic_info += f'Total phone links:                         {total_phone_links}\n'
        statistic_info += f'Total email links:                         {total_email_links}\n'
        statistic_info += f'Total image links:                         {total_image_links}\n\n'
        statistic_info += f'Average number of internal links per page: {average_internal_links_per_page}\n'
        statistic_info += f'Average number of external links per page: {average_external_links_per_page}\n'
        statistic_info += f'Average size (in bytes) of page:           {average_page_size_bytes}\n'
        

        return statistic_info

    def generate_and_save_graph(self) -> dict:
        self.build_dict_map()
        graph = self.convert_counters_to_graph_edges()

        self.write_graph_dict_to_json_file()
        self.write_map_dict_to_json_file()
        return graph