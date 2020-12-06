from bs4 import BeautifulSoup as bs
from xlwt import Workbook

content=[]

workbook=Workbook()
sheet=workbook.add_sheet("Sheet1")

for i in range (701,801):
    fileName='0'+str(i)
    
    with open(f"articles/{fileName}.xml",encoding="utf8") as file:
        content=file.read()
        Content=bs(content,"lxml")
        sheet.write(i-1,3,str(Content.find("title"))[7:-8])
        sheet.write(i-1,4,str(Content.find("maintext"))[10:-11])


workbook.save("demo corpus.xls")