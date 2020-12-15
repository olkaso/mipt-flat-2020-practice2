import unittest
import algo

grammar = dict()
grammar['S'] = ['S+P', 'P']
grammar['P'] = ['P*T', 'T']
grammar['T'] = ['(S)', 'x', 'y', 'z']


class TestEarley(unittest.TestCase):
    def test_scan(self):
        D = [set() for i in range(5)]
        D5 = {('T', 3, '(S)', 0), ('P', 1, 'T', 0), ('S', 1, 'P', 0), ('S', 1, 'S+P', 0),
              ('P', 1, 'P*T', 0), ('X', 1, 'S', 0)}
        D.append(D5)
        D6 = {('P', 2, 'P*T', 0)}
        algo.Algo.scan(D, '*', 5)
        self.assertEqual(D6, D[6])

    def test_predict(self):
        D = [set() for i in range(5)]
        D5 = {('T', 3, '(S)', 0), ('P', 1, 'T', 0), ('S', 1, 'P', 0), ('S', 1, 'S+P', 0),
              ('P', 1, 'P*T', 0), ('X', 1, 'S', 0)}
        D.append(D5)
        D6 = {('T', 0, 'z', 6), ('T', 0, 'y', 6), ('P', 2, 'P*T', 0), ('T', 0, 'x', 6), ('T', 0, '(S)', 6)}
        D.append({('P', 2, 'P*T', 0)})
        algo.Algo.predict(D, 6, grammar)
        self.assertEqual(D6, D[6])

    def test_complete(self):
        D = [set() for i in range(5)]
        D5 = {('T', 3, '(S)', 0), ('P', 1, 'T', 0), ('S', 1, 'P', 0), ('S', 1, 'S+P', 0),
              ('P', 1, 'P*T', 0), ('X', 1, 'S', 0)}
        D.append(D5)
        D6 = {('T', 0, 'z', 6), ('T', 0, 'y', 6), ('P', 2, 'P*T', 0), ('T', 0, 'x', 6), ('T', 0, '(S)', 6)}
        D.append(D6)
        D7 = {('P', 3, 'P*T', 0), ('T', 1, 'z', 6)}
        D.append({('T', 1, 'z', 6)})
        algo.Algo.complete(D, 7)
        self.assertEqual(D7, D[7])

    def test_earley(self):
        word_true = '(x+y)*z'
        word_false = '(x+)*z'
        self.assertTrue(algo.earley(grammar, word_true))
        self.assertFalse(algo.earley(grammar, word_false))


if __name__ == '__main__':
    unittest.main()
