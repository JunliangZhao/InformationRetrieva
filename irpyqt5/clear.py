import os
import re
path = "data"
filelist = [i for i in os.listdir(path)]
mydict=dict()
for file in filelist:
    data=""
    with open("data2/"+file,'r',encoding='utf-8') as f:
        temptext=f.read()
        tempdata = re.findall('[\u4E00-\u9FA5]', temptext)
        for i in tempdata:
            if i in mydict:
                mydict[i]=mydict[i]+1
            else:
                mydict[i]=1

templist=sorted(mydict,key=lambda x:(mydict[x]))
j=0
mydict2=dict()
for i in templist:
    mydict2[i]=j
    j=j+1




for file in filelist:
    with open("data2/"+file,'r',encoding='utf-8') as f:
        temptext=f.read()
        tempvector=dict()
        for i in temptext:
            if mydict2[i] in tempvector:
                tempvector[i]+=1
            else:
                tempvector[i]=1
        print(tempvector)

