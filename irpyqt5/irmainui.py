import re
import sys
from PyQt5.uic import *
from PyQt5.QtWidgets import *
from pythonds.basic.stack import Stack
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import MySQLdb
from poetryDialogui import PoertyDialogui
from heap import myheap
import os
import matplotlib.pyplot as plt 
import matplotlib.font_manager as fm
import numpy as np
from scipy import interpolate
class SearchWindow(QMainWindow):        
    def __init__(self):
        super(SearchWindow, self).__init__() #初始化
        self.ui = loadUi(r'mainwindow.ui', self)#加载ui
        self.setFixedSize(self.width(), self.height()); 
        self.setWindowIcon(QIcon("title.jpg"))
        self.bad=False
        self.ui.lineEdit.returnPressed.connect(lambda:self.doallsearch())
        self.ui.pushButton.clicked.connect(lambda:self.clicksearch())#获取按键
        self.ui.listView.clicked.connect(self.clickedlist)		 #listview 的点击事件
        self.ui.radioButton.clicked.connect(lambda:self.clicksearch())
        self.ui.radioButton_2.clicked.connect(lambda:self.clicksearch())
        self.ui.radioButton_3.clicked.connect(lambda:self.clicksearch())
        self.ui.radioButton_4.clicked.connect(lambda:self.clicksearch())
        self.ui.radioButton_5.clicked.connect(lambda:self.clicksearch())
        self.ui.radioButton.setChecked(True)
        self.ui.pushButton.setCursor(QCursor(Qt.PointingHandCursor));
        self.db=db = MySQLdb.connect("localhost", "root", "zjl123...", "if", charset='utf8' )
        self.cursor = db.cursor()
        self.k=20
        self.lam=0.5
        self.sortway=False
        self.avgcommentres=[]
        for i in range(10):
            self.avgcommentres.append(0)
        with open("search.txt",'r',encoding='gbk') as f:  #打开选中文件
            self.allmyser=f.readlines()
            self.sernum=len(self.allmyser)
        with open("commentres.txt","w") as f: 
            f.write("")

    def mycomment(self,requesttext):
        reslist=dict()
        num=1
        for i in self.listname:
            self.cursor.execute("select doc_id from docdic where doc_name='"+i.split(" ")[0]+"'")
            result=self.cursor.fetchall()
            if result:
                reslist[str(result[0][0])]=num
                num+=1
        commentres=dict()
        for i in range(1,11):
            commentres[i]=0.0
        for i in requesttext:
            self.cursor.execute("select docs from new_terms where term='"+i+"'")
            result=self.cursor.fetchall()
            if result:
                tempstr=result[0][0]
                alldoc=tempstr.split("/")
                alldoc.remove('')
                alldoc1=sorted(alldoc, key= lambda i:(int(i.split(",")[1])) ,reverse=True)
                # l=0
                # count=0
                # temprank=dict()
                # last=""
                # for j in alldoc1:
                #     if last!="" and int(last.split(",")[1])==int(j.split(",")[1]):
                #         pass
                #     else:
                #         l+=1
                #         if count>10:
                #             break
                #     temprank[j.split(",")[0]]=l
                #     count+=1
                #     last=j
                # for x in temprank:
                #     pass
                l=1
                #print(reslist)
                #print(alldoc1)
                for i in alldoc1:
                    if i.split(",")[0] in reslist:
                        tempcal=float(reslist[i.split(",")[0]]/l)
                        commentres[l]+=tempcal
                        l+=1
                        if l>10:
                            break
        max=commentres[1]
        min=commentres[1]
        for i in commentres:
            if max<commentres[i]:
                max=commentres[i]
            if min>commentres[i]:
                min=commentres[i]

        tempcomment=[]
        if max==min:
            for i in commentres:
                tempcomment.append(commentres[i])
        else:    
            for i in commentres:
                tempcomment.append((commentres[i]-min)/(max-min))
        for i in range(len(tempcomment)):
            self.avgcommentres[i]+=tempcomment[i]
        with open("commentres.txt","a") as f:  #打开选中文件
            f.write(str(tempcomment)+"/"+requesttext+"\n")
        x=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
        X_arr = np.array(x)
        Y_arr = np.array(tempcomment)
        X_new = np.linspace(X_arr.min(),X_arr.max(),200)
        f = interpolate.interp1d(X_arr,Y_arr,kind = 'cubic')
        Y_smooth = f(X_new)
        plt.plot(X_new,Y_smooth,label=requesttext)
        if self.sernum<=0:  
            myfont = fm.FontProperties(fname=r'C:\Windows\Fonts\STKAITI.ttf') 
            plt.legend()  # 让图例生效
            plt.margins(0)
            plt.subplots_adjust(bottom=0.10)
            plt.legend(prop=myfont)
            plt.savefig("pic/所有查询汇总.png")
    
    def doallsearch(self):
        if self.sernum>0:
            self.ui.lineEdit.setText(self.allmyser[len(self.allmyser)-self.sernum].split(" ")[0])
            self.ui.radioButton_5.setChecked(True)
            if self.allmyser[len(self.allmyser)-self.sernum].split(" ")[1]=="1\n":
                self.ui.radioButton.setChecked(True)
            if self.allmyser[len(self.allmyser)-self.sernum].split(" ")[1]=="2\n":
                self.ui.radioButton_2.setChecked(True)
            if self.allmyser[len(self.allmyser)-self.sernum].split(" ")[1]=="3\n":
                self.ui.radioButton_4.setChecked(True)
            if self.allmyser[len(self.allmyser)-self.sernum].split(" ")[1]=="4\n":
                self.ui.radioButton_5.setChecked(True)
            self.clicksearch()
            self.sernum-=1
        else:
            self.sernum=len(self.allmyser)
            x=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
            for i in range(len(self.avgcommentres)):
                self.avgcommentres[i]=self.avgcommentres[i]/self.sernum
            plt.plot(x,self.avgcommentres)
            plt.savefig("pic/统计平均结果.png")
            plt.clf()
            for i in range(10):
                self.avgcommentres[i]=0.0
        self.mycomment(self.ui.lineEdit.text())


    def vectormodel(self,requesttext):
        searchvector=[]
        docid=[]
        for i in requesttext:
            self.cursor.execute("select term_index from term_index where term_name='"+i+"'")  #查询数据库，获取用户输入term的term_id 也是构建向量的维数
            result = self.cursor.fetchall()  #获取查询结果
            if not result:
                pass
            else:
                searchvector.append(result[0][0])

            # self.cursor.execute("select docs from new_terms where term='"+i+"'")
            # result = self.cursor.fetchall()  #获取查询结果
            # tempdocs=""
            # if not result:
            #     tempdocs =""
            # else:tempdocs=result[0][0]
            # templist=tempdocs.split("/")
            # templist2=[i.split(",")[0] for i in templist]  #字符串分割获取id链表
            # if not docid:
            #     docid=templist2
            # docid=self.mult(docid,templist2)
        self.cursor.execute("select * from docdic")  #查询文档向量
        result =self.cursor.fetchall()
        mydoic=dict()
        for i in result:
            templist=i[2].split("/")
            templist2=dict()
            templist.remove("")
            if self.sortway:
                for j in templist:
                    templist2[j.split(",")[0]]=j.split(",")[3]   #余弦归一化
            else:
                for j in templist:
                    templist2[j.split(",")[0]]=j.split(",")[4]   #最大值归一化
            tempscore=0.0
            for j in searchvector:   #匹配两个向量的维度  
                if str(j) in templist2:
                    tempscore+=float(templist2[str(j)])
            mydoic[i[1]]=tempscore
        #建立最大堆的数据
        tempheap=myheap(self.k)
        for i in mydoic:
            tempheap.push((i,mydoic[i]))
        myresult=tempheap.returnSortHeap()
        return myresult  

    def boolmodel(self,requesttext):
        mydict=dict()
        for i in requesttext: #对每个term项进行查找
            self.cursor.execute("select docs from new_terms where term='"+i+"'")
            result = self.cursor.fetchall()  #获取查询结果
            tempdocs=""
            if not result:  #如果查询不到结果
                tempdocs =""
            else:tempdocs=result[0][0]  #如果有结果
            tempdocs1=tempdocs.split("/")
            for j in tempdocs1:
                if j=="":
                    continue
                tempdocs2=j.split(",")
                if tempdocs2[0] in mydict: 
                    mydict[tempdocs2[0]]=mydict[tempdocs2[0]]+(float(tempdocs2[3]),float(tempdocs2[4]))  #采用字典和map两个结合
                else:
                    mydict[tempdocs2[0]]=(float(tempdocs2[3]),float(tempdocs2[4]))
        return mydict
    
    def bimodel(self,requesttext):
        searchvector=[]
        for i in requesttext:
            self.cursor.execute("select term_index from term_index where term_name='"+i+"'")  #查询数据库，获取用户输入term的term_id 也是构建向量的维数    
            result = self.cursor.fetchall()
            if not result:
                pass
            else:
                tempid=result[0][0]
                self.cursor.execute("select score from term_possi where term='"+i+"'")#再次查询数据库获取该Term得分
                result = self.cursor.fetchall()
                searchvector.append((tempid,result[0][0]))
        self.cursor.execute("select * from docdic")  #查询文档向量
        result =self.cursor.fetchall()
        mydoic=dict()#保存所有文档得得分
        for i in result:  #遍历所有文档
            templist=i[2].split("/")  #第一次分割获取`termindex,tf,tf_idf,w1,w2/`
            templist2=dict()  #创建一个字典 hashmap 来保存向量得维度和归一化结果
            templist.remove("")
            if self.sortway:
                for j in templist:  #对文档向量得不为零得维度进行赋值
                    templist2[j.split(",")[0]]=j.split(",")[3]   #余弦归一化
            else:
                for j in templist:
                    templist2[j.split(",")[0]]=j.split(",")[4]   #最大值归一化
            tempscore=0.0
            for j in searchvector:   #匹配两个向量的维度  
                if str(j[0]) in templist2:
                    tempscore+=float(templist2[str(j[0])])*float(j[1])
            mydoic[i[1]]=tempscore
        tempheap=myheap(self.k)
        for i in mydoic:
            tempheap.push((i,mydoic[i]))
        myresult=tempheap.returnSortHeap()
        return myresult
    
    def mlemodel(self,requesttext):
        self.cursor.execute("select * from new_doc_dic");
        result=self.cursor.fetchall();
        mydoc=dict()  #准备保存每个文档得名称和得分
        myrequest=[]
        for i in requesttext:
            myrequest.append(i)
        for i in result:  #查询数据库 
            if i[2]:
                tempinfo=i[2].split("/")
                tempinfo.remove("")  #第一次分割 获取每篇doc 得所有term项 
                score=1.0 
                for j in tempinfo:
                    tempterm=j.split(",")[0]  #第二次分割 提取 mc md term
                    if tempterm in myrequest:
                        score*=self.lam*(float(j.split(",")[1])+1)+(1-self.lam)*(float(j.split(",")[2])+1)  #lambda公式
                mydoc[i[1]]=score-1
        tempheap=myheap(self.k)  #建堆排序
        for i in mydoc:
            tempheap.push((i,mydoc[i]))
        myresult=tempheap.returnSortHeap()
        return myresult
    def clicksearch(self):
        judge=0
        self.sortway=not self.sortway
        if self.sortway:
            print("余弦归一化")
            print("tf_idf")
        else:
            print("最大值归一化")
            print("wf_idf")

        requesttext=self.ui.lineEdit.text() #获取用户输入框
        reslist=[]
        if self.ui.radioButton.isChecked(): #判定向量模型
            reslist=self.vectormodel(requesttext) #二元组
            judge=1
        elif self.ui.radioButton_2.isChecked():  #判定布尔模型
            reslist=self.boolmodel(requesttext)
            judge=2
        elif self.ui.radioButton_3.isChecked():  #判定条件表达式模型 
            reslist=self.splitword(requesttext)
            judge=3
        elif self.ui.radioButton_4.isChecked(): #判定为概率模型
            reslist=self.bimodel(requesttext)
            judge=4
        elif self.ui.radioButton_5.isChecked(): #判定为语义模型
            reslist=self.mlemodel(requesttext)
            judge=5


        self.ui.label.setText("")#初始化label提示
        if self.bad:  #判定是否表达式不规范
            self.ui.label.setText("表达式不规范")
            listModel=QStringListModel()
            self.ui.listView.setModel(listModel)
            self.bad=False
            return
        if  judge==2:  #如果是bool 则需要对返回结果进行排序
            if self.sortway:
                reslist1=sorted(reslist, key = lambda i:[reslist[i][0],reslist[i][1]],reverse=True)
            else:
                reslist1=sorted(reslist, key = lambda i:[reslist[i][1],reslist[i][0]],reverse=True)
            reslist2=dict()
            for i in reslist1:
                reslist2[i]=reslist[i]
            reslist=reslist2
        listModel=QStringListModel()
        self.listname=[]
        tempnum=0
        if not reslist:
            if self.ui.lineEdit.text()!="":
                self.ui.label.setText("没有检索到结果")
                self.listname.append("对不起")
                self.listname.append("没有找到您要得结果")
                self.listname.append("下次一定做得更好")
                self.listname.append("=3=")
            listModel.setStringList(self.listname)
            self.ui.listView.setModel(listModel)
            return
        for i in reslist:
            if judge==1 or judge==4 or judge==5:
                tempres="vectror or bim"
            else:
                self.cursor.execute("select doc_name from doc where doc_id="+str(i))
                tempres = self.cursor.fetchall()  #获取查询结果
            if not tempres:
                pass
            else:
                if judge==2:  #判定是否为bool模型
                    self.listname.append(tempres[0][0]+" "+str(reslist[i][0])+" "+str(reslist[i][1]))
                elif judge==1 or judge==4 or judge==5: #判断是否为向量模型或者概率模型或者语义模型
                    self.listname.append(i[0]+" "+str(i[1]))  
                else:  #判定为条件检索
                    self.listname.append(tempres[0][0]+" ")
                tempnum+=1
            if tempnum>=self.k:
                break
        listModel.setStringList(self.listname)
        self.ui.listView.setModel(listModel)
        if judge==1 or judge==4 or judge==5:
            self.ui.label.setText("数据库共有602条，显示"+str(self.k)+"条")
        elif self.k>=len(reslist):
            self.ui.label.setText("共检索到"+str(len(reslist))+"条")
        else:
            self.ui.label.setText("共检索到"+str(len(reslist))+"条，显示"+str(self.k)+"条")

    def clickedlist(self,qModelIndex): #编写点击函数
        contextpath=self.listname[qModelIndex.row()].split(" ")[0]
        sorry=["对不起","没有找到您要得结果","下次一定做得更好","=3="]
        if contextpath in sorry:
            with open("data/sorry.txt",'r') as f:  #打开选中文件
                context=f.read()
        elif not os.path.exists("data/"+contextpath):
            with open("data/sorry.txt",'r') as f:  #打开选中文件
                context=f.read()
        else:
            with open("data/"+contextpath,'r',encoding="utf-8") as f:  #打开选中文件
                context=f.read()
        context=contextpath.split(".")[0]+"\n"+context
        poetry=PoertyDialogui(context)
        poetry.show()
        
    def splitword(self,requesttext):  #bool模型
        dict={"*":1,"-":1,"+":2,"(":3,")":3}#建立运算符字典
        stack=Stack()
        output=""
        #中缀表达式改后缀表达式 入栈部分 
        if not requesttext:
            return []
        for i in requesttext: #遍历用户输入搜索表达式
            if i in dict:   #确定该表达式是否在运算符字典中
                if stack.isEmpty():  #栈为空
                    stack.push(i)
                elif dict[stack.peek()]>dict[i]:  #op大于栈顶op的优先级
                    stack.push(i)
                elif i=="(":
                    stack.push(i)
                elif i==")":
                    while stack.peek()!="(":
                        output+=stack.peek()
                        stack.pop()
                    stack.pop()
                else:   #op小于栈顶op优先级
                    while dict[stack.peek()]<=dict[i]:  
                        output+=stack.peek()
                        stack.pop()
                        if stack.isEmpty():
                            break
                    stack.push(i)
            else:
                output+=i
        while stack.isEmpty()==False:
            output+=stack.peek()
            stack.pop()
        stack2=Stack()  #后缀表达式计算值的栈
        #print(output)
        initlist=[]
        if  requesttext[0] is "*":
            initlist=[str(i) for i in range(602)]
        elif requesttext[0] is "-":
            initlist=[str(i) for i in range(602)]
        stack2.push(initlist)
        for i in output:
            if i=="+":
                #取两个操作数起来计算
                if stack2.size()<2:
                    self.bad=True
                    return []
                list1=stack2.peek()
                stack2.pop()
                list2=stack2.peek()
                stack2.pop()
                templist=self.plus(list1,list2)
                stack2.push(templist)
            elif i=="-":
                #取两个操作数起来计算
                if stack2.size()<2:
                    self.bad=True
                    return []
                list1=stack2.peek()
                stack2.pop()
                list2=stack2.peek()
                stack2.pop()
                templist=self.sub(list2,list1)
                stack2.push(templist)
            elif i=="*":
                #取两个操作数起来计算
                if stack2.size()<2:
                    self.bad=True
                    return []
                list1=stack2.peek()
                stack2.pop()
                list2=stack2.peek()
                stack2.pop()
                templist=self.mult(list1,list2)
                stack2.push(templist)
            else:
                self.cursor.execute("select docs from new_terms where term='"+i+"'")
                result = self.cursor.fetchall()  #获取查询结果
                tempdocs=""
                if not result:
                    tempdocs =""
                else:tempdocs=result[0][0]
                templist=tempdocs.split("/")
                templist2=[i.split(",")[0] for i in templist]  #字符串分割获取id链表
                stack2.push(templist2)        
        reslist=stack2.peek()
        reslist1=[int(i) for i in reslist if i!=""] 
        reslist1.sort()
        return reslist1        
    def plus(self,list1,list2):#定义一个链表的加法 
        return list(set(list1)|set(list2))
    def sub(self,list1,list2): #定义一个链表减法
        return list(set(list1)-set(list2))
    def mult(self,list1,list2):#定义一个链表的且运算
        return list(set(list1)&set(list2))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = SearchWindow()
    mainWindow.show()
    sys.exit(app.exec_())

