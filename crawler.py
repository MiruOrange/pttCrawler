import requests
from bs4 import BeautifulSoup
from datetime import datetime

class PttCrawler():
    def __init__(self, url, pages, name):
        self.url = url
        self.articles = []                   #文章陣列
        self.pages = pages
        self.name = name
    
    def getWebSoup(self):
        cookies = {'over18':'1'}
        htmlFile = requests.get(self.url, cookies= cookies)    
        soup = BeautifulSoup(htmlFile.text, 'lxml')
        return soup

    #將文章內容資訊截取出來
    def parseSoupObject(self, soup):
        articleData = soup.select('.r-ent')
        for article in articleData:
            if article.find('a') !=None:        #文章被刪除時，標題會變None，所以要加此判斷式
                title = article.find('a').text
                url = article.find('a')['href']
                author = article.find('div', 'author').text
                pushAmount = article.find('div', 'nrec').text
                issueDateList = article.find('div', 'date').text.strip().split('/')
                issueMonth = issueDateList[0]
                if issueMonth == '12' or issueMonth == '11':    #因為是年末，所以加上這個設定
                    issueYear = str(datetime.now().year-1)
                else:
                    issueYear = str(datetime.now().year)
                issueDay = issueDateList[1]
                self.articles.append({                  #self.articles陣列存放字典資料
                    'author':author,
                    'title':title, 
                    'push':pushAmount,
                    'year':issueYear,
                    'month':issueMonth,
                    'day':issueDay,
                    'url' :'https://www.ptt.cc'+url
                })

    #<div class="btn-group btn-group-paging">
    #尋找'上頁'的網址
    def getUrl(self, soup):
        self.url = 'https://www.ptt.cc'+soup.find('div', 'btn-group btn-group-paging').select('a')[1]['href']
    
    #依照指定的頁數(pages)爬取網頁
    def getPagesData(self):
        for i in range(self.pages):
            soup = self.getWebSoup()
            self.parseSoupObject(soup)
            self.getUrl(soup)
    
    #依照指定的表單名稱建立網頁(name)
    def createDbTables(self,db):
        sql = f'''
        CREATE TABLE IF NOT EXISTS {self.name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT, 
            title TEXT,
            url TEXT,
            push TEXT,
            year TEXT,
            month TEXT,
            day TEXT
        )
        '''
        db.execute(sql)
    
    # 在這裡建立篩選機制，將不存在資料庫的文章放入資料庫
    # 比對的機制有二：
    # 1.文章title不存在資料庫中，則存入。
    # 2.文章title存在資料庫中，再比對其author是否相同，不相同，則存入。
    # 理由是同一個文章由同一個人發布的，沒有存下的價值。
    def saveData(self, db):
        #第一步，從資料庫撈取文章資料，把title和author分開存放，準備用來比對
        articleTitleList = []
        authorList = []
        selectSql = "SELECT author, title FROM {}"  #括號中準備放入各表單名稱
        sql = selectSql.format(self.name)           #取出表單名稱name放入
        selectDatas = db.execute(sql).fetchall()
        for data in selectDatas:                    #把文章標題和作者放入不同list準備比較
            authorList.append(data[0])
            articleTitleList.append(data[1])
        #第二步，進行比對
        for article in self.articles:                   #self.articles陣列內以字典存放每一筆文章
            if article['title'] not in articleTitleList:#如果新的文章標題不在資料庫文章標題list中
                addSql = "INSERT INTO {} (author, title, url, push, year, month, day) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                sql = addSql.format(self.name, article['author'], article['title'], article['url'], article['push'],article['year'] , article['month'], article['day'])
                db.execute(sql)
                db.commit()
            #如果在文章標題列表中，但作者不同，一樣存起來
            else:
                if article['author'] not in authorList:  #判斷作者是否存在作者列表中
                    addSql = "INSERT INTO {} (author, title, url, push, year, month, day) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                    sql = addSql.format(self.name, article['author'], article['title'], article['url'], article['push'],article['year'] , article['month'], article['day'])
                    db.execute(sql)                         #執行sql語法
                    db.commit()                             #表單內容有修正，都必須commit()一次
