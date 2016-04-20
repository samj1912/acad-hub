import unittest
from details import semFinder, depFinder

class unitTester(unittest.TestCase):

    def test_is_correct_sem(self):
    	rolls = ['120101039', '130101058','140101052','150101043']
    	sems = [8, 6,4,2]
    	for i in range(len(rolls)):
        	self.assertEqual(semFinder(rolls[i]), sems[i])

    # def test_is_correct_dep(self)

if __name__ == '__main__':
    unittest.main()