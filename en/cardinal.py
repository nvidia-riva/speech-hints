from nemo_text_processing.inverse_text_normalization.en.taggers.cardinal import (
    CardinalFst,
)
from nemo_text_processing.inverse_text_normalization.en.taggers.ordinal import (
    OrdinalFst as TOrdinal,
)
from nemo_text_processing.inverse_text_normalization.en.verbalizers.ordinal import (
    OrdinalFst as VOrdinal,
)


class Cardinal:
    def __init__(self):
        self.fst = CardinalFst().graph
