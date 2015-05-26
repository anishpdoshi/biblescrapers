#By Anish Doshi, 2/21/14. Uses beautiful soup 
#(http://www.crummy.com/software/BeautifulSoup/bs4/doc/)

from bs4 import BeautifulSoup
import webbrowser
import urllib2
import csv


def writeCSV(d):
	write = csv.writer(open("bibledict.csv", "a"))
	for key, val in d.items():
		try:
			write.writerow([key, val])
		except:
			write.writerow([key, val.encode('utf-8')])
	write.writerow(["end", "line"])

def readCSV():
	read = csv.reader(open("bibledict.csv"))
	dictList = []
	tempDict = {}
	for key, val in read:
		if not key == "end":
			if key == "chapter" or key == "verse" or key == "date":
				tempDict[key] = int(val)
			else:
				tempDict[key] = val.decode("unicode_escape").encode("ascii", "ignore")
		else:
			dictList.append(tempDict)
			tempDict = dict()
	return dictList


class Page:

	dataTypes = {"version" : "text", "book" : "text", 
	"chapter" : "int", "verse" : "int", "line" : "text", "date" : "int"}
	staticIndex = 1

	def __init__(self, version, book, chapter, verses, url):
		self.version = version
		self.book = book
		self.chapter = chapter
		self.verses = verses
		self.url = url

	def unify_verses(self, single_line=True):
		if (single_line):
			for verse in self.verses:
				line = ""
				for word in self.verses[verse]:
					line += word + " "
				self.verses[verse] = line[:len(line) - 1]
		else:
			body = ""			
			for verse in self.verses:
				for word in self.verses[verse]:
					body += word + " "
				body += "\n"
			return body

	def text_write(self, name):
		text = open(name, 'a')
		text.write(self.url + "\n")
		text.write(self.version + "\n")
		text.write(self.book + " " + str(self.chapter) + "\n\n")
		for verse in self.verses:
			
			decoded = self.verses[verse].encode('utf-8')
			text.write(str(verse) + ": " + decoded + "\n")
		text.close()

	def exportData(self):
		dictList = []
		for verseNum in self.verses:
			#print self.verses[verseNum]
			#self.verses[verseNum].encode('utf-8')
			#print(self.verses[verseNum])
			contentDict = {"version" : self.version, 
						   "book" : self.book, 
						   "chapter": self.chapter, 
						   "verse" : verseNum,
						   "line" : self.verses[verseNum],
						   "date" : Page.staticIndex * 3600 * 24}
			Page.staticIndex += 1
			#writeCSV(contentDict)
			dictList.append(contentDict)
		return dictList	

site = "http://www.biblegateway.com"

def openURL(url):
	response = urllib2.urlopen(url)
	html = response.read()
	return BeautifulSoup(html)

def createPage(url):
	tree = openURL(url)
	# tree = BeautifulSoup(html)
	verseDict = {}
	first = True;
	for verse in tree.find_all('p', class_="verse"):
		rawtext = verse.span.text.encode('ascii','ignore')
		#noPunc = rawtext.replace("\"", "").replace(",", "").replace(".", "")
		letterIndex = 0
		while (rawtext[letterIndex].isdigit()):
			letterIndex += 1
		textList = rawtext[letterIndex:]
		if first:
			verseDict[1] = textList
			first = False
		else:
			verseNum = int(rawtext[:letterIndex])
			verseDict[verseNum] = textList
	titleInfo = tree.find('div', class_="heading passage-class-0")
	bookInfo = titleInfo.h3.text.split()
	if (len(bookInfo) == 3):
		bookInfo = [bookInfo[0] + " " + bookInfo[1], bookInfo[2]]
	elif (len(bookInfo) == 4):
		bookInfo = [bookInfo[0] + " " + bookInfo[1] + " " + bookInfo[2], bookInfo[3]];
	print("Successfully created " + bookInfo[0] + " - " + bookInfo[1])
	version = titleInfo.p.text.encode('ascii', 'ignore')
	book = bookInfo[0].encode('ascii', 'ignore')
	p = Page(version, book, int(bookInfo[1]), 
		verseDict, url)
	#p.unify_verses()
	#p.text_write("data.txt")
	return p

def harvestEnglishLinks():
	versionsTree = openURL("http://www.biblegateway.com/versions/")
	versionsTable = versionsTree.find('table', class_="infotable")
	englishSection = versionsTable.find('td', text="English (EN)").parent
	englishVersions = [site + 
	"versions/21st-Century-King-James-Version-KJ21-Bible/"]
	englishSection = englishSection.next_sibling
	i = 20
	try:
		while (not englishSection.td.has_attr("rowspan")):
			#print(englishSection)
			englishVersions.append(site + englishSection.td.a.get('href'))
			if (i > 0):
				webbrowser.open(site + englishSection.td.a.get('href'))
				i -= 1
			englishSection = englishSection.next_sibling
	except Exception as e:
		pass;
	return englishVersions

def adaptiveScrape(url):
	tree = openURL(url)
	linkTable = linkTree.find('table', class_="infotable " + 
		"chapterlinks updatepref")
	count = 100
	for link in linkTable.find_all("a"):
		if (count > 0):
			address = link.get('href')
			adaptivePage(site + address)
			count -= 1
		
#BibleVersion: text
#BookName: text
#BookChapter: text
#VerseNum: int
#VerseLine: text
def adaptivePage(url):
	return "lol"                              

def kingjames():
	pages = []
	linkTree = openURL("http://www.biblegateway.com/" +
		"versions/21st-Century-King-James-Version-KJ21-Bible/")
	# linkTree = BeautifulSoup(linkRaw)
	linkTable = linkTree.find('table', class_="infotable " + 
		"chapterlinks updatepref")
	count = 50
	for link in linkTable.find_all("a"):
		if (count > 0):
			address = link.get('href')
			pages.append(createPage("http://www.biblegateway.com" + address))
			count -= 1
		else:
			break
	#print(readCSV())
	return pages



#createPage("http://www.biblegateway.com/passage/?search=1+Samuel+1&version=KJ21")
#kingjames()
#harvestEnglishLinks()