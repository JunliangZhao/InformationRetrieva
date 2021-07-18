class myheap():
    def __init__(self,maxSize):
        self.maxSize=maxSize
        self.alldata=[]
        self.alldata.append(("",0.0))
        for i in range(self.maxSize):
            self.alldata.append(("",0.0))
    def push(self,keyvalue):
        if keyvalue[1]>self.alldata[1][1]:
            self.alldata[1]=keyvalue
        self.fix_down()
    def fix_down(self): #向下维护堆
        i=1
        while i<=self.maxSize:
            if 2*i>self.maxSize:break   #如果函数新插入元素下沉到底部，停止
            #选出最小的子节点，与父节点比较，若小则与父节点交换位置，如果存在不交换的情况，证明堆的维护完成
            elif 2*i+1>self.maxSize:  
                if self.alldata[2*i][1]<self.alldata[i][1]:
                    self.alldata[2*i],self.alldata[i]=self.alldata[i],self.alldata[2*i]
                    i=i*2
                else:break
            else:
                if self.alldata[2*i+1][1]<self.alldata[2*i][1]:
                    if self.alldata[i][1]>self.alldata[2*i+1][1]:
                        self.alldata[2*i+1],self.alldata[i]=self.alldata[i],self.alldata[2*i+1]
                        i=i*2+1
                    else:break
                else:
                    if self.alldata[i][1]>self.alldata[2*i][1]:
                        self.alldata[2*i],self.alldata[i]=self.alldata[i],self.alldata[2*i]
                        i=i*2  
                    else:break                 
    def myprint(self): #打印堆
        print(self.alldata)
    def returnSortHeap(self):   
        returndata=sorted(self.alldata,key=lambda x:x[1],reverse=True)
        tempreturn=[]
        for i in returndata:
            if i[1]==0.0:
                pass
            else:
                tempreturn.append((i[0],i[1]))
        return tempreturn
# temp=myheap(20)
# for i in range(1,21):
#     keyvalue=("zjl",float(i))
#     temp.push(keyvalue)
# mytemp=temp.returnSortHeap()
# print(mytemp)
