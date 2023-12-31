from selenium import webdriver
import os
import time
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.by import By
import pandas as pd
from application import mycursor,mydb
import datetime



class OlxScrapper():
    def __init__(self,searchWord):
        chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--disable-notifications')
        # chromeOptions.add_argument("window-size=1280,800")
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--disable-extensions')
        chromeOptions.add_argument("--user-data-dir=" + os.getcwd() + "\\src\\userdata")
        chromeOptions.add_argument("--disable-plugins-discovery")
        chromeOptions.add_argument("--start-maximized")
        chromeOptions.add_argument('--ignore-certificate-errors')
        chromeOptions.add_argument('--ignore-ssl-errors')
        # For older ChromeDriver under version 79.0.3945.16
        chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
        chromeOptions.add_experimental_option('useAutomationExtension', False)
        # For ChromeDriver version 79.0.3945.16 or over
        chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
        self.browser = webdriver.Chrome(options=chromeOptions)
        self.browser.implicitly_wait(5)
        self.browser.maximize_window()
        self.baseUrl="https://www.olx.com.pk"
        self.searchWord=searchWord


    def loginInOLX(self):
        self.browser.get(self.baseUrl)
        time.sleep(5)
        signInButton=self.browser.find_element(By.CSS_SELECTOR,"._1075545d._17fba712._96d4439a ._1075545d._7d3927ca :only-child").click()
        time.sleep(5)
        loginWithEmail=self.browser.find_element(By.CSS_SELECTOR,".bff16e15._0f49b494 ._1075545d.a67fa1b7._42f36e3b.d059c029._858a64cf  > :nth-child(3)").click()
        # emailInput = self.browser.find_element(By.ID,'email')
        time.sleep(20)
        # emailInput.send_keys("umerpythondevelopment@gmail.com")
        time.sleep(2)
        emailSubmitButton=self.browser.find_element(By.CSS_SELECTOR,".f7d9469e > :nth-child(2)").click()
        time.sleep(3)
        # passwordInput = self.browser.find_element(By.ID, 'password')
        # passwordInput.send_keys("@Raniakhan12345")
        # passwordSubmitButton=self.browser.find_element(By.CSS_SELECTOR,".f7d9469e > :nth-child(3)").click()
        # print(passwordSubmitButton.text)
        # time.sleep(10)

    def extractLinks(self):

        self.browser.get(self.baseUrl)
        searchfield=self.browser.find_element(By.CSS_SELECTOR,"._1075545d._1dc43551 ._45df2c45 ._2cf807e6._828ba44c ._162767a9")
        searchfield.send_keys(searchWord)
        searchSubmit=self.browser.find_element(By.CSS_SELECTOR,"._1075545d._1dc43551 .a3e390b5").click()
        time.sleep(5)
        for count in range(0,5):
            try:
                loadMoreButton=self.browser.find_element(By.CSS_SELECTOR,"._1075545d._96d4439a.d059c029._858a64cf ._95dae89d ._4408f4a8._5d33e436").click()
                time.sleep(3)
                self.browser.execute_script("window.scrollBy(0,1000)")
                time.sleep(2)
                loadMoreButton = self.browser.find_element(By.CSS_SELECTOR,"._1075545d._96d4439a.d059c029._858a64cf ._95dae89d ._4408f4a8._5d33e436").click()
                time.sleep(3)
            except:
                continue
        soup = BeautifulSoup(self.browser.page_source, "lxml")
        allLinks = soup.find_all('a')
        allLinkSet = set()
        for x in allLinks:
            # print(x.get("href"))
            allLinkSet.add(str(x.get("href")))
        # print(allLinkSet)
        allLinkList = list(allLinkSet)
        def filterGenuineAddLinks(alLinkList):
            pattern = "/item/([a-z]*[0-9]*-+)+iid-[0-9]+"
            return re.match(pattern, alLinkList)

        filteredAddLinks = list(filter(filterGenuineAddLinks, allLinkList))
        return filteredAddLinks

    def saveInExcelFile(self,date):
        linksDataFrame=pd.Series(date,name="Links")
        linksDataFrame.to_csv("data/olxAddsLinks.csv",index=False)

    def extractInfoFromLinks(self):
        linkDataFrame=pd.read_csv("data/olxAddsLinks.csv")
        # time.sleep(30)
        infoDF=pd.DataFrame(columns=["Name","PhoneNumber","MemberSince","Address","AddId","Price","Heading"])
        for row in range(0,len(linkDataFrame)):
            newRow={}
            fullLink=self.baseUrl+linkDataFrame.at[row,"Links"]
            # newRow["AddLinks"]=fullLink
            # print(fullLink)
            try:
                self.browser.get(fullLink)
                time.sleep(6)
                try:
                    name=self.browser.find_element(By.CSS_SELECTOR,"._1075545d._96d4439a ._1075545d._6caa7349._42f36e3b.d059c029 ._6d5b4928.be13fe44")
                    time.sleep(5)
                    # print(name.text)
                    newRow["Name"]=name.text
                except:
                    newRow["Name"] = "name Not Found"
                    continue
                try:
                    memberSince=self.browser.find_element(By.CSS_SELECTOR,"._1075545d._96d4439a ._1075545d._6caa7349._42f36e3b.d059c029  ._05330198 ._6d5b4928")
                    time.sleep(3)
                # print(name.text)
                    newRow["MemberSince"]=memberSince.text[13:]

                except:
                    newRow["MemberSince"]="member since not found"
                    continue
                try:
                    address=self.browser.find_element(By.CSS_SELECTOR,"._1075545d._0fe18041 ._25ceab92 ")
                    time.sleep(3)
                # print(name.text)
                    newRow["Address"]=address.text
                except:
                    newRow["Address"]="address not found"
                    continue

                try:
                    adId=self.browser.find_element(By.CSS_SELECTOR,"._1075545d._84d5a753._5f872d11._96d4439a ._171225da")
                    time.sleep(3)
                # print(name.text)
                    newRow["AddId"] = adId.text[6:]
                except:
                    newRow["AddId"] = "no id found"
                    continue
                try:
                    price=self.browser.find_element(By.CSS_SELECTOR,"._1075545d._51680bd1._5f872d11.c96de063 ._1075545d ._56dab877")
                    time.sleep(3)
                # print(name.text)
                    newRow["Price"] = price.text
                except:
                    newRow["Price"] = "no price find"
                    continue
                try:
                    buttonNumber = self.browser.find_element(By.CSS_SELECTOR,".cf4781f0 ._1075545d.d059c029 ._1075545d.b34f9439._42f36e3b._96d4439a._1709dcb4 ._4408f4a8._58676a35").click()
                    time.sleep(3)

                except:
                    continue
                try:
                    number = self.browser.find_element(By.CSS_SELECTOR,"._4408f4a8._58676a35 ._5079de6b.be13fe44 ._45d98091.ae608d5a._221ec77a.be13fe44")
                    time.sleep(3)
                    # print(number.text)
                    newRow["PhoneNumber"] = number.text[1:]
                except:
                    newRow["PhoneNumber"] = "no number found"
                    continue

                try:
                    heading = self.browser.find_element(By.CSS_SELECTOR,"._1075545d.d059c029._858a64cf .a38b8112")
                    time.sleep(3)
                    # print(number.text)
                    newRow["Heading"] = heading.text
                except:
                    newRow["Heading"] = "no heading"
                    continue

                try:
                    description = self.browser.find_element(By.CSS_SELECTOR,".cf4781f0 ._0f86855a span")
                    time.sleep(3)
                    # print(number.text)
                    newRow["description"] = description.text.replace("  ",'')
                except:
                    newRow["description"] = "no description"
                    continue

                try:
                    addPosted = self.browser.find_element(By.CSS_SELECTOR,"._1075545d.e3cecb8b._5f872d11 ._6d5b4928 span")
                    time.sleep(3)
                    olxAddPostedDate=addPosted.text
                    addPostedDateList = olxAddPostedDate.split(' ')
                    if 'hours'  in olxAddPostedDate or 'hour' in olxAddPostedDate:
                        addPostedDate = datetime.datetime.today()
                        newRow["addPosted"]=addPostedDate.date()

                    elif 'days' in olxAddPostedDate or 'day' in olxAddPostedDate:
                        addPostedDate = datetime.datetime.today()-datetime.timedelta(days=int(addPostedDateList[0]))
                        newRow["addPosted"]=addPostedDate.date()

                    elif 'week'  in olxAddPostedDate or 'weeks'  in olxAddPostedDate:
                        addPostedDate = datetime.datetime.today() - datetime.timedelta(days=int(addPostedDateList[0])*7)
                        newRow["addPosted"]=addPostedDate.date()

                    elif 'month'  in olxAddPostedDate or 'months' in olxAddPostedDate:
                        addPostedDate = datetime.datetime.today() - datetime.timedelta(days=int(addPostedDateList[0])*30)
                        newRow["addPosted"]=addPostedDate.date()

                except:
                    newRow["addPosted"] = "no description"
                    continue

            except:
                continue
            try:
                query = "INSERT INTO OlxData (Name, PhoneNumber,MemberSince,AddPosted,Address,AddId,Price,AddHeading,AddCategory,AddDescription,RecordAdded) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (newRow["Name"], newRow["PhoneNumber"], newRow["MemberSince"], newRow["addPosted"], newRow["Address"],
                    newRow["AddId"], newRow["Price"], newRow["Heading"], self.searchWord, newRow["description"],datetime.date.today())
                print(val)
                mycursor.execute(query, val)
            except:
                continue
        mydb.commit()


    def addingDataToDatabase(self):

        contactInfoDf=pd.read_csv("data/olxContactInfo.csv")
        contactInfoDf.fillna("no value",inplace=True)
        # print(contactInfoDf)
        query = "INSERT INTO contactinfo (Name, PhoneNumer,MemberSince,Address,AddId,Price,AddHeading) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        for x in range(0,len(contactInfoDf)):
            val = (contactInfoDf.at[x,"Name"], str(contactInfoDf.at[x,"PhoneNumber"]),contactInfoDf.at[x,"MemberSince"],contactInfoDf.at[x,"Address"],str(contactInfoDf.at[x,"AddId"]),contactInfoDf.at[x,"price"],contactInfoDf.at[x,"Heading"])
            print(val)
            # mycursor = mydb.cursor()
            mycursor.execute(query, val)
            mydb.commit()
            # print(mycursor.rowcount, "record inserted.")




if __name__=="__main__":
    with open('searchWord.txt', 'r') as file:
        searchWord = file.read()
        file.close()
    scrapper=OlxScrapper(searchWord)
    linksList=scrapper.extractLinks()
    time.sleep(10)
    scrapper.saveInExcelFile(linksList)
    time.sleep(5)
    scrapper.extractInfoFromLinks()



    # scrapper.loginInOLX()
