import pytest
import json
from typing import Callable, Counter
from app.webpage_parser import WebpageParser, ArgumentNotProvided


def test_get_links_from_web_page_no_url(web_parser: WebpageParser):
    '''
    Test ArgumentNotProvided exception.
    '''

    with pytest.raises(ArgumentNotProvided):
        web_parser.perform_get_request()


def test_get_links_from_web_page(web_parser: WebpageParser, build_path: Callable[[], str]):
    '''
    Test if the obtained links are correct - with minimal attempts.
    '''

    link_10 = '<a aria-expanded="false" aria-haspopup="true" data-hs-event-102002560="1" data-hs-event-190178346="1" data-hs-event-205950610="1" data-hs-event-43945764="1" href="https://www.globalapptesting.com/solutions" role="menuitem">Solutions</a>'
    last_link = '<a href="https://go.globalapptesting.com/speak-to-us" role="menuitem">Speak to Us</a>'
    links_len = 167

    file_path = build_path('global_test_app', 'html')
    with open(file=file_path, mode='r', encoding='utf8') as fhandle:
        links = web_parser.get_links_from_web_page(fhandle)

        assert str(links[10]) == link_10
        assert str(links[-1]) == last_link
        assert len(links) == links_len


def test_extract_hrefs_invalid_type_for_links(web_parser: WebpageParser):
    '''
    Test the exception when invalid data types for links are provided.
    '''

    with pytest.raises(ValueError):
        web_parser.extract_hrefs(links=1)


def test_extract_hrefs_empty_links_list(web_parser: WebpageParser):
    '''
    Test when the links list is empty - returns an dict with empty Counter objects.
    '''

    hrefs = web_parser.extract_hrefs(links=[])

    assert 'internal_links' in hrefs
    assert 'external_links' in hrefs
    assert 'dead_links' in hrefs
    assert 'phone_links' in hrefs
    assert 'email_links' in hrefs

    assert not hrefs['internal_links']
    assert not hrefs['external_links']
    assert not hrefs['dead_links']
    assert not hrefs['phone_links']
    assert not hrefs['email_links']


def test_extract_hrefs(web_parser: WebpageParser, build_path: Callable[[], str]):
    '''
    Test the correct extraction of hrefs.
    '''

    internal_href_key = 'https://www.globalapptesting.com/product'
    external_href_key = 'https://www.leadingqualitybook.com/'

    file_path = build_path('global_test_app', 'html')
    with open(file=file_path, mode='r', encoding='utf8') as fhandle:
        links = web_parser.get_links_from_web_page(fhandle)
        hrefs = web_parser.extract_hrefs(links=links)

        assert 'internal_links' in hrefs
        assert 'external_links' in hrefs
        assert 'dead_links' in hrefs
        assert 'phone_links' in hrefs
        assert 'email_links' in hrefs

        assert hrefs['internal_links'].get(internal_href_key, 0) == 9
        assert hrefs['external_links'].get(external_href_key, 0) == 3
        assert not hrefs['dead_links']
        assert not hrefs['phone_links']
        assert not hrefs['email_links']


def test_extract_links_from_counter_invalid_obj_type(web_parser: WebpageParser):
    '''
    Test the exceptin when the argument counter_obj is not of type Counter.
    '''

    with pytest.raises(ValueError):
        web_parser.extract_links_from_counter(counter_obj=[])


def test_extract_links_from_counter_empty_object(web_parser: WebpageParser):
    '''
    Test the exceptin when the argument counter_obj is empty - returns an empty list.
    '''

    links = web_parser.extract_links_from_counter(counter_obj=Counter())
    assert not links


def test_extract_links_from_counter(web_parser: WebpageParser, build_path: Callable[[], str]):
    '''
    Test the correct extraction of links from the Counter object.
    '''

    file_path = build_path('global_test_app', 'html')
    with open(file=file_path, mode='r', encoding='utf8') as fhandle:
        links = web_parser.get_links_from_web_page(fhandle)
        hrefs = web_parser.extract_hrefs(links=links)
        local_links_extraction = [
            link for (link, _) in hrefs['internal_links'].items()]

        extracted_internal_links = web_parser.extract_links_from_counter(
            hrefs['internal_links'])
        assert extracted_internal_links == local_links_extraction


