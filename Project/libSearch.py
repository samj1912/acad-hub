import requests
from bs4 import BeautifulSoup as bs

def splitAndJoin(text):
	return " ".join(text.split()).rstrip().lstrip()

def libgenSearch(book):
	return "None"
	name = book[0]
	author = book[1]
	url = "http://gen.lib.rus.ec/search.php?req="+name+" "+author+"&open=0&view=simple&phrase=1&column=def"
	source_code = requests.get(url)
	plain_text = source_code.text

	soup = bs(plain_text, "lxml")
	table = soup.find('table', {'class':'c'})
	link = table.find('a', {'id':1})
	if link is None:
		return "None"

	url = "http://gen.lib.rus.ec/"+link['href']
	soup = bs(requests.get(url).text, "lxml")
	table = soup.find('table')
	link = table.find('a')
	
	soup = bs(requests.get(link['href']).text,"lxml")
	table = soup.find('table')
	link = table.find('a')
	return "http://libgen.io"+link['href']

def librarySearch(book):
	name = book[0]
	author = book[1]
	url = "http://bidya.iitg.ernet.in:8680/opac/search/searchResult.html?searchdata="+name+"&qcon1=1&cat1=1&con1=1&searchdata2="+author+"&qcon2=1&cat2=0&con2=1&searchdata3=&qcon3=1&cat3=7&docType=BK&fromTF1=&toTF1=&sortBy=-1&level1=&physicalForm1=&sourceTF1=&subjectCode1=&subjectDocType1=&locationTF1=&db=8&databaseList=&search_selectedSites=1"

	soup = bs(requests.get(url).text,"lxml")
	bookdiv = soup.find('div', {'class':'recordObjectDiv'})
	if bookdiv is None:
		return "None"

	bookInfo = bookdiv.findAll('p')
	return splitAndJoin(bookInfo[2].text)

# librarySearch(["Digital Design", "M Mano"])