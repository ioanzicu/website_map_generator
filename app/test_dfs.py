from app.webpage_parser import DFS


def test_get_longest_path(dfs: DFS, temp_graph_dict_full: dict):
    '''
    Check if the value of method get_lingest_path is equal to expected one.
    '''
    dfs = dfs(temp_graph_dict_full)
    obtained_longest_path = dfs.get_longest_path()
    expected_longest_path = 379
    assert expected_longest_path == obtained_longest_path
