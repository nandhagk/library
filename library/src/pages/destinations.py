# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

from enum import Enum, auto

class Destinations(Enum):
    home = auto()
    browse = auto()
    search = auto()
    add = auto()
    edit = auto()
    loanInfo = auto()
    bookInfo = auto()
    personInfo = auto()
