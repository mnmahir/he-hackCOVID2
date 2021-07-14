import tkinter as tk
from tkinter.constants import RIGHT, W
import PIL.Image, PIL.ImageTk
import time
import cv2


# Import module
from webcamvid import VideoCapture
from detection import *
from tkinter import ttk
from tkinter import HORIZONTAL
from tkinter import CENTER
from tkinter import LEFT

class App:
    def __init__(self, window, window_title, video_source=0):
        # ======= APP GUI ATTR =======
        self.window = window
        self.window.title(window_title)
        window.iconbitmap('Far.ico')
        
        
        #============FRAME============
        self.frame1 = tk.Frame(self.window, padx = 40, pady=80, bg = 'DeepSkyBlue4')
        self.frame1.grid(row=0, column =0, rowspan=20)
        self.frame2 = tk.Frame(self.window, padx = 10, pady=10)
        self.frame2.grid(row=1, column =1, rowspan=20 , columnspan =3)
        
        # ======= IMAGE WIDGET =======
        # Image Layout size
        self.people=tk.Canvas(self.frame2, width = 130, height =100)
        self.violations=tk.Canvas(self.frame2, width = 130, height =100)
        self.face=tk.Canvas(self.frame2, width = 130, height =110)
        self.mask=tk.Canvas(self.frame2, width = 140, height =120)
        self.nomask=tk.Canvas(self.frame2, width = 140, height =120)
        self.logo=tk.Canvas(self.frame2, width = 200, height =100)
                
        # Image Layout
        self.people.grid(row=1, column=3, sticky='w')
        self.violations.grid(row=3, column=3, sticky='w')
        self.face.grid(row=5, column=3, sticky='w')
        self.mask.grid(row=7, column=3, sticky='w')
        self.nomask.grid(row=9, column=3, sticky='w')
        self.logo.grid(row=12, column=3,sticky='w', columnspan = 2, rowspan = 2)
        
        #Image data
        self.img_people = PIL.ImageTk.PhotoImage(PIL.Image.open("people3.png"))  
        self.people.create_image(15, 10, anchor='nw', image=self.img_people)        
        self.img_violations = PIL.ImageTk.PhotoImage(PIL.Image.open("violation.png"))  
        self.violations.create_image(15, 10, anchor='nw', image=self.img_violations)        
        self.img_face = PIL.ImageTk.PhotoImage(PIL.Image.open("face.png"))  
        self.face.create_image(15, 10, anchor='nw', image=self.img_face)        
        self.img_mask = PIL.ImageTk.PhotoImage(PIL.Image.open("mask.png"))  
        self.mask.create_image(-15, 60, anchor='w', image=self.img_mask)        
        self.img_nomask = PIL.ImageTk.PhotoImage(PIL.Image.open("nomask.png"))  
        self.nomask.create_image(-15, 60, anchor='w', image=self.img_nomask)        
        self.img_logo = PIL.ImageTk.PhotoImage(PIL.Image.open("Far.png"))  
        self.logo.create_image(-15, 60, anchor='w', image=self.img_logo)
        
        # ======= TEXT WIDGET =======
        # Text data
        #self.numofpeople=tk.Label(self.window, text="No. of People = ")
        self.numofpeople_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'), bg = 'gold', width = 6, height = 2)
        self.numofviolations_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)
        self.numofface_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)
        self.numofmask_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)
        self.numofnomask_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)
        self.maxpeople=tk.Label(self.frame1, text="COVID-19 SOP ALERT SYSTEM", font=('Helvetica',15,'bold'),bg = 'gold', width = 70, height = 2, justify = LEFT,anchor='w')
