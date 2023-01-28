from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3

def setKeyWords(boardName):
    jobKeyWords = [
        '台中', '大學', '高中', '國中', '國小', '學校', 
        '中部', '全國', '不分區', '全區', '多區', '日本', '大阪', '東京'
    ]
    partTimeKeyWords = [
        '台中', '臺中', '中部', '全國', '不分區', '全區', '多區'
    ]
    actuaryKeyWords = [
        '情報', '台中', '臺中', '中部', '百貨', '多區', '不分區', '全區',
    ]
    techJobKeyWords = [
        '徵人', '台中', '中部'
    ]
    giveKeyWords = [
        '台中', '臺中', '中部', '彰化', '南投', '苗栗'
    ]
    if boardName == 'job':
        return jobKeyWords
    elif boardName == 'partTime':
        return partTimeKeyWords
    elif boardName == 'actuary':
        return actuaryKeyWords
    elif boardName == 'tech_job':
        return techJobKeyWords
    elif boardName == 'give':
        return giveKeyWords
    
#在此進行關鍵字篩選，從資料庫撈出所需資料
#將該資料放入send_message()函數中進行寄送
def sendMail(boardName):
    #連結資料庫
    # path = 'database/ptt.db'
    pttDB = sqlite3.connect('ptt.db')

    #設定關鍵字
    keyWords = setKeyWords(boardName)

    #從資料庫中撈出資料取得信件內容
    #sql語法分成front, middle及end三段，front及end內容沒有變化
    #middle段的內容，隨著keyWord的內容而增減
    sqlFront = f'SELECT * FROM {boardName} WHERE title '
    sqlMiddle = ''
    for i in range(len(keyWords)):
        if i<(len(keyWords)-1):
            sqlMiddle += f"LIKE '%{keyWords[i]}%' OR title "
        else:
            sqlMiddle += f"LIKE '%{keyWords[i]}%'"
    sqlEnd = " order by year DESC, month DESC, day DESC;"
    sql = sqlFront+ sqlMiddle+sqlEnd
    mailcontent = pttDB.execute(sql)    
    send_message(mailcontent, boardName+'版')

# 1.郵件相關設定
# 2.傳入的郵作內容與html信件內容結合
# 3.傳入的boardName可修改信件標題
def send_message(contentList, boardName):
    strSmtp = 'smtp.gmail.com:587'
    mailfrom = 'Sender Gmail Account(寄件者gmail信箱)'
    mailpw = 'Your App Password(應用程式密碼，可參考: https://www.youtube.com/watch?v=Qre7EbYfXis)'
    mailto = 'Receiver Mail Account(收件者信箱)'
    #取得現在時間
    nowTime = datetime.now()
    nowHour = nowTime.hour      #現在幾點
    nowMonth = nowTime.month    #現在幾月
    nowDay = nowTime.day        #現在幾日
    mailsubject = f'資訊小幫手-{boardName}{nowMonth}月{nowDay}日{nowHour}時報告'

    #寄送html信件內容
    msg = MIMEMultipart('alternative')  
    msg['Subject'] = mailsubject        #加上郵件標題
    textContent = ''
    for content in contentList:
        textContent += f"{content[6]}/{content[7]}, <a href='{content[3]}'>{content[2]}</a><br><br>"
    htmlContent = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        {textContent}
    </body>
    </html>
    '''
    mailContent = MIMEText(htmlContent, 'html') 
    msg.attach(mailContent)

    mailto = mailto
    server = SMTP(strSmtp)
    server.ehlo()                   #跟主機溝通
    server.starttls()               #TTLS安全認證
    server.login(mailfrom, mailpw)    
    server.sendmail(mailfrom, mailto, msg.as_string())