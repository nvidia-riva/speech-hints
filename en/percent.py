from en.decimal import Decimal
from en.primitives import delete_space
import pynini
from pynini.lib import pynutil

class Percent():
    def __init__(self):
        decimal_graph = Decimal().fst
        percent_graph = pynini.invert(pynini.cross("%", pynini.union("percent", "per cent")).optimize())
        self.fst = decimal_graph+pynutil.add_weight(delete_space+percent_graph,-0.0002)
