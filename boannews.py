import newsMain
from sqlite3 import connect,IntegrityError
from datetime import datetime

nc = newsMain.newsCrawler()
scrap = nc.setSoup("https://www.boannews.com/media/t_list.asp")

body=nc.CSS_selector("div.news_list",scrap)
for b in body:
    t_headline=nc.CSS_selector("span.news_txt",b)[0].string #제목
    for f in nc.searchFilter:   #키워드 필터링
        try:
            if f in t_headline:
                t_content=nc.CSS_selector("a:nth-of-type(2)",b)[0].string   #간추린 내용
                href=nc.hrefExtract(str(nc.CSS_selector("a:nth-of-type(2)",b)[0]))
                t_newsLink="https://www.boannews.com"+href.split('"')[1]    #본문링크

                conn = connect(nc.getDBPath()) 
                cur = conn.cursor()
                sql = "INSERT INTO news_news_table(headline, link, content, newsTime, origin) values (?,?,?,?,?)"
                cur.execute(sql,(t_headline,t_newsLink,t_content,datetime.now(),"보안뉴스"))
                conn.commit()
                conn.close()
                break

        except IntegrityError as e:
                pass