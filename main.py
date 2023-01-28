from crawler import PttCrawler
import sqlite3

#連結資料庫，如果沒有該資料庫，則會建立一個新的
pttDB = sqlite3.connect('ptt.db')

#建立物件串列，設定網址及爬取的頁數
objectList = [
    PttCrawler('https://www.ptt.cc/bbs/Gossiping/index.html', 4, 'gossip'),         #八掛版
    PttCrawler('https://www.ptt.cc/bbs/job/index.html', 4, 'job'),                  #工作版
    PttCrawler('https://www.ptt.cc/bbs/part-time/index.html', 4, 'partTime'),       #打工版
    PttCrawler('https://www.ptt.cc/bbs/Actuary/index.html', 4, 'actuary'),          #精打細算版
    PttCrawler('https://www.ptt.cc/bbs/Tech_Job/index.html', 4, 'tech_job'),        #科技業工作版
    PttCrawler('https://www.ptt.cc/bbs/give/index.html', 4, 'give')                 #give版
    ]

#將資料存到資料庫
articleData = []
tableNameList = []
for obj in objectList:
    obj.getPagesData()                  #取得指定網頁的資料，並爬取指定次數
    articleData.append(obj.articles)    #存放每個版的文章資料
    tableNameList.append(obj.name)      #存放每個版的文章標題，用來建立或撈取表單
    obj.createDbTables(pttDB)           #依照每個版的版名創建表單
    obj.saveData(pttDB)                 #將撈取的資料比對後，將未重複的文章放入資料庫
pttDB.close()                           #關閉資料庫