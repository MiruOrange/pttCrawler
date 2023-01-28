# pttCrawler
我在樹莓派上搭載這個專案，定時自動執行程式進行資料爬取、資料庫存取，最後篩選後再進行自動信件報告。</br>
算是我自己的一個資訊助手，可以無痛進行ptt爬蟲及資料篩選，成果如下圖。</br>
如果有想要再進行客製化的，可以聯繫我 mafiahsu0.1@gmail.com
![image](https://user-images.githubusercontent.com/109893487/215242577-f55cc891-783f-4a41-ba2d-0c24f3cd0aa9.png)


## 檔案介紹
* 必須額外安裝 requests 及bs4模組，可用右方指令下載 : 'pip install 模組名稱'
* main.py
  * 功能介紹
    * 設定要爬取的版面
    * 設定要爬取的頁數
    * 將爬取的資料存入sqlite資料庫中
  * 引用了craler.py的模組進行了其它工作，使用者不用去理會，如果有興趣再往下看。
  * 基本上只要把要爬的版網址新增進去，再把頁數設定好就可以執行了。
  * 資料夾就會自動產生一個ptt.db的資料庫，可用各家資料庫軟體打開來查看，或在程式中用sqlite3的模組取出來查看內容。
  ![image](https://user-images.githubusercontent.com/109893487/215240970-5f34e07b-6fb2-4269-b88a-77542e99cbd0.png)
* sendMail.py
  * 功能介紹
    * 決定要從資料庫撈哪幾個版的文章寄給自己
    * 相關設定要到mailSetting.py檔案中去做修正
    
    ![image](https://user-images.githubusercontent.com/109893487/215242228-271d59dc-42df-4d64-9509-b7f2575e3854.png)

* mailSetting.py
  * setKeyWords(boardName)方法：
    * 針對不同的版，可以設定不同的關鍵字。
    * 範例中是我自己設定的客製化關鍵字。
    
    ![image](https://user-images.githubusercontent.com/109893487/215242308-ac731a5d-1457-4c17-9d06-d22e44655933.png)
  * sendMail(boardName)方法：
    * 根據關鍵字從資料庫撈取資料，放入send_message()方法中去做寄送
    
    ![image](https://user-images.githubusercontent.com/109893487/215242345-5e9fa3e9-b69c-48d5-af97-bedf23cba6ef.png)
  * send_message(contentList, boardName)方法：
    * 設定寄件者信箱、寄件者密碼、收件人信箱，並把從資料庫中撈出的資料整理成html信件
    
    ![image](https://user-images.githubusercontent.com/109893487/215242426-5353e51b-ad0d-483b-984c-d11f7c63bc84.png)
    ![image](https://user-images.githubusercontent.com/109893487/215242450-3f96708d-3edd-42cc-b52d-c54841c55b7e.png)

* crawler.py
  * 此專案的核心模組
  * 功能介紹
    * 使用了requests 及 bs4第三方模組
    * __init__(self, url, pages, name)方法：
      * 為此模組的建構子
      * url，為目標版面的網址
      * pages，為指定要爬取的頁數
      * name，為表單的名稱
 
      ![image](https://user-images.githubusercontent.com/109893487/215241542-83ef66ad-357c-46b0-b8d2-94ac6ff95a40.png)
    * getWebSoup(self)方法:
      * 設定年滿18歲的cookies
      * 登入所指定的版面網址
      * 取得soup物件
      
      ![image](https://user-images.githubusercontent.com/109893487/215241547-d50ec191-9bad-49d3-8e2b-e7d4ddd63af2.png)
    * parseSoupObject(self, soup)方法：
      * 將soup物件進行解析
      * 找出文章的title(標題)、url(網址)、author(作者)、pushAmount(推文數)、issueYear(發文年)、issueMonth(發文月)、issueDay(發文日)
      * 將找到的文章存到self.articles串列中，以字典方式存放。
      
      ![image](https://user-images.githubusercontent.com/109893487/215241691-90084d06-688c-4368-afcf-7a0dc0cedb38.png)
    * getUrl(self, soup)方法:
      * 在版面抓取'上頁'的網址
      * 如此一來，在抓完當下的頁面後，就可再繼續到'上頁'的網站去爬取
      
      ![image](https://user-images.githubusercontent.com/109893487/215241788-d1861452-4a76-4540-8241-5de4e84e3892.png)
    
    * getPagesData(self)方法:
      * 在這裡以for迴圈去爬取指定的頁數
      * 如，設定pages為4，則會爬取4個頁面
      
      ![image](https://user-images.githubusercontent.com/109893487/215241880-39d330cc-19ff-48f2-90d8-62815e3b242b.png)
     
    * createDbTables(self, db)方法:
      * 傳入database，建立指定的table名稱
      * table有8個欄位，id是自動增加，其餘皆是TEXT
      
      ![image](https://user-images.githubusercontent.com/109893487/215241958-c32d4aef-d706-47a7-8022-981c92f7c4f9.png)
    
    * saveData(self, db)方法:
      * 傳入database，將爬到的文章與資料庫中資料做比對，重複的就不存入。
      * 篩選的機制有二：
        1. 文章title不存在資料庫中，則存入。
        2. 如果title已存在資料庫中，再比對author是否相同。不相同，則存入。
        
        ![image](https://user-images.githubusercontent.com/109893487/215242107-a9dd64e0-5c8d-4da0-be45-b65edae8ee6a.png)





    
