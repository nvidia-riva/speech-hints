import pynini
from en.utils import get_abs_path
from nemo_text_processing.text_normalization.en.graph_utils import GraphFst
from nemo_text_processing.inverse_text_normalization.en.taggers.telephone import (
    get_serial_number,
)
from nemo_text_processing.inverse_text_normalization.en.taggers.cardinal import (
    CardinalFst,
)
from en.primitives import (
    NEMO_ALPHA,
    NEMO_DIGIT,
    NEMO_SIGMA,
    delete_extra_space,
    delete_space,
    insert_space,
    plurals,
)
from pynini.lib import pynutil


class FullPhoneNum(GraphFst):
    def __init__(self):
        super().__init__(name="full_phone_num", kind="classify")
        # country code, number_part, extension
        digit_to_str = (
            pynini.invert(
                pynini.string_file(get_abs_path("data/numbers/digit.tsv")).optimize()
            )
            | pynini.cross("0", pynini.union("o", "oh", "zero")).optimize()
        )

        str_to_digit = pynini.invert(digit_to_str)

        double_digit = pynini.union(
            *[
                pynini.cross(
                    pynini.project(str(i) @ digit_to_str, "output")
                    + pynini.accep(" ")
                    + pynini.project(str(i) @ digit_to_str, "output"),
                    pynutil.insert("double ")
                    + pynini.project(str(i) @ digit_to_str, "output"),
                )
                for i in range(10)
            ]
        )
        double_digit.invert()

        # to handle cases like "one twenty three"
        cardinal = CardinalFst()
        two_digit_cardinal = pynini.compose(
            cardinal.graph_no_exception, NEMO_DIGIT ** 2
        )
        double_digit_to_digit = (
            pynini.compose(
                double_digit, str_to_digit + pynutil.delete(" ") + str_to_digit
            )
            | two_digit_cardinal
        )

        single_or_double_digit = (
            pynutil.add_weight(double_digit_to_digit, -0.0001) | str_to_digit
        ).optimize()
        single_or_double_digit |= (
            single_or_double_digit
            + pynini.closure(
                pynutil.add_weight(pynutil.delete(" ") + single_or_double_digit, 0.0001)
            )
        ).optimize()

        area_part = (
            pynutil.add_weight(
                pynini.compose(single_or_double_digit, NEMO_DIGIT ** 3), 0.0001
            )
            | pynutil.add_weight(pynini.cross("eight hundred", "800"), 1)
        ) + pynutil.delete(" ")

        number_part = pynini.compose(
            single_or_double_digit,
            pynutil.insert("-")
            + NEMO_DIGIT ** 3
            + pynutil.insert("-")
            + NEMO_DIGIT ** 4,
        ).optimize()

        cardinal_option = pynini.compose(single_or_double_digit, NEMO_DIGIT ** (2, 3))

        country_code = pynini.closure(pynini.cross("plus ", "+"), 0, 1) + (
            (pynini.closure(str_to_digit + pynutil.delete(" "), 0, 2) + str_to_digit)
            | cardinal_option
        )

        optional_country_code = pynini.closure(
            country_code + pynutil.delete(" ") + pynutil.insert("-"), 0, 1
        ).optimize()
        graph = optional_country_code + area_part + number_part

        self.fst = graph.optimize()
