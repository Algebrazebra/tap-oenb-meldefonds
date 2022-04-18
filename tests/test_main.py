import unittest
from tap_oenb_meldefonds.main import main as tap_execute

from unittest.mock import patch
from singertools import check_tap


def load_sample_meldefonds_csv() -> str:
    """Read sample Meldefonds CSV into Python string."""
    with open("./sample_meldefonds.csv", "r") as f:
        meldefonds_csv = f.read()
    return meldefonds_csv


class TestTapOenbMeldefonds(unittest.TestCase):

    @patch("tap_oenb_meldefonds.main.download_meldefonds_data")
    def test_tap_end_to_end(self, mock_download):
        """Test whether tap conforms to Singer spec using `singer-tools.check_tap`."""
        mock_download.return_value = load_sample_meldefonds_csv()
        import tap_oenb_meldefonds
        summary = check_tap.run_and_summarize(tap_oenb_meldefonds.main, config="")
        print(summary)
        assert 0


if "__name__" == "__main__":
    unittest.main()
