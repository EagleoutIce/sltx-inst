import unittest
from pathlib import Path

import sltxtest.util.globals as sug
from sltxtest.util.dir import retrieve_tmpdir, assert_dir_exact_files


class TestDependencies(unittest.TestCase):
    def test_local_pull(self):
        test_dep_file: Path = Path(__file__).parent / 'local-repo/sltx-dep.yml'
        target_dir = retrieve_tmpdir()
        sug.run_bare_sltx(['dep', '-l', target_dir, str(test_dep_file)])
        assert_dir_exact_files(self, target_dir, {
            'info.txt': ["Important information"],
            'recursive.1': ["Rekursionsdatei", "Uno"],
            'recursive.2': ["Rekursionsdatei", "Duo"],
            'recursive.3': ["Rekursionsdatei", "Tre"],
            'recursiveb.1': ["Rekursionsdatei b", "Uno"],
            'recursive-target.info': ["Help me i am a target"],
            'extra.rofl': ["Mich gibts nur, wenn die profiles (default) richtig gewählt werden!"],
            'datei.a': ["Die a-Datei"],
            'datei.b': ["Die b-Datei"],
            'datei.x': ["Die x-Datei"]
        })

    def tearDown(self):
        sug.restore_configuration()


if __name__ == '__main__':
    unittest.main()
