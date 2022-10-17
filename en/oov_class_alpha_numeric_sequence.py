from en.primitives import (
    NEMO_ALNUM,
    NEMO_ALPHA,
    NEMO_DIGIT,
    delete_space,
    insert_space,
)
from en.utils import get_abs_path
import pynini
from pynini.lib import pynutil
from en.oov_class_alpha_sequence import  AlphaSequence
from en.oov_class_numeric_sequence import NumericSequence


class AlphaNumericSequence:
    def __init__(self, alpha:AlphaSequence, numeric:NumericSequence):
        self.double_triple_graph = alpha.double_triple_graph|numeric.double_triple_graph

        self.alpha_numeric_graph = (alpha.alpha_graph | numeric.numeric_graph)

        sequence = (self.alpha_numeric_graph + pynini.closure(delete_space + self.alpha_numeric_graph,
                                                         1)) | self.double_triple_graph
        self.fst = sequence
