import json
from typing import Callable
from app.webpage_parser import FileManager


def test_load_from_json(file_manager: FileManager, build_path: Callable[[], str], expected_json_sample: json, write_to_json_file: Callable[[str, ], None]):
    '''
    Test the correct loading of dictionary from json.
    '''

    file_name = 'test_load'
    write_to_json_file(file_name, expected_json_sample)
    obtained_json = file_manager.load_from_json(
        file_name=build_path(file_name))
    assert expected_json_sample == obtained_json


def test_write_to_file(file_manager: FileManager, build_path: Callable[[], str], small_map_sample: dict):
    '''
    Test the writing dict object to the json file.
    '''

    file_name = 'test_file'
    file_path = build_path(file_name)
    file_manager.write_to_file(data=small_map_sample,
                               file_name=file_path)

    with open(file=build_path(file_name, 'json'), mode='r', encoding='utf8') as fhandle:
        try:
            obtained_json = json.load(fhandle)
            assert small_map_sample == obtained_json
        except Exception as exc:
            print(
                f'Exception occured when trying to read from the json file with name={file_name}: {exc}')
