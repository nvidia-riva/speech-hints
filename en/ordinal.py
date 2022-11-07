from nemo_text_processing.inverse_text_normalization.en.taggers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.en.taggers.ordinal import OrdinalFst as TOrdinal
from nemo_text_processing.inverse_text_normalization.en.verbalizers.ordinal import OrdinalFst as VOrdinal

class Ordinal:
    def __init__(self):
        cardinal = CardinalFst()
        t_fst = TOrdinal(cardinal).fst
        v_fst = VOrdinal().fst
        self.fst = (t_fst @ v_fst).optimize() 
