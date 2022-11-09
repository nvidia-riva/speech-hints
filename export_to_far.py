from en.oov_class_numeric_sequence import NumericSequence
from en.oov_class_alpha_sequence import AlphaSequence
from en.oov_class_alpha_numeric_sequence import AlphaNumericSequence
from en.address_num import AddressNum
from en.full_phone_num import FullPhoneNum
from en.postal_code import PostalCode
from en.ordinal import Ordinal
from en.month import Month
from en.utils import apply_fst
from en.primitives import NEMO_SPACE, NEMO_WHITE_SPACE
from en.passthrough import PassThrough

import pynini
from pynini.lib import pynutil
from pynini.export import export
import os
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

fst_dict = {
    '$OOV_NUMERIC_SEQUENCE': nseq.fst.optimize(),
    '$OOV_ALPHA_SEQUENCE': aseq.fst.optimize(),
    '$OOV_ALPHA_NUMERIC_SEQUENCE': anseq.fst.optimize(),
    '$FULLPHONENUM': fpnum.fst.optimize(),
    '$POSTALCODE': pcode.fst.optimize(), 
    '$OOV_CLASS_ORDINAL': ordinal.fst.optimize(),
    '$MONTH': month.fst.optimize(),
    '$__PASSTHROUGH__': passthrough.phrase_fst.optimize(),
    '$__SPACE__': NEMO_WHITE_SPACE.optimize()

}

fst_weights={
        '$__PASSTHROUGH__': 0,
    '$__SPACE__': 1

        }

def export_grammars(grm_dict:dict, lang="en", path_prefix=''):

    if len(path_prefix)>3 and path_prefix[-1]!="/":
        path_prefix = path_prefix+'/'
    fpath=f"{path_prefix}far/{lang}"
    fname=f"{fpath}/speech_class.far"
    os.makedirs(fpath, exist_ok=True)
    fst_export=export.Exporter(fname)
    for speech_class in grm_dict:
        weight= fst_weights.get(speech_class,-10)
        fst_export[speech_class] = pynutil.add_weight(grm_dict[speech_class],weight).optimize()
    fst_export.close()
    print(f"Created {fname}")

if __name__=="__main__":
    export_grammars(fst_dict)


