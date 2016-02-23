import requests
from bs4 import BeautifulSoup
from libSearch import libgenSearch
import string 

def stripAll(text):
	strippedText = ''.join(text.split())
	return strippedText

def splitAndJoin(text):
	return " ".join(text.split()).rstrip().lstrip()

def removePunc(text):
	for c in string.punctuation:
		text = text.replace(c, "")
	return text.replace("and", "")

def getBooks(row):
	para = row.findAll('p')

	bookPos = len(para)
	referencePos = len(para)
	for i in range(len(para)):
		if "Texts" in para[i].text:
			bookPos = i
			break
	for i in range(len(para)):
		if "References" in para[i].text:
			referencePos = i
			break


	books = []
	for i in range(bookPos+1, referencePos):
		if stripAll(para[i].text) != "":
			books.append(para[i])

	ref = []
	for i in range(referencePos+1, len(para)):
		if stripAll(para[i].text) != "":
			ref.append(para[i])
	return (books, ref)

def getCourseBooks(courses, soup):
	tables = soup.findAll('table', {'class':'MsoTableGrid'})
	rows = []
	for table in tables:
		rows += table.findAll('tr')

	strippedRows = []
	for row in rows:
		strippedRows.append(stripAll(row.text))

	courseBooks = []
	for course in courses:
		# print course
		# print courses[course]["code"]
		# print courses[course]["L"]
		# print courses[course]["T"]
		# print courses[course]["P"]
		# print courses[course]["C"]
		for i in range(len(rows)):
			if courses[course]["code"] != "" and courses[course]["code"] in strippedRows[i][:10]:
				books, ref = getBooks(rows[i])

				for book in books:
					name = book.find('i')	
					try:
						title = name.text
					except:
						continue
					title = splitAndJoin(title)

					row = splitAndJoin(book.text)
					pos = row.find(title)

					author = row[3:pos-2]
					pub = row[pos+len(title)+1:]
					# print title + "\t" + author + "\t" + pub
					downloadLink = libgenSearch([removePunc(title), removePunc(author)])
					courseBooks.append((course, courses[course]["code"], title, author, pub, downloadLink))
				 
				break
	# print courseBooks
	return courseBooks



def showBooks(dept, sem):
	sem = int(sem)
	url = "http://shilloi.iitg.ernet.in/~acad/intranet/CourseStructure/"+dept.lower()+"UG2013onwards.htm"
	source_code = requests.get(url)
	plain_text = source_code.text

	soup = BeautifulSoup(plain_text, "lxml")

	table = soup.find('table', {'class':'MsoNormalTable'})
	rows = table.findAll('tr')
	semTitleRows=[]
	for i in range(len(rows)):
		text = rows[i].text
		if "Semester" in text:
			semTitleRows.append(i)
			continue
	semTitleRows.append(len(rows))
	
	rowSemEquivalent = sem/2 - (sem+1)%2

	courses = {}

	for i in range(semTitleRows[rowSemEquivalent]+1, semTitleRows[rowSemEquivalent+1]-1):
		td = rows[i].findAll('td')
		info = []
		if sem%2 == 1:
			if stripAll(td[0].text) == "" and stripAll(td[1].text) == "":
				continue
			for j in range(0,6):
				strippedText = splitAndJoin(td[j].text)
				info.append(str(strippedText))
		else:
			if len(td)<=8 or stripAll(td[7].text) == "" and stripAll(td[8].text) == "":
				continue
			for j in range(7,len(td)):
				strippedText = splitAndJoin(td[j].text)
				info.append(str(strippedText))

		info[0] = stripAll(info[0])
		# print info
		courses[info[1]] = {"code":info[0], "L":info[2], "T":info[3], "P":info[4], "C":info[5],}

	return getCourseBooks(courses, soup)

# x=showBooks("CSE", 4)	
# print x