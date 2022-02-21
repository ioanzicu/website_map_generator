import json
from app.file_manager import FileManager
from app.graph import Graph
from typing import Callable


def test_get_longest_path(initialized_graph: Graph, temp_adj_list_graph_full: dict, file_manager: FileManager):
    '''
    Check if the value of method get_longest_path is equal to expected one.
    '''

    obtained_longest_path = initialized_graph.get_longest_path()
    print(obtained_longest_path)
    expected_longest_path = 379
    assert expected_longest_path == obtained_longest_path


def test_write_adj_list_graph_to_json_file(non_initialized_graph: Graph, expected_json, build_path: Callable[[], str], temp_adj_list_graph: dict, file_manager: FileManager):
    '''
    Test the writing adj_list_graph object to the json file.
    '''

    graph: Graph = non_initialized_graph(
        adj_list_graph=temp_adj_list_graph, file_manager=file_manager)

    graph.write_adj_list_graph_to_json_file(
        file_name=build_path('test_adj_list_graph'))

    file_name = 'test_adj_list_graph'
    file_path = build_path(file_name, 'json')
    with open(file=file_path, mode='r', encoding='utf8') as fhandle:
        try:
            obtained_json = json.load(fhandle)
            assert expected_json == obtained_json
        except Exception as exc:
            print(
                f'Exception occured when trying to read from the json file with name={file_name}: {exc}')


def test_load_adj_list_graph_from_json(initialized_graph: Graph, expected_json_sample, build_path: Callable[[], str], temp_adj_list_graph: dict, write_to_json_file: Callable[[str, ], None], file_manager: FileManager):
    '''
    Test the correct loading of the adj_list_graph dictionary from json.
    '''

    file_name = 'test_load_adj_list_graph'
    write_to_json_file(file_name, expected_json_sample)
    obtained_json = initialized_graph.load_adj_list_graph_from_json(
        file_name=build_path(file_name))
    assert expected_json_sample == obtained_json


def test_count_incoming_edges(initialized_graph: Graph, temp_adj_list_graph_full: dict, expected_incoming_count_links: dict):
    '''
    Validate integrity of returned dictionary.
    '''

    obtained_incoming_links_counter = initialized_graph.count_incoming_edges()
    assert expected_incoming_count_links == obtained_incoming_links_counter


def test_get_nodes_with_min_max_links(initialized_graph: Graph):
    '''
    Validate integrity of returned dictionary.
    '''

    obtained_dict = initialized_graph.get_nodes_with_min_max_links()

    assert 'maximum_incoming_links' in obtained_dict
    assert 'minimum_incoming_links' in obtained_dict
    assert obtained_dict['maximum_incoming_links']['incoming_links_count'] == 361
    assert obtained_dict['minimum_incoming_links']['incoming_links_count'] == 1
    assert len(obtained_dict['maximum_incoming_links']
               ['links']) == 3
    assert len(obtained_dict['minimum_incoming_links']
               ['links']) == 48
