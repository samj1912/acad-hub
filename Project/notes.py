import requests
import os

def uploadFile(file, roll, course):
	print course
	url = 'http://10.0.2.22/upload.php'
	files = {'fileToUpload': open(file, 'rb')}
	data = {'roll':roll, 'course':course}
	r = requests.post(url, files=files, data=data)
	print r.text


def listUploads():
	files = os.listdir('.')
	fileicon = 'pdficon.png'
	x = []
	for i in files:
		x.append(fileicon)
	return x, files


# listUploads()
# uploadFile('exam.py')