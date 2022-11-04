from en.oov_class_numeric_sequence import NumericSequence
from en.oov_class_alpha_sequence import AlphaSequence
from en.oov_class_alpha_numeric_sequence import AlphaNumericSequence
from en.address_num import AddressNum
from en.full_phone_num import FullPhoneNum
from en.postal_code import PostalCode
from en.ordinal import Ordinal
from en.month import Month
from en.utils import apply_fst
from en.primitives import NEMO_SPACE
from en.passthrough import PassThrough

import pynini
from pynini.lib import pynutil


nseq = NumericSequence()
aseq = AlphaSequence()
anseq = AlphaNumericSequence(aseq,nseq)
passthrough = PassThrough()

anum = AddressNum()
fpnum = FullPhoneNum()
pcode = PostalCode()
ordinal = Ordinal()
month = Month()

#ns_replace

fst_dict={
    '$OOV_NUMERIC_SEQUENCE': nseq.fst,
    '$OOV_ALPHA_SEQUENCE': aseq.fst,
    '$OOV_ALPHA_NUMERIC_SEQUENCE': anseq.fst,
    '$ADDRESSNUM': anum.fst,
    '$FULLPHONENUM': fpnum.fst,
    '$POSTALCODE': pcode.fst, 
    '$OOV_CLASS_ORDINAL': ordinal.fst,
    '$MONTH': month.fst,
}

def get_fst(word:str):

    return  pynutil.add_weight(fst_dict.get(word,pynini.accep(word)),0.25)


def speech_hint_to_fst(speech_hint:str):
    if speech_hint in fst_dict:
        speech_hint_fst = get_fst(speech_hint)
    else:
        word, speech_hint_words = speech_hint.split(' ', maxsplit=1)
        speech_hint_fst = get_fst(word)

        for word in speech_hint_words.split(' '):
            speech_hint_fst += pynini.closure(NEMO_SPACE) + get_fst(word)

    return passthrough.passthrough_fst(speech_hint_fst)

def _add_spaces_(s:str):
    return f" {s.strip()} "


speech_hint_phrase="my phone number is $OOV_NUMERIC_SEQUENCE good"
speech_hint_class="$OOV_NUMERIC_SEQUENCE"

speech_hint_fst = speech_hint_to_fst(speech_hint_phrase)
speech_hint_class_fst = speech_hint_to_fst(speech_hint_class)
#zero padding(left and right) is required for some of the grammars
apply_fst(" my phone number is five six seven eight good ", speech_hint_fst)
# Output: my phone number is 5678

apply_fst("i would like to call five six seven eight", speech_hint_fst)
# Output: i would like to call five six seven eight

apply_fst(" my phone number is five six seven eight ", speech_hint_class_fst)
# Output: my phone number is 5678

apply_fst("i would like to call five six seven eight", speech_hint_class_fst)
# Output: i would like to call 5678
apply_fst((" b b d e d c "), speech_hint_to_fst("$OOV_ALPHA_SEQUENCE"))
apply_fst(" double b b d e d c ", speech_hint_to_fst("$OOV_ALPHA_SEQUENCE"))

apply_fst(" i work at double b b d e c radio ", speech_hint_to_fst("$OOV_ALPHA_SEQUENCE"))
apply_fst(" i work at double b b c radio d ", speech_hint_to_fst("$OOV_ALPHA_SEQUENCE"))
apply_fst(" i work at b b c radio", speech_hint_to_fst("i work at $OOV_ALPHA_SEQUENCE "))
apply_fst(" i work at t t k j j j low d ", speech_hint_to_fst("$OOV_ALPHA_SEQUENCE"))
apply_fst(" i work at b b c nine ", speech_hint_to_fst("$OOV_ALPHA_NUMERIC_SEQUENCE"))

apply_fst(" my postal code is one zero zero one zero ", speech_hint_to_fst("$POSTALCODE"))
apply_fst(" my postal code is six double oh one oh ", speech_hint_to_fst("$POSTALCODE"))

apply_fst(" my phone number is one eight hundred five five five four oh oh one ", speech_hint_to_fst("$FULLPHONENUM"))
apply_fst(" i would like to call plus one eight hundred five five five four oh oh one ", speech_hint_to_fst("$FULLPHONENUM"))
apply_fst(" please call seven one eight five five five six one oh one ", speech_hint_to_fst("$FULLPHONENUM"))

apply_fst(" i work at one peachtree street northeast ", speech_hint_to_fst("$ADDRESSNUM"))
apply_fst(" i work at one hundred ninety one peachtree street northeast ", speech_hint_to_fst("$ADDRESSNUM"))
apply_fst(" i work at a hundred ninety one peachtree street northeast ", speech_hint_to_fst("$ADDRESSNUM"))
apply_fst(" i work at ten and a half peachtree street northeast ", speech_hint_to_fst("$ADDRESSNUM"))
apply_fst(" i work at twenty four thousand seven hundred and seven vantage point terrace malibu ", speech_hint_to_fst("$ADDRESSNUM"))

apply_fst(" it is my third time doing this ", speech_hint_to_fst("$OOV_CLASS_ORDINAL"))
apply_fst(" today is their fifty first anniversary ", speech_hint_to_fst("$OOV_CLASS_ORDINAL"))
apply_fst(" they won the four thousand six hundred and twenty seventh place ", speech_hint_to_fst("$OOV_CLASS_ORDINAL"))

apply_fst(" they will get back to you by july ", speech_hint_to_fst("$MONTH"))
apply_fst(" it is january already ", speech_hint_to_fst("$MONTH"))
apply_fst(" the next semester will start in april  ", speech_hint_to_fst("$MONTH"))
