from PIL import ImageTk,Image,ImageDraw,ImageOps
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from threading import Thread
import time


class mainUi(tk.Tk):
    def __init__(self,inTitle):
        self.windows = tk.Tk()
        
        self.windows.minsize(1280,720)
        self.windows.maxsize(1280,720)
        self.windows.title(inTitle)
        self.btnChooseImg = tk.Button(self.windows,text='OpenImage',command=self.chooseImage,font=(None,20))
        self.btnChooseImg.grid(column=0,row=0,columnspan=6,pady=10)
        self.bkImg = ImageTk.PhotoImage(Image.new('RGBA',(512,512), (255,255,255,255)))
        self.canvas1 = tk.Canvas(self.windows,width=512,height=512)
        self.canvas1.grid(column=0,columnspan=2,row=1,stick='wn',padx=10)
        self.canvas1Img = self.canvas1.create_image(0,0,anchor='nw',image=self.bkImg)
        self.canvas2 = tk.Canvas(self.windows,width=512,height=512)
        self.canvas2.grid(column=2,columnspan=2,row=1,stick='en',padx=10)
        self.canvas2Img = self.canvas2.create_image(0,0,anchor='nw',image=self.bkImg)

        self.labelFram = tk.Frame(self.windows)
        self.labelFram.grid(column=5,columnspan=2,row=1,rowspan=4,stick='nwse',padx=20)
        self.listBox = tk.Listbox(self.labelFram)
        self.listBox.pack(side='left',fill='both',ipadx=10)
        self.listBoxScrollBar = ttk.Scrollbar(self.labelFram,orient=tk.VERTICAL,command=self.listBox.yview)
        self.listBoxScrollBar.pack(side='right',fill='both')
        self.listBox['yscrollcommand'] = self.listBoxScrollBar.set
        

        self.btnConv = tk.Button(self.windows,text='Processing',command=self.processingImg,font=(None,20))
        self.btnConv.grid(column=0,columnspan=5,row=2,stick='nwse',pady=10)

        #sysinfo
        self.sysOpenUrlTitle = tk.Label(self.windows,text='ImagePath',font=(None,20),bg='white')
        self.sysOpenUrlTitle.grid(column=0,columnspan=1,row=3,stick='nwes')
        self.sysOpenUrlMsg = tk.StringVar()
        self.sysOpenUrlText = tk.Label(self.windows,textvariable=self.sysOpenUrlMsg,font=(None,20),bg='yellow',anchor='w')
        self.sysOpenUrlText.grid(column=1,columnspan=3,row=3,stick='nwes')

        self.systemInfotTitle = tk.Label(self.windows,text='System Info:',font=(None,20),bg='pink')
        self.systemInfotTitle.grid(column=0,columnspan=1,row=4,stick='nwes')
        self.systemMesg = tk.StringVar()
        self.sys_info = tk.Label(self.windows,textvariable=self.systemMesg,font=(None,20),anchor='e')
        self.sys_info.grid(column=1,columnspan=3,row=4,stick='nws')
        

        #parament
        self.canvas1ShowInputImg=None
        self.canvas2ShowInputImg=None
        
        #updataUi
        self.updateUI=updateUI(self.systemMesg,self.canvas2)
        
        #user set
        self.openImgUrl = None
        
        
    def chooseImage(self):
        self.openImgUrl = filedialog.askopenfilename()
        if self.openImgUrl:
            self.sysOpenUrlMsg.set(self.openImgUrl)
            inputImg = Image.open(self.openImgUrl)
            self.canvas1ShowInputImg = ImageTk.PhotoImage(inputImg.resize((512,512)))
            self.canvas1.itemconfig(self.canvas1Img,image=self.canvas1ShowInputImg)

    def processingImg(self):
        self.updateUI.isRun=True
    
        
    def show(self):
        self.updateUI.start()
        self.windows.mainloop()

    def setFunc(self,infunc,*inInput):
        self.updateUI.inputFunc = infunc
        
    def setFuncPara(self,*inInput):
        self.updateUI.inputFuncPara = inInput
    
    def setOutputImag(self,inOutputImg):
        self.canvas2ShowInputImg=ImageTk.PhotoImage(Image.fromarray(inOutputImg.astype('uint8')).resize((512,512)))
        self.canvas2.itemconfig(self.canvas2Img,image=self.canvas2ShowInputImg)

    def setOutputData(self,inData):
        self.listBox.delete(0,'end')
        n = 0
        for data in inData:
            self.listBox.insert('end',str(data))
            if n%2==0:
                self.listBox.itemconfig(n,background='deep sky blue')
            else:
                self.listBox.itemconfig(n,background='pink')
            n+=1
##MainProcess
class updateUI(Thread):
    def __init__(self,inSysMsg,incanvas2):
        Thread.__init__(self)
        self.daemon=True
        self.sysMsg=inSysMsg
        self.isRun=False
        self.inputFunc = None
        self.inputFuncPara = None
        
        self.canvas2 = incanvas2 
        
    def run(self):
        
        while True:
            if self.isRun == True:
                try:
                    startTime=time.time()
                    self.inputFunc(*self.inputFuncPara)
                    self.sysMsg.set(str(round(time.time()-startTime,2))+'s')
                except Exception as exec:
                    self.sysMsg.set('Error:'+str(exec))
                
                self.isRun=False
            else:
                time.sleep(0.1)



