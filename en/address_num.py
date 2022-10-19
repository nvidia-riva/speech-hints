import pynini
from pynini.lib import pynutil
from nemo_text_processing.text_normalization.en.taggers.fraction import FractionFst as TFractionFst
from nemo_text_processing.text_normalization.en.verbalizers.fraction import FractionFst as VFractionFst

from en.primitives import (
    NEMO_ALPHA, 
    NEMO_DIGIT, 
    NEMO_SIGMA,
    NEMO_SPACE,
    delete_space    
)
from en.utils import get_abs_path

class AddressNum:
    def __init__(self, v_fraction: VFractionFst, t_fraction: TFractionFst):
        
        # Handle cardinal
        graph_zero = pynini.string_file(get_abs_path("data/numbers/zero.tsv"))
        graph_digit = pynini.string_file(get_abs_path("data/numbers/digit.tsv"))
        graph_ties = pynini.string_file(get_abs_path("data/numbers/ties.tsv"))
        graph_teen = pynini.string_file(get_abs_path("data/numbers/teen.tsv"))

        # Handle "a hundrend"
        graph_digit_and_a = (
            pynini.invert(graph_digit)
            | pynini.cross("1", pynini.union("a", "one")).optimize()
        )
        graph_digit = pynini.invert(graph_digit_and_a)

        graph_hundred = pynini.cross("hundred", "")

        graph_hundred_component = pynini.union(graph_digit + delete_space + graph_hundred, pynutil.insert("0"))
        graph_hundred_component += delete_space
        graph_hundred_component += pynini.union(
            graph_teen | pynutil.insert("00"),
            (graph_ties | pynutil.insert("0")) + delete_space + (graph_digit | pynutil.insert("0")),
        )

        graph_hundred_component_at_least_one_none_zero_digit = graph_hundred_component @ (
            pynini.closure(NEMO_DIGIT) + (NEMO_DIGIT - "0") + pynini.closure(NEMO_DIGIT)
        )
        self.graph_hundred_component_at_least_one_none_zero_digit = (
            graph_hundred_component_at_least_one_none_zero_digit
        )

        graph_thousands = pynini.union(
            graph_hundred_component_at_least_one_none_zero_digit + delete_space + pynutil.delete("thousand"),
            pynutil.insert("000", weight=0.1),
        )

        graph = pynini.union(
            graph_thousands
            + delete_space
            + graph_hundred_component,
            graph_zero,
        )

        graph = graph @ pynini.union(
            pynutil.delete(pynini.closure("0")) + pynini.difference(NEMO_DIGIT, "0") + pynini.closure(NEMO_DIGIT), "0"
        )
        
        graph = (
            pynini.cdrewrite(pynutil.delete("and"), NEMO_SPACE, NEMO_SPACE, NEMO_SIGMA)
            @ (NEMO_ALPHA + NEMO_SIGMA)
            @ graph
        )

        digit_graph = graph.optimize()

        fraction_graph = t_fraction.fst @ v_fraction.fst
        fraction_graph.invert()

        final_graph = (
            pynutil.add_weight(digit_graph, weight=0.0001)
            | pynutil.add_weight(fraction_graph, 1)
        )

        self.fst = final_graph.optimize()
