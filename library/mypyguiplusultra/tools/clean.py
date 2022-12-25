from pathlib import Path
from .config_constants import BUILT_FILES

def clean(config : dict):
    '''
    Clears all the built files in the project
    NOTE: Use at your own risk
    NOTE: Config must be updated after this function is called
    '''
    for path in config[BUILT_FILES]:
        file = Path(path)
        if file.is_file():file.unlink()

    config[BUILT_FILES].clear()
