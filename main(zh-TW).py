import tkinter as tk
from PIL import Image,ImageTk #處理label圖像
import cv2
import numpy as np
from tkinter import filedialog #搜尋檔案的那個視窗 #file_path = filedialog.askopenfilename()

PresetIMG="Pixabay Enrique Mesegue.jpg"#預設值
kernal_threshold_value='127'
edge_strong_value='200'
edge_week_value='70'
edge_size='3'
file_path=''
seesee_v=True
def preview():#預覽
        inner_kernal_threshold_value=int(kernal_threshold_value)#複製全域數值
        inner_edge_strong_value=int(edge_strong_value)
        inner_edge_week_value=int(edge_week_value)
        inner_edge_size=int(edge_size)
        def update_image():#更新label圖像
            yl,xl=e.shape
            if(xl>yl):#長邊等於900
                img=cv2.resize(e,None,fx=900/xl,fy=900/xl,interpolation=cv2.INTER_NEAREST)*255
            else:
                img=cv2.resize(e,None,fx=900/yl,fy=900/yl,interpolation=cv2.INTER_NEAREST)*255
            global mesh
            if(mesh.shape!=img.shape):#除法精度誤差修正
                #print("除法精度誤差已修正")
                mesh=cv2.resize(mesh,(len(img[0]),len(img)),interpolation=cv2.INTER_NEAREST)
            img=cv2.add(img,mesh)#讓預覽跟成品更接近
            PILimg= Image.fromarray(img)#轉換np成PIL
            PILimgtk = ImageTk.PhotoImage(PILimg) #PIL成tkinter
            lab.configure(image=PILimgtk)#不明，但跟下面的一起用
            lab.image=PILimgtk
        def edge():    #邊緣強化
            if(inner_edge_size!=0):
                b=cv2.Canny(a,inner_edge_week_value,inner_edge_strong_value)
                b=255-b
                if(inner_edge_size>3):
                    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(inner_edge_size,inner_edge_size))
                else:
                    kernel=np.ones((inner_edge_size,inner_edge_size),np.uint8)
                c=cv2.erode(b,kernel)#把邊緣變粗
                
                #zero,c=cv2.threshold(c,127,255,cv2.THRESH_BINARY)       
                d=cv2.bitwise_and(a,c)
                return d
            else:
                return a
        #------------------------------------------
        d=edge()#preview的起點
        global e#e是一個暫時性的成品
        trash,e=cv2.threshold(d,inner_kernal_threshold_value,1,cv2.THRESH_BINARY)
        update_image()

def update1(ikernal_threshold_value):
    global kernal_threshold_value
    kernal_threshold_value=ikernal_threshold_value#更新全域
    preview()
def update2(iedge_strong_value):
    global edge_strong_value
    edge_strong_value=iedge_strong_value
    preview()    
def update3(iedge_week_value):
    global edge_week_value
    edge_week_value=iedge_week_value
    preview()
def update4(iedge_size):
    global edge_size
    edge_size=iedge_size
    preview()

def change_file():
    file_path = filedialog.askopenfilename()#抓檔案的視窗
    if(file_path):#路徑不能有中文
        global a
        a=read(file_path)
    seesee()
    ent1.delete(0,"end")#更新entry預設值
    ent1.insert(0,str(len(a[0])))
    ent2.delete(0,"end")
    ent2.insert(0,str(len(a)))
    global mesh
    mesh=mesh_read()#更新網格

def read(path):#讀圖函式
    global file_path
    file_path=path
    a=cv2.imread(file_path,cv2.IMREAD_GRAYSCALE)
        #,cv2.IMREAD_REDUCED_GRAYSCALE_2
        #,cv2.IMREAD_GRAYSCALE
    def get_size():
        y=len(a)#讓尺寸好處理
        y=y-y%4
        x=len(a[0])
        x=x-x%2
        return (x,y)
    a=cv2.resize(a,get_size(),cv2.INTER_NEAREST)
    return a

def char_assignment(result):#上字
    #weight=((1,8),(2,16),(4,32),(64,128))
    weimatrix=np.array([[1,8],[2,16],[4,32],[64,128]])
    for i in range(0,len(e),4):
        result.append([]) 
        for j in range(0,len(e[0]),2):
            imgmatrix=np.zeros((4,2),dtype=np.uint8)#矩陣運算可提高兩倍多的速度
            imgmatrix=e[i:i+4,j:j+2]
            imgmatrix=1-imgmatrix
            matresult=imgmatrix*weimatrix
            index=np.sum(matresult)
            if(index!=0):
                result[int(i/4)].append(chr(0x2800+index)) #unicode編碼
            else:
                result[int(i/4)].append('⠀') 
    return result

def file_editor(result):
    strn=[]
    for i in range(len(result)):
        strn.append(''.join(result[i]))#二維字源陣列壓成一維字串陣列
    str1='\n'.join(strn)#陣列壓縮成字串
    f=open('img.txt','w',encoding="utf-8")
    f.write(str1)
    f.close()

def output_txt():
    preview()
    result=char_assignment([])
    file_editor(result)
