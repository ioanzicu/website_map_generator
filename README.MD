The motivation for this project is the [**Python engineer test**](https://gitlab.com/GlobalAppTesting/public-recruitment-tests/gat-senior-python-engineer-dev-task)


# Requirements

- Operating System: Windows 10, MacOS or Linux
- Python version 3.9.7
- pip version 22.0.3


## Install packages
- ```pip install -r requirements.txt```

## Run the script
- `python main.py`
    
or 
- `python main.py > logs.txt`

to store the terminal output in logs.txt file

In the main.py file you can choose to:
- change the `root` link - website that you want to build a graph from 
- `local_data` if is `True` it  will load the data from json files (make sure you have them)
               if is `False` the script will crawl the website from `root` variable and create the json files with obtained data so it can be rerun again (if you need to) from local data which is faster.

After the script execution is finished, the `.html` file will be generated with the graph representation of the obtained data. The browser automaticaly should open this file (Chrome browser, or other which is in your system set as default).
The graph visualisation is interactive, the user can get more information about each node by howering the mouse over it.
If you scroll down, there is a panel with configuration buttons for nodes, edges and physics.

![Example of generated graph](/graph_representation.png)

Above you vcan see an example of generated graph.

Also you can check out the globalapptesting_map.html.

## Run unit test
Without output in the terminal
- `python -m pytest`

Witht output in the terminal, verbose flags: `-v` (short logs)  or `-vv` (full logs)

- `python -m pytest -vv`


This code is not meant to be used in production (for commercial purpose). The author Ioan Zicu, does not allow it!