The motivation for this project is the [**Python engineer test**](https://gitlab.com/GlobalAppTesting/public-recruitment-tests/gat-senior-python-engineer-dev-task)


# Requirements

- Windows, Mac or Linux Operating System
- Python version 3.9.7
- pip version 22.0.3


## Install packages
- ```pip install -r requirements.txt```

## Run the script
- `python main.py`
    
or 
- `python main.py > logs.txt`

to store the terminal output in logs.txt file



## Run unit test
Without output in the terminal
- `python -m pytest`

Witht output in the terminal, verbose flags: `-v` (short logs)  or `-vv` (full logs)

- `python -m pytest -vv`