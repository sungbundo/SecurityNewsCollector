import newsMain
from sqlite3 import connect,IntegrityError
from datetime import datetime

nc = newsMain.newsCrawler()
scrap = nc.setSoup("https://www.krcert.or.kr/main.do")
body=nc.CSS_selector("div#totalNewsPC > div.inbox > ul > li",scrap)

for b in body:
        t_headline=nc.CSS_selector("a",b)[0].string    #제목
        if(t_headline==None):
                t_headline=nc.CSS_selector("strong",b)[0].string        #새글이 올라오면 strong태그가 달림
        t_headline=t_headline.strip()
        for f in nc.searchFilter:   #키워드 필터링
                try:
                        if f in t_headline:
                                href=nc.hrefExtract(str(b))
                                t_newsLink="https://www.krcert.or.kr"+href.split('"')[1]    #본문링크

                                conn = connect(nc.getDBPath()) 
                                cur = conn.cursor()
                                sql = "INSERT INTO news_news_table(headline, link, content, newsTime, origin) values (?,?,?,?,?)"
                                cur.execute(sql,(t_headline,t_newsLink,"-",datetime.now(),"KrCERT"))
                                conn.commit()
                                conn.close()
                                break

                except IntegrityError as e:
                        pass
                