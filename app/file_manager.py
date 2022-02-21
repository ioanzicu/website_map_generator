import json


class FileManager():
    def __init__(self) -> None:
        pass

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