'''
This test is commented because the current
implementation will query the real website
and it takes too much time to finish.
'''
# def test_build_dict_map(web_parser: WebpageParser):
#     '''
#     Test the correct generation of dict map.
#     '''

#     actual_obj_map = web_parser.build_dict_map()

#     response = web_parser.perform_get_request(url=root_link)
#     links = web_parser.get_links_from_web_page(web_page=response)
#     hrefs = web_parser.extract_hrefs(links=links, root=root_link)
#     extracted_internal_links = web_parser.extract_links_from_counter(
#         hrefs['internal_links'])

#     expected_map = {root_link: hrefs}
#     for url in extracted_internal_links:
#         response = web_parser.perform_get_request(url=root_link)
#         page_links = web_parser.get_links_from_web_page(web_page=response)
#         counter_links = web_parser.extract_hrefs(links=page_links, root=url)
#         expected_map[url] = counter_links

#     assert type(expected_map) == type(actual_obj_map)
#     for (key_map, value_map), (key_obj_map, value_obj_map) in zip(expected_map[root_link].items(), actual_obj_map[root_link].items()):
#         assert key_map == key_obj_map
#         assert value_map == value_obj_map


def test_convert_counters_to_graph_edges_tuples(web_parser_without_root: WebpageParser, temp_map_dict: dict, graph_edges: list):
    '''
    Test convertion of Counter objects into tuples that represent the edges of a graph.

    '''

    web_parser_without_root.map_dict = temp_map_dict
    obtained_graph_dict = web_parser_without_root.convert_counters_to_graph_edges()

    for expected_tuple, obtained_tuple in zip(graph_edges, obtained_graph_dict['https://www.globalapptesting.com/']):
        # the expected tuples contain \n added by vscode beacause of auto formating, for this reason the comparision is done by elements
        for exp_element, obt_element in zip(expected_tuple, obtained_tuple):
            assert exp_element == obt_element


def test_write_map_dict_to_json_file(web_parser_without_root: WebpageParser, build_path: Callable[[], str], small_map_sample: dict):
    '''
    Test the writing map_dict object to the json file.
    '''

    web_parser_without_root.map_dict = small_map_sample
    file_name = 'test_map_dict'
    file_path = build_path(file_name)
    web_parser_without_root.write_map_dict_to_json_file(file_name=file_path)
    with open(file=build_path(file_name, 'json'), mode='r', encoding='utf8') as fhandle:
        try:
            obtained_json = json.load(fhandle)
            assert small_map_sample == obtained_json
        except Exception as exc:
            print(
                f'Exception occured when trying to read from the json file with name={file_name}: {exc}')


def test_write_graph_dict_to_json_file(web_parser_without_root: WebpageParser, expected_json, build_path: Callable[[], str], temp_graph_dict: dict):
    '''
    Test the writing graph_dict object to the json file.
    '''

    web_parser_without_root.graph_dict = temp_graph_dict
    web_parser_without_root.write_graph_dict_to_json_file(
        file_name=build_path('test_graph_dict'))

    file_name = 'test_graph_dict'
    file_path = build_path(file_name, 'json')
    with open(file=file_path, mode='r', encoding='utf8') as fhandle:
        try:
            obtained_json = json.load(fhandle)
            assert expected_json == obtained_json
        except Exception as exc:
            print(
                f'Exception occured when trying to read from the json file with name={file_name}: {exc}')


def test_load_map_dict_from_json(web_parser_without_root: WebpageParser, build_path: Callable[[], str], expected_json_sample: json, write_to_json_file: Callable[[str, ], None]):
    '''
    Test the correct loading of the map dictionary from json.
    '''

    file_name = 'test_load_map_dict'
    write_to_json_file(file_name, expected_json_sample)
    obtained_json = web_parser_without_root.load_map_dict_from_json(
        file_name=build_path(file_name))
    assert expected_json_sample == obtained_json


