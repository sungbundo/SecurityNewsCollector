import newsMain
from sqlite3 import connect,IntegrityError
from datetime import datetime

nc = newsMain.newsCrawler()
scrap = nc.setSoup("http://www.etnews.com/news/section.html?id1=04&id2=045")

body=nc.CSS_selector("ul.list_news > li > dl",scrap)
for b in body:
    t_headline=nc.CSS_selector("dt",b)[0].string    #제목
    for f in nc.searchFilter:   #키워드 필터링
        try:
            if f in t_headline:
                t_content=nc.CSS_selector("dd.summury",b)[0].string   #간추린 내용
                href=nc.hrefExtract(str(nc.CSS_selector("dt",b)[0]))
                t_newsLink=href.split('"')[1]    #본문링크

                conn = connect(nc.getDBPath()) 
                cur = conn.cursor()
                sql = "INSERT INTO news_news_table(headline, link, content, newsTime, origin) values (?,?,?,?,?)"
                cur.execute(sql,(t_headline,t_newsLink,t_content,datetime.now(),"전자신문"))
                conn.commit()
                conn.close()
                break

        except IntegrityError as e:
                pass



                