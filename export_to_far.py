from en.oov_class_numeric_sequence import NumericSequence
from en.oov_class_alpha_sequence import AlphaSequence
from en.oov_class_alpha_numeric_sequence import AlphaNumericSequence
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


#ns_replace

fst_dict = {
    '$OOV_NUMERIC_SEQUENCE': nseq.fst.optimize(),
    '$OOV_ALPHA_SEQUENCE': aseq.fst.optimize(),
    '$OOV_ALPHA_NUMERIC_SEQUENCE': anseq.fst.optimize(),
    'passthrough': passthrough.phrase_fst.optimize(),
    'space': NEMO_WHITE_SPACE.optimize()

}

fst_weights={
        'passthrough': 0,
    'space': 1

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