#        
        # STATUS WIDGET
        self.numofpeople_stat=tk.Label(self.frame2, text="NORMAL", font=('Helvetica',20,'bold'),bg = 'green', width = 8, height = 2)
        self.numofviolations_stat=tk.Label(self.frame2, text="NORMAL", font=('Helvetica',20,'bold'),bg = 'green', width = 8, height = 2)
        self.numofnomask_stat=tk.Label(self.frame2, text="NORMAL", font=('Helvetica',20,'bold'),bg = 'green', width= 8, height = 2)
        
        
        #ICON LABEL 
        self.numofpeople_label=tk.Label(self.frame2, text="PEOPLE COUNTER", font=('Helvetica',12,'bold'), width = 18)
        
        self.numofviolations_label=tk.Label(self.frame2, text="VIOLATIONS COUNTER", font=('Helvetica',12,'bold'),width = 18)
       
        self.numofface_label=tk.Label(self.frame2, text="FACES COUNTER  ", font=('Helvetica',12,'bold'),width = 14)
       
        self.numofmask_label=tk.Label(self.frame2, text="MASK COUNTER", font=('Helvetica',12,'bold'),width = 18)
        
        self.numofnomask_label=tk.Label(self.frame2, text="NO MASK COUNTER", font=('Helvetica',12,'bold'), width = 18)
        
        self.maxpeople_label=tk.Label(self.frame2, text="MAX PEOPLE", font=('Helvetica',12,'bold'), width = 18)
        
        #Text Layout
        
        self.numofpeople_val.grid(row=1, column=4)
        self.numofviolations_val.grid(row=3, column=4)
        self.numofface_val.grid(row=5, column=4)
        self.numofmask_val.grid(row=7, column=4)
        self.numofnomask_val.grid(row=9, column=4)
        self.maxpeople.grid(row=15, column = 1, padx=10)
        
        # Status Layout
        self.numofpeople_stat.grid(row=1, column=5)
        self.numofviolations_stat.grid(row=3, column=5)
        self.numofnomask_stat.grid(row=9, column=5)
        
        #ICON LABEL LAYOUT
        
        self.numofpeople_label.grid(row=2, column=3)        
        self.numofviolations_label.grid(row=4, column=3)       
        self.numofface_label.grid(row=6, column=3)       
        self.numofmask_label.grid(row=8, column=3)        
        self.numofnomask_label.grid(row=10, column=3)        
        self.maxpeople_label.grid(row=8, column=5)      


        # ======= BUTTON WIDGET =======
        # Button Data
        self.btn_snapshot=tk.Button(self.frame1, text="SNAPSHOT", bg = 'gold', command=self.snapshot, width=15, height=2)  
        self.btn_quit=tk.Button(self.frame2, text='QUIT',command=quit,bg = 'cold',width=15, height=2)
        # Button Layout
        self.btn_snapshot.grid(row=12, column=1, padx=10, pady=30)
        self.btn_quit.grid(row=12, column = 5,padx=10, pady=10)
        
        
         # ======= SLIDER WIDGET =======
        self.slider = tk.Scale(self.frame2, from_=0, to=50, command = self.check_people, width = 30, length = 200)
        self.slider.grid(row=5, column=5, rowspan = 3) 
        
    
        # ======== WEBCAM DISPLAY WIDGET =======
        self.frame_size = frame_size
        self.video_source = video_source
        # Canvas to fit above video source widget size
    
        #self.canvas = tk.Canvas(self.frame1, width = 640 , height = 500)
        self.canvas = tk.Canvas(self.frame1, width = frame_size[0], height = frame_size[1])
        
        # Widget Layout
        self.canvas.grid(row=1, column=1, rowspan=10)
        # Open webcam
        self.vid = VideoCapture(self.video_source)
        # Update frame from webcam and also detection info
        self.delayupdate = 5 # update frame in x millisecond + detection delay
        self.update()
        self.delay_snap = 1000 # check every x milli second
        self.auto_snap()



        # ======= LEAVE THIS AT THE END =======
        # This method listens for events, such as button clicks or keypresses, and blocks any code that comes after it from running until the window it's called on is closed.
        self.window.mainloop()
        


    # >METHOD TO UPDATE FRAME AND DATAS IN APP GUI
    def update(self):
        t_start = time.time()
        ret, frame = self.vid.get_frame()   # Get a frame from the video source
        frame = cv2.resize(frame, self.frame_size,fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        frame, faces, has_mask, no_mask, soc_dist_violate, total_people = goDetect(frame)      # Call method for detection
        

        self.numofpeople_val.config(text=str(total_people))
        self.numofviolations_val.config(text=str(soc_dist_violate))
        self.numofface_val.config(text=str(faces))
        self.numofmask_val.config(text=str(has_mask))
        self.numofnomask_val.config(text=str(no_mask))
        if total_people >= self.slider.get():
            self.numofpeople_stat.config(text="ALERT", bg = "red")
        else:
            self.numofpeople_stat.config(text="NORMAL", bg = "green")

        if soc_dist_violate >= 1:
            self.numofviolations_stat.config(text="ALERT", bg = "red")
        else:
            self.numofviolations_stat.config(text="NORMAL", bg = "green")

        if no_mask >= 1:
            self.numofnomask_stat.config(text="ALERT", bg = "red")
        else:
            self.numofnomask_stat.config(text="NORMAL", bg = "green")

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.delayupdate,self.update)
        t_end = time.time()
        print("Delay: {:.2f}ms".format((t_end-t_start)*1000))



    # >METHOD TO TAKE SNAPSHOT
    def snapshot(self):
        ret,frame = self.vid.get_frame()      # Get a frame from the video source
        frame = cv2.resize(frame, self.frame_size,fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        frame, faces, has_mask, no_mask, soc_dist_violate, total_people = goDetect(frame)             # Call method for detection
        if ret:
            cv2.imwrite("snapshot/frame-snapshot-"+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))

    def auto_snap(self):
        ret,frame = self.vid.get_frame()      # Get a frame from the video source
        print("Auto snap check")
        frame = cv2.resize(frame, self.frame_size,fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        frame, faces, has_mask, no_mask, soc_dist_violate, total_people = goDetect(frame)             # Call method for detection
        if total_people > self.slider.get():
            self.numofpeople_stat.config(text="ALERT", bg = "red")
        else:
            self.numofpeople_stat.config(text="NORMAL", bg = "green")

        if soc_dist_violate >= 1:
            self.numofviolations_stat.config(text="ALERT", bg = "red")
            cv2.imwrite("snapshot/social_distancing_violation/frame-socdist"+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
        else:
            self.numofviolations_stat.config(text="NORMAL", bg = "green")

        if no_mask >= 1:
            self.numofnomask_stat.config(text="ALERT", bg = "red")
            cv2.imwrite("snapshot/nomask/frame-nomask"+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
        else:
            self.numofnomask_stat.config(text="NORMAL", bg = "green")
        
        self.window.after(self.delay_snap,self.auto_snap)
     
   

    

    