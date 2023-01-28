from mailSetting import sendMail
#執行此程式，決定要從資料庫撈出哪些table的資料進行寄送

#把想寄送的版名放入陣列
boardName = ['job', 'actuary', 'partTime', 'tech_job', 'give']

for i in range(len(boardName)):
    sendMail(boardName[i])