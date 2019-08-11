#!/usr/bin/python3

#App Name : k stop watch 
#version : 0.1
#Author : Khaled  Fathi [ khaledfathi@protonmail.com]
#code : Python3 / PyQt5
#repository : https://github.com/khaledfathi/K-Stopwatch-

import sys , time , threading
from PyQt5.QtWidgets import QApplication , QWidget , QPushButton , QLabel ,QTextBrowser , QFrame
from PyQt5.QtGui import QFont  

class app (QWidget):
    "PyQt GUI"
    def __init__(self):
        super().__init__()
        #Geometry 
        self.left , self.top , self.width , self.height = 100 , 100 , 600 , 230
        
        #GUI
        self.main_window()
        self.labels()
        self.buttons()
        self.text_browser()
        
        #Backend
        self.hr , self.mn , self.sc , self.ss = 0 , 0 , 0 , 0
        self.startcount=act(self.lb1,self.hr, self.mn,self.sc, self.ss) # threading object 
        
        #show GUI
        self.show()
    
    def main_window(self):
        "main window"
        self.setWindowTitle("Khaled Stop watch")
        self.setGeometry(self.left , self.top , self.width, self.height)
        self.setMaximumHeight(self.height)
        self.setMaximumWidth(self.width)
        self.setMinimumHeight(self.height)
        self.setMinimumWidth(self.width)
    
    def labels (self):
        "any labels in any place in 'main_window'"
        self.lb1 = QLabel("00 : 00 : 00 : 00" , self)
        self.lb1.setGeometry (200,20,400,50)
        self.lb1.setFont(QFont("Times" , 30))
    
    def buttons (self):
        "any buttons in any place in 'main_window'"
        self.b1 = QPushButton("Start" , self)
        self.b1.move(10,10)
        self.b1.setToolTip("Start Stopwatch")
        self.b1.clicked.connect(self.start_action)
        
        self.b2 = QPushButton("Pause" , self)
        self.b2.move(10,60)
        self.b2.setToolTip("Pause")
        self.b2.clicked.connect(self.pause_action)
        
        self.b3 = QPushButton("Stop" , self)
        self.b3.move(10,110)
        self.b3.setToolTip("Stop and Clear result")
        self.b3.clicked.connect(self.stop_action)
        
        self.b4 = QPushButton("Lap" , self)
        self.b4.move(500,35)
        self.b4.setToolTip("Capture Lap")
        self.b4.clicked.connect(self.lap_action)
       
        self.out = QPushButton("Quit" , self)
        self.out.move(10,160)
        self.out.setToolTip("Exit")
        self.out.clicked.connect(self.quit_)
    
    def text_browser (self):
        "QTextBrowser to show lap result "
        self.text = ""
        self.res = QTextBrowser(self)
        self.res.setGeometry(100,90,480,100)
        self.res.setFont(QFont("Time" , 20))
    
    def start_action (self):
        "method for start button"
        try :
            self.startcount.start()
        except:
            pass    
    def pause_action (self):
        "method for pause button"
        self.startcount.flag=0
        self.hr = self.startcount.hr
        self.mn = self.startcount.mn
        self.sc = self.startcount.sc
        self.ss = self.startcount.ss
        del self.startcount
        self.startcount = act(self.lb1 , self.hr , self.mn , self.sc , self.ss)
    
    def stop_action (self):
        "method for stop button"
        self.startcount.flag=0
        try :
            self.startcount.join() #cant clear result without it ?!
        except:
            pass
        del self.startcount
        self.hr, self.mn, self.sc , self.ss = 0 , 0 , 0 ,0
        self.startcount = act(self.lb1,self.hr, self.mn, self.sc , self.ss)
        self.lb1.setText("00 : 00 : 00 : 00")
    
    def lap_action (self):
        text = str(self.startcount.hr) + " : " + str(self.startcount.mn) + " : " +\
            str(self.startcount.sc) + " : " + str(self.startcount.ss)+"\n"
        text = self.startcount.make_00(self.startcount.hr , self.startcount.mn ,self.startcount.sc , self.startcount.ss) +"\n"
        self.text += text
        self.res.setText(self.text)
            
    def quit_ (self) :
        "method for quit button"
        self.startcount.flag=0
        sys.exit()
        
class act (threading.Thread) :
    "Thread for stop watch"
    def __init__(self,lb,hr,mn,sc,ss):
        super().__init__()
        self.lb , self.hr , self.mn , self.sc , self.ss , self.flag = lb , hr , mn , sc , ss , 1
    
    def make_00 (self,*arg):
        "check number [hour , minute , second , f_second] , if they are less than 10 add zero\
        reslut should be like this '05' , also it format the whole text for output like this"
        data = ["0"+str(i) if i < 10 else str(i) for i in arg ]
        return data[0] + " : " + data[1] + " : " + data[2] + " : "  + data[3]
        
    def run (self):
        "the Thread methon , run by methon 'Threading.start()'"
        while self.flag :
            self.ss+=1
            time.sleep(1/60)
            if self.ss > 59 :
                self.ss=0
                self.sc+=1
            if self.sc > 59 :
                self.sc=0
                self.mn+=1
            if self.mn > 59 :
                self.mn=0
                self.hr+=1
            self.lb.setText(self.make_00(self.hr,self.mn,self.sc,self.ss))
        
#run app from this file 
if __name__ == "__main__":
    APP = QApplication(sys.argv)
    ex = app()
    sys.exit(APP.exec_())
    
        
