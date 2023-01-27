# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright 2015 and onwards Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# https://raw.githubusercontent.com/NVIDIA/NeMo/main/nemo_text_processing/inverse_text_normalization/en/taggers/money.py

import pynini
from nemo_text_processing.inverse_text_normalization.en.utils import get_abs_path
from nemo_text_processing.text_normalization.en.graph_utils import (
    NEMO_DIGIT,
    NEMO_NOT_SPACE,
    NEMO_SIGMA,
    GraphFst,
    convert_space,
    delete_extra_space,
    delete_space,
    get_singulars,
    insert_space,
)

from en.decimal import Decimal
from pynini.lib import pynutil


class Money:
    """
    Finite state transducer for classifying money
        e.g. twelve dollars and five cents -> money { integer_part: "12" fractional_part: 05 currency: "$" }

    Args:
        cardinal: CardinalFst
        decimal: DecimalFst
    """

    def __init__(self):
        # quantity, integer_part, fractional_part, currency
        digit_to_str = (
            pynini.invert(
                pynini.string_file(get_abs_path("data/numbers/digit.tsv")).optimize()
            )
            | pynini.cross("0", pynini.union("o", "oh", "zero")).optimize()
        )

        str_to_digit = pynini.invert(digit_to_str)

        decimal = Decimal().fst

        # dollar standalone
        graph_dollar_standalone = (
            pynutil.insert("$")
            + decimal
            + delete_space
            + (pynutil.delete("dollars", -0.002) | pynutil.delete("dollar", -0.001))
        )
        # cents
        graph_cent = pynutil.add_weight(
            pynutil.insert(".0")
            + str_to_digit
            + delete_space
            + (pynutil.delete("cents", -0.002) | pynutil.delete("cent", -0.001)),
            -0.005,
        ) | (
            pynutil.insert(".")
            + decimal
            + delete_space
            + (pynutil.delete("cents", -0.002) | pynutil.delete("cent", -0.001))
        )

        # cents standalone
        graph_cent_standalone = pynutil.add_weight(
            pynutil.insert("$0") + graph_cent, +0.005
        )

        graph_dollar_plus_cent = graph_dollar_standalone | pynutil.add_weight(
            graph_dollar_standalone | pynutil.delete(" and ") + graph_cent, -0.002
        )

        self.fst = graph_dollar_plus_cent | graph_cent_standalone.optimize()
