import urllib2 
import re 
import time 
from bs4 import BeautifulSoup 
  
#myURL = "http://www.biblegateway.com/passage/?search=Genesis+1&version=ASV" 
myURL = "http://www.biblegateway.com/passage/?search=Genesis+1&version=KJ21"
#myURL = "http://www.biblegateway.com/passage/?search=Genesis+1&version=CEB" 
myRoot = "http://www.biblegateway.com/"
  
start = time.clock() 
  
response = urllib2.urlopen(myURL) 
page_source = response.read() 
soup = BeautifulSoup(page_source) 
  
myText = open("theText.txt","wb") 
fuText = soup.findAll(attrs={'class':'heading passage-class-0'}) 
#print fuText[0].text 
myText.write(fuText[0].text.encode('utf8') + "\n") 
  
print fuText[0].text 
  
fuText = soup.findAll("span", attrs={'class':re.compile('text')}) 
for i in fuText: 
  
    print i.text 
  
    myText.write(i.text.encode('utf8') + "\n") 
myText.close() 
  
nextPage = soup.find_all(href=re.compile("/passage"), text = ">") 
  
while (len(nextPage) != 0): 
    nextURL = myRoot + nextPage[0]["href"] 
    response = urllib2.urlopen(nextURL) 
    page_source = response.read() 
    soup = BeautifulSoup(page_source) 
  
    myText = open("theText.txt","a") 
    fuText = soup.findAll(attrs={'class':'heading passage-class-0'}) 
    myText.write(fuText[0].text.encode('utf8') + "\n") 
  
    print fuText[0].text 
  
    fuText = soup.findAll("span", attrs={'class':re.compile('text')}) 
    for i in fuText: 
        myText.write(i.text.encode('utf8') + "\n") 
  
        print i.text 
  
    myText.close() 
    nextPage = soup.find_all(href=re.compile("/passage"), text = ">") 
  
end = time.clock() 
print "Done!"
print "Time cost is " + str(end - start)