class Page:

	dataTypes = {"version" : "text", "book" : "text", 
	"date" : "int", "verse" : "int", "line" : "text"}

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
		for verseNum in verses:
			contentDict = {"version" : version, 
						   "book" : book, 
						   "chapter": chapter, 
						   "verse" : verseNum,
						   "line" : verses[verseNum]}
			dictList.append(contentDict)
		return dictList	