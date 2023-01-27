from en.primitives import (
    NEMO_ALNUM,
    NEMO_ALPHA,
    NEMO_LOWER,
    NEMO_DIGIT,
    NEMO_SPACE,
    delete_space,
    insert_space,
    NEMO_WHITE_SPACE,
)
import pynini
from pynini.lib import pynutil


class AlphaSequence:
    def __init__(self):
        # character = NEMO_ALPHA
        #
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

        double_char_to_char = pynini.compose(
            double_char, NEMO_ALPHA + delete_space + NEMO_ALPHA
        )
        triple_char_to_char = pynini.compose(
            triple_char,
            NEMO_ALPHA + delete_space + NEMO_ALPHA + delete_space + NEMO_ALPHA,
        )
        self.double_triple_graph = triple_char_to_char | double_char_to_char
        character = NEMO_ALPHA | self.double_triple_graph
        word_fst = pynutil.add_weight(pynini.closure(NEMO_ALPHA), -0.0001)
        sequence = (
            pynutil.add_weight(NEMO_WHITE_SPACE + character, 1)
            + pynini.closure(
                pynutil.add_weight(pynutil.delete(" ") + character, -1.01), 1
            )
            + pynutil.add_weight(NEMO_WHITE_SPACE, 0.25)
        )
        sequence = sequence @ (NEMO_WHITE_SPACE + word_fst + NEMO_WHITE_SPACE)

        self.fst = sequence

        self.alpha_graph = self.double_triple_graph | pynini.closure(
            pynutil.delete(" ") + character, 2
        )