def test_load_graph_dict_from_json(web_parser_without_root: WebpageParser, build_path: Callable[[], str], expected_json_sample: json, write_to_json_file: Callable[[str, ], None]):
    '''
    Test the correct loading of the graph dictionary from json.
    '''

    file_name = 'test_load_graph_dict'
    write_to_json_file(file_name, expected_json_sample)
    obtained_json = web_parser_without_root.load_graph_dict_from_json(
        file_name=build_path(file_name))
    assert expected_json_sample == obtained_json


def test_get_link_info(web_parser_without_root: WebpageParser,  temp_map_dict: dict):
    '''
    Test statistic info of a given link.
    '''

    web_parser_without_root.map_dict = temp_map_dict
    expected_dict = {'internal_links': 5,
                     'external_links': 6,
                     'dead_links': 0,
                     'phone_links': 0,
                     'email_links': 0,
                     'file_links': 0,
                     'HTTP_STATUS': 200}
    obtained_dict = web_parser_without_root.get_link_info(
        'https://www.globalapptesting.com/')

    assert expected_dict == obtained_dict


def test_get_webpage_statistics(web_parser_without_root: WebpageParser, build_path: Callable[[], str]):
    '''
    Validate the webpage statistic values and format.
    '''

    web_parser_without_root.load_map_dict_from_json(
        file_name=build_path('test_map_dict_full'))
    web_parser_without_root.load_graph_dict_from_json(
        file_name=build_path('test_graph_dict_full'))
    expected_statistic = '\nGeneral information about                  \n\nTotal web pages found (unique links):      361\nHTTP 200:                                  354\nHTTP 404:                                  7\n\nTotal internal links (non-unique links):   17409\nDistance between the most distant pages:   379\n\nTotal external links:                      5207\nTotal dead links:                          86\nTotal phone links:                         25\nTotal email links:                         183\nTotal file links:                          36\n\nAverage number of internal links per page: 48\nAverage number of external links per page: 14\nAverage size (in bytes) per page:          97343'
    obtained_statistic = web_parser_without_root.get_webpage_statistics()
    assert expected_statistic == obtained_statistic[:657]


def test_get_link_status_code(web_parser_without_root: WebpageParser,  temp_map_dict: dict):
    '''
    Check if the returned HTTP status code is correct.
    '''

    web_parser_without_root.map_dict = temp_map_dict
    obtained_status_code = web_parser_without_root.get_link_status_code(
        'https://www.globalapptesting.com/')
    assert 200 == obtained_status_code


def test_get_pages_with_min_max_links(web_parser_without_root: WebpageParser, temp_graph_dict_full: dict):
    '''
    Validate integrity of returned dictionary.
    '''

    web_parser_without_root.graph_dict = temp_graph_dict_full
    obtained_dict = web_parser_without_root.get_pages_with_min_max_links()

    assert 'maximum_incoming_links' in obtained_dict
    assert 'minimum_incoming_links' in obtained_dict
    assert obtained_dict['maximum_incoming_links']['incoming_links_count'] == 361
    assert obtained_dict['minimum_incoming_links']['incoming_links_count'] == 1
    assert len(obtained_dict['maximum_incoming_links']
               ['links']) == 3
    assert len(obtained_dict['minimum_incoming_links']
               ['links']) == 48


def test_count_incoming_links(web_parser_without_root: WebpageParser, temp_graph_dict_full: dict, expected_incoming_count_links: dict):
    '''
    Validate integrity of returned dictionary.
    '''

    web_parser_without_root.graph_dict = temp_graph_dict_full
    obtained_incoming_links_counter = web_parser_without_root.count_incoming_links()
    assert expected_incoming_count_links == obtained_incoming_links_counter
