import pynini
from pynini.lib import pynutil
from en.utils import get_abs_path

class Month:
    def __init__(self):
        month_graph = pynini.string_file(get_abs_path("data/months.tsv"))
        self.fst = month_graph
