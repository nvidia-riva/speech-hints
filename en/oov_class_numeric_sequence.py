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


class NumericSequence:
    def __init__(self):
        digit_to_str = (
            pynini.invert(pynini.string_file(get_abs_path("data/numbers/digit.tsv")).optimize())
            | pynini.cross("0", pynini.union("o", "oh", "zero")).optimize()
        )

        str_to_digit = pynini.invert(digit_to_str)

        double_digit = pynini.union(
            *[
                pynini.cross(
                    pynini.project(str(i) @ digit_to_str, "output")
                    + pynini.accep(" ")
                    + pynini.project(str(i) @ digit_to_str, "output"),
                    pynutil.insert("double ") + pynini.project(str(i) @ digit_to_str, "output"),
                )
                for i in range(10)
            ]
        )
        double_digit.invert()

        triple_digit = pynini.union(
            *[
                pynini.cross(
                    pynini.project(str(i) @ digit_to_str, "output")
                    + pynini.accep(" ")
                    + pynini.project(str(i) @ digit_to_str, "output")
                    + pynini.accep(" ")
                    + pynini.project(str(i) @ digit_to_str, "output"),
                    pynutil.insert("triple ") + pynini.project(str(i) @ digit_to_str, "output"),
                )
                for i in range(10)
            ]
        )
        triple_digit.invert()
        double_digit_to_digit = (
            pynini.compose(double_digit, str_to_digit + pynutil.delete(" ") + str_to_digit)
        )
        triple_digit_to_digit = pynini.compose(
            triple_digit, str_to_digit + delete_space + str_to_digit + delete_space + str_to_digit
        )
        self.double_triple_graph = triple_digit_to_digit | double_digit_to_digit

        self.numeric_graph = (
            self.double_triple_graph| str_to_digit
        ).optimize()

        sequence = ((self.numeric_graph + pynini.closure(delete_space + self.numeric_graph,
                                                      1)) | double_digit_to_digit | triple_digit_to_digit).optimize()

        self.fst = pynini.compose(sequence,
                                  NEMO_DIGIT ** (2, ...)).optimize()