def output_png():
    cv2.imwrite("output.png",e*255)

def seesee():#顯示原圖
    global seesee_v
    if(seesee_v==True):   
        yl,xl=a.shape
        if(xl>yl):
            aimg=cv2.resize(a,None,fx=900/xl,fy=900/xl,interpolation=cv2.INTER_NEAREST)
            PILimg= Image.fromarray(aimg)
            PILimgtk = ImageTk.PhotoImage(PILimg) 
            lab.configure(image=PILimgtk)
            lab.image=PILimgtk  
        else:
            aimg=cv2.resize(a,None,fx=900/yl,fy=900/yl,interpolation=cv2.INTER_NEAREST)
            PILimg= Image.fromarray(aimg)
            PILimgtk = ImageTk.PhotoImage(PILimg) 
            lab.configure(image=PILimgtk)
            lab.image=PILimgtk       
    else:
        preview()
    seesee_v=not seesee_v

def update_size():#尺寸更新後有很多東西要改
    global a
    a=read(file_path)
    a=cv2.resize(a,(int(x.get()),int(y.get())),cv2.INTER_NEAREST)
    def get_size():
        y=len(a)
        y=y-y%4
        x=len(a[0])
        x=x-x%4
        return (x,y)
    a=cv2.resize(a,get_size(),cv2.INTER_NEAREST)
    global mesh
    mesh=mesh_read()
    preview()

def mesh_read():
    mesh=cv2.imread("Mesh.png",cv2.IMREAD_GRAYSCALE)
    if(len(a)>len(a[0])):#提前裁切好網格，盡量不要用縮放的方式
        mesh=mesh[0:900,0:int(900*len(a[0])/len(a))]
    else:
        mesh=mesh[0:int(900*len(a)/len(a[0])),0:900]
    return mesh
    
root = tk.Tk()#創建父元件"root",rootg是視窗"tk"
#root.geometry("1440x720")#讓系統自動
a=read(PresetIMG)#預設讀取圖片，可改成商標
mesh=mesh_read()
#Rearrang the color channel
#b,g,r = cv2.split(a)
#img = cv2.merge((r,g,b))

#######以下是GUI###############

lab=tk.Label(root)#,width=800,height=1080)
lab.grid(row=0,column=0,padx=10,pady=5,rowspan=10)

sc1=tk.Scale(root, from_=0, to=254, label="內部臨界強度" , orient="horizontal",length=510,command=update1)
sc1.grid(row=1,column=1,padx=10,pady=5,columnspan=50)
sc1.set(127)
sc2=tk.Scale(root, from_=0, to=255, label="強邊緣值" , orient="horizontal",length=512,command=update2)
sc2.grid(row=2,column=1,padx=10,pady=5,columnspan=50)
sc2.set(200)
sc3=tk.Scale(root, from_=0, to=255, label="弱邊緣值" , orient="horizontal",length=512,command=update3)
sc3.grid(row=3,column=1,padx=10,pady=5,columnspan=50)
sc3.set(70)
sc4=tk.Scale(root, from_=0, to=8, label="邊緣強度(0=關閉)" , orient="horizontal",length=512,command=update4)
sc4.grid(row=4,column=1,padx=10,pady=5,columnspan=50)
sc4.set(3)


x=tk.StringVar()
y=tk.StringVar()
ent1=tk.Entry(root,width=5,textvariable=x)
ent1.grid(row=0,column=3)
ent2=tk.Entry(root,width=5,textvariable=y)
ent2.grid(row=0,column=5)
ent1.delete(0,"end")#這兩行是預設數值
ent1.insert(0,str(len(a[0])))
ent2.delete(0,"end")
ent2.insert(0,str(len(a)))


lab4=tk.Label(root,width=30,height=2,text="    圖片輸出解析度")
lab4.grid(row=0,column=1,rowspan=1)
lab2=tk.Label(root,width=3,height=2,text="x:",)
lab2.grid(row=0,column=2,rowspan=1)
lab3=tk.Label(root,width=3,height=2,text="y:")
lab3.grid(row=0,column=4,rowspan=1)
labemp=tk.Label(root,width=15,height=2,text="  ")
labemp.grid(row=0,column=6,columnspan=50)
bot5=tk.Button(root,width=10,height=2,text="解析度更新",command=update_size)
bot5.grid(row=0,column=7,padx=10,pady=5)


bot1=tk.Button(root,width=10,height=3,text="輸出txt檔",command=output_txt)
bot1.grid(row=5,column=1,padx=10,pady=5)
bot2=tk.Button(root,width=10,height=3,text="輸出線稿",command=output_png)
bot2.grid(row=5,column=2,padx=10,pady=5)
bot3=tk.Button(root,width=10,height=3,text="選擇導入圖片",command=change_file)
bot3.grid(row=5,column=3,padx=10,pady=5)
bot4=tk.Button(root,width=10,height=3,text="檢視原圖",command=seesee)
bot4.grid(row=5,column=4,padx=10,pady=5)

root.mainloop()
