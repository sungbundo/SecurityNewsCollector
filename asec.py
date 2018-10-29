import newsMain
from sqlite3 import connect,IntegrityError
from datetime import datetime


nc = newsMain.newsCrawler()
scrap = nc.setSoup("http://asec.ahnlab.com/category")
body=nc.CSS_selector("div#content > div#searchList > ol > li",scrap)

for b in body:
    t_headline=nc.CSS_selector("a",b)[0].string.strip()    #제목
    for f in nc.searchFilter:   #키워드 필터링
        try:
            if f in t_headline:
                href=nc.hrefExtract(str(b))
                t_newsLink="http://asec.ahnlab.com"+href.split('"')[1]    #본문링크

                conn = connect(nc.getDBPath()) 
                cur = conn.cursor()
                sql = "INSERT INTO news_news_table(headline, link, content, newsTime, origin) values (?,?,?,?,?)"
                cur.execute(sql,(t_headline,t_newsLink,"-",datetime.now(),"안랩ASEC"))
                conn.commit()
                conn.close()
                break

        except IntegrityError as e:
                pass