from en.primitives import (
    NEMO_ALNUM,
    NEMO_ALPHA,
    NEMO_DIGIT,
    NEMO_SPACE,
    delete_space,
    insert_space,
    str_to_digit,
    digit_to_str
)
import pynini

from pynini.lib import pynutil



class PassThrough:
    def __init__(self):
        self.word_fst = pynini.closure(NEMO_ALPHA)
        self.sent_fst = pynini.closure(NEMO_SPACE|self.word_fst)

    def passthrough_fst(self, fst):
        return pynini.closure(NEMO_SPACE|self.word_fst|fst)

