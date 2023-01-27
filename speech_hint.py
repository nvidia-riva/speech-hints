from en.oov_class_numeric_sequence import NumericSequence
from en.oov_class_alpha_sequence import AlphaSequence
from en.oov_class_alpha_numeric_sequence import AlphaNumericSequence
from en.address_num import AddressNum
from en.full_phone_num import FullPhoneNum
from en.postal_code import PostalCode
from en.ordinal import Ordinal
from en.month import Month
from en.decimal import Decimal
from en.percent import Percent
from en.day import Day
from en.primitives import NEMO_SPACE
from en.passthrough import PassThrough
from en.time import Time
from en.money import Money
import pynini
from pynini.lib import pynutil


aseq = AlphaSequence()
anseq = AlphaNumericSequence(aseq, NumericSequence(o_is_zero=False))
passthrough = PassThrough()

# ns_replace

fst_dict = {
    "$OOV_NUMERIC_SEQUENCE": NumericSequence().fst,
    "$OOV_ALPHA_SEQUENCE": aseq.fst,
    "$OOV_ALPHA_NUMERIC_SEQUENCE": anseq.fst,
    "$ADDRESSNUM": AddressNum().fst,
    "$FULLPHONENUM": FullPhoneNum().fst,
    "$POSTALCODE": PostalCode().fst,
    "$OOV_CLASS_ORDINAL": Ordinal().fst,
    "$OOV_CLASS_NUMERIC": Decimal().fst,
    "$PERCENT": Percent().fst,
    "$TIME": Time().fst,
    "$MONEY": Money().fst,
    "$MONTH": Month().fst,
    "$DAY": Day().fst,
}


def get_fst(word: str):
    return fst_dict.get(word, pynini.accep(word))


def speech_hint_to_fst(speech_hint: str):
    if speech_hint in fst_dict:
        speech_hint_fst = get_fst(speech_hint)

    else:
        word, speech_hint_words = speech_hint.split(" ", maxsplit=1)
        speech_hint_fst = get_fst(word)

        for word in speech_hint_words.split(" "):
            speech_hint_fst += pynini.closure(NEMO_SPACE) + get_fst(word)

    return passthrough.passthrough_fst(speech_hint_fst)


def apply_hint(utterance: str, hint: str):
    utterance = f" {utterance.strip()} "
    hint_fst = speech_hint_to_fst(hint)
    try:
        return pynini.shortestpath(utterance @ hint_fst).string().strip()
    except pynini.FstOpError:
        print(f"Error: No valid output with given input: '{utterance}, {hint}'")
