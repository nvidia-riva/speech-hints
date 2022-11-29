import pynini
from pynini.lib import pynutil

from en.ordinal import Ordinal
from en.primitives import NEMO_WHITE_SPACE

class Day:
    def __init__(self):
        ordinal_fst = Ordinal().fst
        graph = pynutil.delete(pynini.closure("the" + NEMO_WHITE_SPACE, 0, 1)) + ordinal_fst
        self.fst = graph.optimize()
