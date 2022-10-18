from en.primitives import (
    NEMO_ALNUM,
    NEMO_ALPHA,
    NEMO_DIGIT,
    delete_space,
    insert_space,
)
import pynini
from pynini.lib import pynutil
class AlphaSequence:
    def __init__(self):
        character = NEMO_ALPHA

        double_char = pynini.union(
            *[
                pynini.cross(
                    pynini.project(chr(i), "output")
                    + pynini.accep(" ")
                    + pynini.project(chr(i), "output"),
                    pynutil.insert("double ") + pynini.project(chr(i), "output"),
                )
                for i in range(97, 123)
            ]
        ).invert()
        triple_char = pynini.union(
            *[
                pynini.cross(
                    pynini.project(chr(i), "output")
                    + pynini.accep(" ")
                    + pynini.project(chr(i), "output")
                    + pynini.accep(" ")
                    + pynini.project(chr(i), "output"),
                    pynutil.insert("triple ") + pynini.project(chr(i), "output"),
                )
                for i in range(97, 123)
            ]
        ).invert()

        double_char_to_char = (
            pynini.compose(double_char, NEMO_ALPHA + delete_space + NEMO_ALPHA)
        )
        triple_char_to_char = pynini.compose(
            triple_char, NEMO_ALPHA + delete_space + NEMO_ALPHA + delete_space + NEMO_ALPHA
        )
        self.double_triple_graph = triple_char_to_char | double_char_to_char
        self.alpha_graph = (self.double_triple_graph  | character)
        sequence = (self.alpha_graph + pynini.closure(delete_space + self.alpha_graph,
                                                         1)) | double_char_to_char | triple_char_to_char
        self.fst = sequence

