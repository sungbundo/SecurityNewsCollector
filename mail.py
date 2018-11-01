import smtplib
import sqlite3
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_gmail = smtplib.SMTP('smtp.gmail.com', 587)
smtp_gmail.ehlo()
smtp_gmail.starttls()
smtp_gmail.login('ID','PW')	#구글 ID, PW 입력


def newsSentence(row):  #headline, content, link 반복되는 문장
    msg="""
        <p><b>{0}</b></p>
		<p>- {1}</p>
		<p>관련 링크 : <a href="{2}">{2}</a></p>
        <hr style="border: solid 1px;">
        """.format(row[0],row[1],row[2])
    return msg

conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__))+"/../db.sqlite3")
cur = conn.cursor()
now=datetime.datetime.now()
t_year=now.year
t_month=now.month
t_day=now.day
t_dow=now.weekday()  #0:일요일, 1:월요일, 2:화요일, 3:수요일, 4:목요일, 5:금요일, 6:토요일
pastday=(now-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
if (t_dow==1):
    pastday=(now-datetime.timedelta(days=3)).strftime('%Y-%m-%d')

s_today='{0} 09:00'.format(now.strftime('%Y-%m-%d'))    #메일 발송 시간
s_pastday='{0} 09:00'.format(pastday)  #이전 발송 시간

sql="select headline, content, link from news_news_table where newsTime BETWEEN '{0}' AND '{1}'".format(s_pastday,s_today)
cur.execute(sql)
rows = cur.fetchall()
#메일 첫부분
set_news="""\
<html>
	<body>
		<p><span>{0}년 {1}월 {2}일 보안이슈 전달드립니다 참고하시길 바랍니다</p>
		<p>모니터링 현황은 <a href="http://106.10.44.192">여기</a>에서 확인하시기 바랍니다.</p>
		</br>
		<hr style="border: solid 1px;">
        """.format(t_year,t_month,t_day)

for row in rows:
    set_news+=newsSentence(row)

conn.close()

msg=MIMEMultipart('alternative')
msg['Subject']="{0}년 {1}월 {2}일 보안이슈".format(t_year,t_month,t_day)
msg['From']=''	#보내는 사람
msg['To']=''	#받는 사람
mailFrom=''	#보내는 메일 주소
mailTo=('')	#받는 메일 주소
if rows==[]:
	set_news="""\
	<html>
	<p>새로운 뉴스가 존재하지 않습니다.</p>
	<p>모니터링 현황은 <a href="http://106.10.44.192">여기</a>에서 확인하시기 바랍니다.</p>
	</html>
	"""
set_news+='</body></html>'
msg.attach(MIMEText(set_news, 'html', 'utf-8'))
smtp_gmail.sendmail(mailFrom, mailTo, msg.as_string())