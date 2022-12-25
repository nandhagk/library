from pathlib import Path
from mypyguiplusultra.pyx.transpiler import transpilePyx
from .config_constants import SRC_DIRECTORY, BUILT_FILES

def buildFile(file_path : Path) -> Path:
    '''Builds the .py file for a specific .pyx file'''
    out_file = file_path.parent.joinpath(file_path.name.removesuffix(file_path.suffix) + '.py')
    out_file.write_text(transpilePyx(file_path.read_text()))
    return out_file

def build(config : dict):
    '''
    Creates corresping .py files for all .pyx files in the project
    NOTE: Config must be updated after this function is called
    '''
    src_dir = Path(config[SRC_DIRECTORY])
    for file in src_dir.glob("**/*.pyx"):
        out_file = buildFile(file)
        config[BUILT_FILES].append(out_file.as_posix())
