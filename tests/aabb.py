import unittest
import pytomata

class TestAABBProgram(unittest.TestCase):

  def test_program(self):

      a = pytomata.Automata('tests/programs/aabb.yml')
      self.assertEqual(True, a.validate('aabb'))
      self.assertEqual(False, a.validate('ab'))
      self.assertEqual(False, a.validate('abab'))

if __name__ == '__main__':
    unittest.main()
