import pytest
from parameterized import parameterized
from tests_en.test_utils import parse_test_case_file
from speech_hint import apply_hint

try:
    PYNINI_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    PYNINI_AVAILABLE = False


class TestOovAplhaSeq:
    @parameterized.expand(parse_test_case_file('data/test_cases_OOV_ALPHANUMERIC_SEQUENCE.txt'))
    @pytest.mark.skipif(
        not PYNINI_AVAILABLE,
        reason="`pynini` not installed, please install via nemo_text_processing/pynini_install.sh",
    )
    def test_sh(self, test_input, expected, hint):
        print(test_input)
        pred = apply_hint(test_input, hint)
        assert pred == expected