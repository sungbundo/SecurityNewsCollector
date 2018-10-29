from bs4 import BeautifulSoup 
import urllib.request as req
import re
import os

class newsCrawler():
    def setSoup(self,site):
        res=req.urlopen(str(site))
        soup=BeautifulSoup(res,"html.parser")
        return soup
    
    def CSS_selector(self,selector,soup):
        result=soup.select(selector)
        return result
    
    def hrefExtract(self,context):
        p = re.compile('href=".*"')
        searchResult = p.search(context)
        href=searchResult.group()
        return href
    
    def getJobPath(self):
        return os.path.dirname(os.path.realpath(__file__))
    
    def getDBPath(self):
        return self.getJobPath()+"/../db.sqlite3"
    
    searchFilter=["디도스","우회","해킹","취약점","패치","악성","다크웹","유출","도용","백도어","익스플로잇","버그","패치","GandCrab","갠드크랩","탈취","감염",
    "제로데이","피싱","파밍","랜섬","CVE","동향","바이러스","웜","트로이","원격","디페이스","민감정보","개인정보","사이버공격"]