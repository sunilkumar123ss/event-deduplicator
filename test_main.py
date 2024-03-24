import importlib.util
from pathlib import Path
import sys
import unittest
_spec = importlib.util.spec_from_file_location('lab_' + Path(__file__).parent.name.replace('-', '_'), Path(__file__).with_name('main.py'))
m = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = m
_spec.loader.exec_module(m)

class DedupTests(unittest.TestCase):

    def test_first_and_duplicate(self):
        d = m.Deduplicator()
        self.assertTrue(d.accept('a', 0))
        self.assertFalse(d.accept('a', 1))





if __name__ == '__main__':
    unittest.main()
