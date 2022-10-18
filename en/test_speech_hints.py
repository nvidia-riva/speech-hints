from en.oov_class_numeric_sequence import NumericSequence
from en.oov_class_alpha_sequence import AlphaSequence
from en.oov_class_alpha_numeric_sequence import AlphaNumericSequence
from en.utils import apply_fst
from en.primitives import NEMO_SPACE
from en.passthrough import PassThrough

import pynini
from pynini.lib import pynutil


nseq = NumericSequence()
aseq = AlphaSequence()
passthrough = PassThrough()

#ns_replace

fst_dict={
    '$OOV_NUMERIC_SEQUENCE': nseq.fst,
    '$OOV_ALPHA_SEQUENCE': aseq.fst,
}

def get_fst(word:str):
    return fst_dict.get(word, pynini.accep(word))


def speech_hint_to_fst(speech_hint:str):
    if speech_hint in fst_dict:
        speech_hint_fst = passthrough.passthrough_fst(get_fst(speech_hint))
    else:
        word, speech_hint_words = speech_hint.split(' ', maxsplit=1)
        speech_hint_fst = get_fst(word)

        for word in speech_hint_words.split(' '):
            speech_hint_fst += NEMO_SPACE + get_fst(word)

    return pynutil.add_weight(speech_hint_fst,-0.001)|passthrough.sent_fst


speech_hint_phrase="my phone number is $OOV_NUMERIC_SEQUENCE"
speech_hint_class="$OOV_NUMERIC_SEQUENCE"

speech_hint_fst = speech_hint_to_fst(speech_hint_phrase)
speech_hint_class_fst = speech_hint_to_fst(speech_hint_class)

apply_fst("my phone number is five six seven eight", speech_hint_fst)
# Output: my phone number is 5678

apply_fst("i would like to call five six seven eight", speech_hint_fst)
# Output: i would like to call five six seven eight

apply_fst("my phone number is five six seven eight", speech_hint_class_fst)
# Output: my phone number is 5678

apply_fst("i would like to call five six seven eight", speech_hint_class_fst)
# Output: i would like to call 5678
