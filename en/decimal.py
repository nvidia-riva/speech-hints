from nemo_text_processing.inverse_text_normalization.en.taggers.cardinal import CardinalFst
from en.primitives import str_to_digit, delete_space, zero_to_digit
import pynini
from pynini.lib import pynutil


class Decimal():
    def __init__(self):
        integer_graph = CardinalFst().graph
        point = delete_space + pynini.cross("point", ".")
        decimals_graph = point + pynini.closure(pynutil.add_weight(delete_space + str_to_digit, -0.0001))
        self.fst = pynutil.add_weight(integer_graph, -0.0001) \
                   | ((pynutil.add_weight(integer_graph, -0.0002)| pynutil.add_weight(str_to_digit, 1.0))
                      + pynutil.add_weight(decimals_graph, -0.0003)
                      )
