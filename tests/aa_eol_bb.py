import unittest
import pytomata

class TestAAEOLBBProgram(unittest.TestCase):

  def test_program(self):
      a = pytomata.Automata('tests/programs/aa_eol_bb.yml')
      self.assertEqual(True, a.validate('aa\nbb'))
      self.assertEqual(False, a.validate('aabb'))
      self.assertEqual(False, a.validate('abab'))

if __name__ == '__main__':
    unittest.main()
