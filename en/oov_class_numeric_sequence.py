from en.primitives import (
    NEMO_ALNUM,
    NEMO_ALPHA,
    NEMO_DIGIT,
NEMO_WHITE_SPACE,
    delete_space,
    insert_space,
delete_one_space,
    digit_to_str,
    digit_to_str_simple
)
import pynini
from pynini.lib import pynutil


class NumericSequence:
    def __init__(self, o_is_zero:bool=True):
        delete_spaces = pynini.closure(pynutil.delete(" "))
        if o_is_zero:
            digit_to_str_ns=digit_to_str
        else:
            digit_to_str_ns=digit_to_str_simple

        str_to_digit = digit_to_str_ns.invert()
        double_digit = pynini.union(
            *[
                pynini.cross(
                    pynini.project(str(i) @ digit_to_str_ns, "output")
                    + pynini.accep(" ")
                    + pynini.project(str(i) @ digit_to_str_ns, "output"),
                    pynutil.insert("double ") + pynini.project(str(i) @ digit_to_str_ns, "output"),
                )
                for i in range(10)
            ]
        )
        double_digit.invert()

        triple_digit = pynini.union(
            *[
                pynini.cross(
                    pynini.project(str(i) @ digit_to_str_ns, "output")
                    + pynini.accep(" ")
                    + pynini.project(str(i) @ digit_to_str_ns, "output")
                    + pynini.accep(" ")
                    + pynini.project(str(i) @ digit_to_str_ns, "output"),
                    pynutil.insert("triple ") + pynini.project(str(i) @ digit_to_str_ns, "output"),
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

        self.numeric_graph = pynutil.add_weight((
            self.double_triple_graph| str_to_digit
        ).optimize(),-0.05)

        sequence = ((self.numeric_graph + pynini.closure(pynutil.add_weight(delete_spaces + self.numeric_graph,-0.001) ,
                                                      2)) | double_digit_to_digit | triple_digit_to_digit).optimize()

        self.fst = pynini.compose(NEMO_WHITE_SPACE+sequence+NEMO_WHITE_SPACE,
                                  NEMO_WHITE_SPACE+NEMO_DIGIT ** (2, ...)+NEMO_WHITE_SPACE).optimize()
