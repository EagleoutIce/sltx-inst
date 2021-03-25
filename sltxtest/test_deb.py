import unittest
from pathlib import Path

import sltxtest.util.globals as sug
import sltxpkg.heart as heart


class TestCache(unittest.TestCase):

    def test_local_pull(self):
        test_dep_file: Path = Path(__file__).parent / 'local-repo/sltx-dep.yml';
        heart.run(['dep', '-l', './target', str(test_dep_file)])

    def tearDown(self):
        sug.restore_configuration()


if __name__ == '__main__':
    unittest.main()
