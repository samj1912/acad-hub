import requests
import os
import time

def uploadFile(file, roll, course):
	url = 'http://172.16.115.76/upload.php'
	files = {'fileToUpload': open(file, 'rb')}
	data = {'roll':roll, 'course':course}
	r = requests.post(url, files=files, data=data)
	if r.text == "Ok":
		print "Your file has been uploaded successfully!"
	else:
		print "error while uploading"

def listUploads(course):
	url = 'http://172.16.115.76/listfiles.php'
	data = {'course':course}
	r = requests.post(url, data=data)
	# print r.text
	files = r.text.split("\n")[:-1]
	icondir = 'icons/'
	fileicons = os.listdir(icondir)
	uploadedby = []
	filename = []
	icons = []
	uploadTime = []
	for i in range(0,len(files),2):
		uploadedby.append(files[i][:9])
		filename.append(files[i][9:])
		realTime = time.asctime(time.localtime(int(files[i+1])))
		uploadTime.append(str(realTime))
		flag = 0
		for icon in fileicons:
			if files[i].split('.')[-1] in icon.split('.')[0]:
				flag = 1
				icons.append(icondir+icon)
				break
		if flag is 0:
			icons.append(icondir+'default.png')
	return icons, filename, uploadedby, uploadTime


def downloadFile(filename, filepath, course, roll):
	url = 'http://172.16.115.76/download.php'
	data = {'course':course, 'file':filename, 'roll':roll}
	r = requests.post(url, data=data)
	print r.text
	with open(filepath+'/'+filename, 'wb') as f:
		f.write(r.content)
	print "Yayy!"

# downloadFile('EZ.txt', '/home/maulik/Desktop/test', 'CS203', '140101063')
# listUploads("CS203")
# uploadFile('exam.py')