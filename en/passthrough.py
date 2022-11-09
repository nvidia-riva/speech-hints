from en.primitives import (
    NEMO_ALNUM,
    NEMO_ALPHA,
    NEMO_DIGIT,
    NEMO_SPACE,
NEMO_NOT_SPACE,
    delete_space,
    insert_space,
    str_to_digit,
    digit_to_str,
NEMO_WHITE_SPACE
)
import pynini

from pynini.lib import pynutil



# class PassThrough:
#     def __init__(self):
#         self.word_fst = pynini.closure(NEMO_NOT_SPACE)**(2,...)
#         self.sent_fst = self.word_fst+pynini.closure(NEMO_SPACE+self.word_fst)
#
#     def passthrough_fst(self, fst):
#         return pynini.closure(NEMO_SPACE|self.sent_fst|fst)


class PassThrough:
    def __init__(self):
        self.longest_path=pynini.closure(pynutil.add_weight(NEMO_NOT_SPACE|NEMO_SPACE,100))
        self.word_fst = pynini.closure(NEMO_NOT_SPACE)
        self.sent_fst = pynini.closure(NEMO_SPACE|self.word_fst)
        self.phrase_fst = pynini.closure(pynini.closure(NEMO_NOT_SPACE)**(2,...) + NEMO_WHITE_SPACE)
        w_fst = pynini.closure(NEMO_NOT_SPACE, 2)
        self.w1 = pynutil.add_weight(self.longest_path + NEMO_WHITE_SPACE + w_fst, 1)
        self.w2 = pynutil.add_weight(w_fst + NEMO_WHITE_SPACE + self.longest_path, 1)
        self.w3 = pynutil.add_weight(w_fst + pynini.closure(self.longest_path + w_fst), 1)
        self.w4 = pynutil.add_weight(pynini.closure(self.longest_path + w_fst), 0.5)

        #self.phrase_fst |= NEMO_ALPHA  + NEMO_SPACE + pynini.closure(pynini.closure(NEMO_ALPHA)**(2,...) + NEMO_SPACE)
        self.phrase_fst = pynini.closure(self.w1, 1) | pynini.closure(self.w2, 1) | pynini.closure(self.w3, 1)
        self.phrase_fst |= pynini.closure(NEMO_WHITE_SPACE)

        self.middle_phrase_fst = NEMO_SPACE + self.phrase_fst + NEMO_SPACE

    def passthrough_fst(self, fst):
        return  pynutil.add_weight(self.middle_phrase_fst + pynutil.add_weight(fst, -10) + self.middle_phrase_fst, weight=-100) | pynini.closure(
           self.phrase_fst| self.longest_path | pynutil.add_weight(fst, -10))



