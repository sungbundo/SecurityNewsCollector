import newsMain
from sqlite3 import connect,IntegrityError
from datetime import datetime

nc = newsMain.newsCrawler()
scrap = nc.setSoup("https://www.hauri.co.kr/security/issue.html")
body=nc.CSS_selector("div.column.bbs-title",scrap)

for b in body:
    t_headline=nc.CSS_selector("strong",b)[0].string.strip()    #제목
    for f in nc.searchFilter:   #키워드 필터링
        try:
            if f in t_headline:            
                href=nc.hrefExtract(str(b))
                t_newsLink="https://www.hauri.co.kr/security/"+href.split('"')[1]    #본문링크

                conn = connect(nc.getDBPath()) 
                cur = conn.cursor()
                sql = "INSERT INTO news_news_table(headline, link, content, newsTime, origin) values (?,?,?,?,?)"
                cur.execute(sql,(t_headline,t_newsLink,"-",datetime.now(),"하우리"))
                conn.commit()
                conn.close()
                break

        except IntegrityError as e:
                pass
                