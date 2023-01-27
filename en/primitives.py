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

import os
import string
import pynini

from pathlib import Path
from pynini.examples import plurals
from pynini.lib import byte, pynutil, utf8
from pynini import Far
from en.utils import get_abs_path

NEMO_CHAR = utf8.VALID_UTF8_CHAR

NEMO_DIGIT = byte.DIGIT
NEMO_LOWER = pynini.union(*string.ascii_lowercase).optimize()
NEMO_UPPER = pynini.union(*string.ascii_uppercase).optimize()
NEMO_ALPHA = pynini.union(NEMO_LOWER, NEMO_UPPER).optimize()
NEMO_ALNUM = pynini.union(NEMO_DIGIT, NEMO_ALPHA).optimize()
NEMO_HEX = pynini.union(*string.hexdigits).optimize()
NEMO_NON_BREAKING_SPACE = u"\u00A0"
NEMO_SPACE = " "
NEMO_WHITE_SPACE = pynini.union(" ", "\t", "\n", "\r", u"\u00A0").optimize()
NEMO_NOT_SPACE = pynini.difference(NEMO_CHAR, NEMO_WHITE_SPACE).optimize()
NEMO_NOT_QUOTE = pynini.difference(NEMO_CHAR, r'"').optimize()

NEMO_PUNCT = pynini.union(*map(pynini.escape, string.punctuation)).optimize()
NEMO_GRAPH = pynini.union(NEMO_ALNUM, NEMO_PUNCT).optimize()

NEMO_SIGMA = pynini.closure(NEMO_CHAR)
delete_one_space = pynutil.delete(NEMO_SPACE)

delete_space = pynutil.delete(pynini.closure(NEMO_WHITE_SPACE))
delete_zero_or_one_space = pynutil.delete(pynini.closure(NEMO_WHITE_SPACE, 0, 1))
insert_space = pynutil.insert(" ")
delete_extra_space = pynini.cross(pynini.closure(NEMO_WHITE_SPACE, 1), " ")
delete_preserve_order = pynini.closure(
    pynutil.delete(" preserve_order: true")
    | (pynutil.delete(' field_order: "') + NEMO_NOT_QUOTE + pynutil.delete('"'))
)

suppletive = pynini.string_file(get_abs_path("data/suppletive.tsv"))
# _v = pynini.union("a", "e", "i", "o", "u")
_c = pynini.union(
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "t",
    "v",
    "w",
    "x",
    "y",
    "z",
)
_ies = NEMO_SIGMA + _c + pynini.cross("y", "ies")
_es = NEMO_SIGMA + pynini.union("s", "sh", "ch", "x", "z") + pynutil.insert("es")
_s = NEMO_SIGMA + pynutil.insert("s")

graph_plural = plurals._priority_union(
    suppletive,
    plurals._priority_union(
        _ies, plurals._priority_union(_es, _s, NEMO_SIGMA), NEMO_SIGMA
    ),
    NEMO_SIGMA,
).optimize()

SINGULAR_TO_PLURAL = graph_plural
PLURAL_TO_SINGULAR = pynini.invert(graph_plural)
TO_LOWER = pynini.union(
    *[
        pynini.cross(x, y)
        for x, y in zip(string.ascii_uppercase, string.ascii_lowercase)
    ]
)
TO_UPPER = pynini.invert(TO_LOWER)
MIN_NEG_WEIGHT = -0.0001
MIN_POS_WEIGHT = 0.0001

digit_to_str_simple = (
    pynini.invert(pynini.string_file(get_abs_path("data/numbers/digit.tsv")).optimize())
    | pynini.cross("0", "zero").optimize()
)

digit_to_str = (
    digit_to_str_simple | pynini.cross("0", pynini.union("o", "oh")).optimize()
)

str_to_digit = pynini.invert(digit_to_str)
zero_to_digit = pynini.cross(pynini.union("o", "oh", "zero"), "0").optimize()


class BaseGraph:
    def __init__(self, name: str, kind: str, deterministic: bool = True):
        self.name = name
        self.kind = str
        self._fst = None

        self.far_path = Path(
            os.path.dirname(__file__) + "/grammars/" + kind + "/" + name + ".far"
        )
        if self.far_exist():
            self._fst = Far(
                self.far_path, mode="r", arc_type="standard", far_type="default"
            ).get_fst()
