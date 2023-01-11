import argparse

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

from speech_hint import fst_dict

import pynini
from pynini.lib import pynutil
from pynini.export import export
import os

parser = argparse.ArgumentParser()
parser.add_argument('--export_acceptors', action='store_true',
                    help='export acceptors instead of transducers')

passthrough = PassThrough()

fst_dict['$__PASSTHROUGH__'] = passthrough.phrase_fst.optimize()
fst_dict['$__SPACE__'] = NEMO_WHITE_SPACE.optimize()



fst_weights={
        '$__PASSTHROUGH__': 0,
    '$__SPACE__': 1

        }

def export_grammars(grm_dict:dict, export_acceptors:bool, lang="en", path_prefix=''):

    if len(path_prefix)>3 and path_prefix[-1]!="/":
        path_prefix = path_prefix+'/'
    fpath=f"{path_prefix}far/{lang}"
    fname=f"{fpath}/speech_class.far"
    os.makedirs(fpath, exist_ok=True)
    fst_export=export.Exporter(fname)
    for speech_class in grm_dict:
        weight= fst_weights.get(speech_class,-0.0001)
        fst = pynutil.add_weight(grm_dict[speech_class], weight)
        if export_acceptors:
           fst = fst @ pynini.invert(fst)
        fst_export[speech_class] = fst.optimize()
    fst_export.close()
    print(f"Created {fname}")

if __name__=="__main__":
    args = parser.parse_args()
    export_grammars(fst_dict, args.export_acceptors)


