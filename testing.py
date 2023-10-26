import pandas as pd
from application import mycursor,mydb



contactInfoDf= pd.read_csv("olxData1.csv")
print(contactInfoDf)

query = "INSERT INTO olxdata (Name, PhoneNumber,MemberSince,AddPosted,Address,Addid,Price,AddHeading,AddCategory,AddDescription,RecordAdded) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
for x in range(0,len(contactInfoDf)):
    try:
        val = (contactInfoDf.at[x,"Name"], str(contactInfoDf.at[x,"PhoneNumber"]),contactInfoDf.at[x,"MemberSince"],contactInfoDf.at[x,"AddPosted"],
           contactInfoDf.at[x,"Address"],str(contactInfoDf.at[x,"Addid"]),contactInfoDf.at[x,"Price"],
           contactInfoDf.at[x,"AddHeading"],contactInfoDf.at[x,"AddCategory"],contactInfoDf.at[x,"AddDescription"],contactInfoDf.at[x,"RecordAdded"])
        print(val)
            # mycursor = mydb.cursor()
        mycursor.execute(query, val)
    except:
        print("datanot added")
        continue
mydb.commit()