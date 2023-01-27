from en.primitives import (
    NEMO_ALNUM,
    NEMO_ALPHA,
    NEMO_DIGIT,
    delete_space,
    insert_space,
    delete_one_space,
    NEMO_WHITE_SPACE,
)
from en.utils import get_abs_path
import pynini
from pynini.lib import pynutil
from en.oov_class_alpha_sequence import AlphaSequence
from en.oov_class_numeric_sequence import NumericSequence


class AlphaNumericSequence:
    def __init__(self, alpha: AlphaSequence, numeric: NumericSequence):
        self.double_triple_graph = (
            alpha.double_triple_graph | numeric.double_triple_graph
        )

        self.alpha_numeric_graph = alpha.fst | numeric.numeric_graph | delete_one_space
        character = numeric.numeric_graph | NEMO_ALPHA
        sequence = (
            NEMO_WHITE_SPACE
            + character
            + pynini.closure(pynutil.delete(" ") + character, 2)
            + NEMO_WHITE_SPACE
        )
        sequence = sequence @ (
            NEMO_WHITE_SPACE
            + pynini.closure(NEMO_ALNUM)
            + NEMO_DIGIT
            + pynini.closure(NEMO_ALNUM)
            + NEMO_WHITE_SPACE
        )
        self.fst = sequence
