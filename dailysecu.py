import newsMain
from sqlite3 import connect,IntegrityError
from datetime import datetime

nc = newsMain.newsCrawler()
scrap = nc.setSoup("http://www.dailysecu.com/?mod=news&act=articleList&view_type=S&sc_code=")

body=nc.CSS_selector("div.box",scrap)
for b in body:
    t_headline=nc.CSS_selector("a.title_a",b)[0].string
    for f in nc.searchFilter:   #키워드 필터링
        try:
            if f in t_headline:
                t_content=nc.CSS_selector("a.summary_a",b)[0].string   #간추린 내용
                href=nc.hrefExtract(str(nc.CSS_selector("a.summary_a",b)[0]))
                t_newsLink="http://www.dailysecu.com"+href.split('"')[1]    #본문링크

                conn = connect(nc.getDBPath()) 
                cur = conn.cursor()
                sql = "INSERT INTO news_news_table(headline, link, content, newsTime, origin) values (?,?,?,?,?)"
                cur.execute(sql,(t_headline,t_newsLink,t_content,datetime.now(),"데일리시큐"))
                conn.commit()
                conn.close()
                break

        except IntegrityError as e:
                pass