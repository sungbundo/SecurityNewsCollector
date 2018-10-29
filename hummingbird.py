import newsMain
from sqlite3 import connect,IntegrityError
from datetime import datetime

nc = newsMain.newsCrawler()
scrap = nc.setSoup("https://hummingbird.tistory.com/")
body=nc.CSS_selector("div#ttItem1400418536 > ul > li",scrap)

for b in body:
    t_headline=nc.CSS_selector("div > p.tt-post-title > a",b)[0].string.strip()    #제목
    for f in nc.searchFilter:   #키워드 필터링
        try:
            if f in t_headline:
                t_content=nc.CSS_selector("div > p.tt-post-summary > a",b)[0].string.strip()   #간추린 내용
                href=nc.hrefExtract(str(b))
                t_newsLink="https://hummingbird.tistory.com"+href.split('"')[1]    #본문링크

                conn = connect(nc.getDBPath()) 
                cur = conn.cursor()
                sql = "INSERT INTO news_news_table(headline, link, content, newsTime, origin) values (?,?,?,?,?)"
                cur.execute(sql,(t_headline,t_newsLink,t_content,datetime.now(),"울지않는 벌새"))
                conn.commit()
                conn.close()
                break

        except IntegrityError as e:
                pass

                