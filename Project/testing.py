import unittest
from details import semFinder, depFinder

class unitTester(unittest.TestCase):

    def test_is_correct_sem(self):
    	rolls = ['120101039', '130101058','140101052','150101043'] #year=rolls[0:2]
    	sems = [8, 6,4,2]
    	for i in range(len(rolls)):
        	self.assertEqual(semFinder(rolls[i]), sems[i]) #assertEqual(a,b) = assertEqual(a==b)

    def test_is_correct_dep(self):
    	#deps={"01":"CSE","02":"ECE","03":"ME","04":"CE","05":"bdes","06":"BT","07":"CL","08":"EEE","21":"EPh","22":"CST","23":"MC"}
    	Rollnumber = ['140101057','140102032','140103078','140104080','140105082','140106035','140407025','140508075','140021150','141022402','140123024']
    	Department = ['CSE','ECE','ME','CE','bdes','BT','CL','EEE','EPh','CST','MC']
    	for i in range(len(Rollnumber)):
        	self.assertEqual(depFinder(Rollnumber[i]), Department[i]) #assertEqual(a,b) = assertEqual(a==b)

if __name__ == '__main__':
    unittest.main()
