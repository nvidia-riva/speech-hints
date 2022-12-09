import pynini
from pynini.lib import pynutil
from en.utils import get_abs_path, num_to_word
from en.primitives import (
    delete_space,
delete_extra_space
)
from nemo_text_processing.inverse_text_normalization.en.taggers.cardinal import CardinalFst


class Time:
    def __init__(self):
        cardinal = pynutil.add_weight(CardinalFst().graph_no_exception, weight=-0.7)

        suffix_graph = pynini.string_file(get_abs_path("data/time/time_suffix.tsv"))
        to_hour_graph = pynini.string_file(get_abs_path("data/time/to_hour.tsv"))
        labels_hour = [num_to_word(x) for x in range(0, 24)]
        labels_minute_single = [num_to_word(x) for x in range(1, 10)]
        labels_minute_double = [num_to_word(x) for x in range(10, 60)]

        graph_minute_single = pynini.union(*labels_minute_single) @ cardinal
        graph_minute_double = pynini.union(*labels_minute_double) @ cardinal
        oclock = pynini.cross(pynini.union("o' clock", "o clock", "o'clock", "oclock", "hundred hours"), "")
        graph_hour = pynini.union(*labels_hour) @ cardinal
        graph_minute = (
            oclock + pynutil.insert("00")
            | pynutil.delete("o") + delete_space + graph_minute_single
            | graph_minute_double
        )

        graph_hhmm = graph_hour + delete_space + pynutil.insert(":") + graph_minute

        graph_past = pynutil.delete("half past")+delete_space+graph_hour+pynutil.insert(":30")
        graph_past |= pynutil.delete("quarter past")+delete_space+graph_hour+pynutil.insert(":15")
        graph_to = pynutil.delete("quarter to")+delete_space+to_hour_graph+pynutil.insert(":45")


        graph_time = pynutil.add_weight(graph_hhmm,-0.0001)
        graph_time |= pynutil.add_weight(graph_hhmm + delete_space + suffix_graph,-0.0001)
        graph_time |= graph_to|graph_past
        self.fst = graph_time.optimize()






