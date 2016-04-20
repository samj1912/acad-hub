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

    def test_is_uploading(self):
    	with open("test.txt","w") as f:
   			f.write("Test")
   			self.assertEqual(uploadFile("test.txt","100101001","TEST"),200)
   			os.remove("test.txt")

   	def test_is_listing(self):
   		self.assertEqual(listUploads("TEST")[1][0],"test.txt")


   	def test_is_downloading(self):
   		downloadFile('test.txt','/home/sam/Desktop/bkp/team10cs243','TEST',"100101001","0.00(0)")	
   		x=""
   		with open("../test.txt","r") as f:
 			for i in f:
 				x=i
 		self.assertEqual(x,"Test")
 		os.remove("../test.txt")

 	def test_courses(self):
		depts = ["CSE","ECE","ME","CE","bdes","BT","CL","EEE","EPh","CST","MC"]
		with open("course.json", 'r') as f:
			data = json.load(f)
		j = 0
		for dept in depts:
			for i in range(1,9):
				self.assertEqual(showBooks(dept, i, "courses"), data[j])
				j += 1

if __name__ == '__main__':
    unittest.main()
