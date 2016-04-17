import requests
import os

def uploadFile(file, roll, course):
	url = 'http://10.0.2.22/upload.php'
	files = {'fileToUpload': open(file, 'rb')}
	data = {'roll':roll, 'course':course}
	r = requests.post(url, files=files, data=data)
	# print r.text


def listUploads(course):
	url = 'http://10.0.2.22/listfiles.php'
	data = {'course':course}
	r = requests.post(url, data=data)
	fileicon = 'pdficon.png'
	files = r.text.split()
	uploadedby = []
	filename = []
	icons = []
	for i in files:
		uploadedby.append(i[:9])
		filename.append(i[9:])
		icons.append(fileicon)
	return icons, filename, uploadedby


# listUploads("CS203")
# uploadFile('exam.py')