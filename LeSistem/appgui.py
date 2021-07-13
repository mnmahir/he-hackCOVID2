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

class App:
    def __init__(self, window, window_title, video_source=0):
        # ======= APP GUI ATTR =======
        self.window = window
        window.iconbitmap('ae_Far.ico')
        #self.window.configure(bg='white')
        
        #============FRAME============
        self.frame1 = tk.Frame(self.window, padx = 40, pady=40, bg = 'DeepSkyBlue4')
        self.frame1.grid(row=1, column =0, rowspan=11)
        
        self.frame2 = tk.Frame(self.window, padx = 10, pady=10)
        self.frame2.grid(row=0, column =1, rowspan=11 , columnspan =2)
        
    
        
        # ======= IMAGE WIDGET =======
        # Text data
        self.people=tk.Canvas(self.frame2, width = 130, height =100)
        self.violations=tk.Canvas(self.frame2, width = 130, height =100)
        self.face=tk.Canvas(self.frame2, width = 130, height =110)
        self.mask=tk.Canvas(self.frame2, width = 130, height =100)
        self.nomask=tk.Canvas(self.frame2, width = 130, height =100)
        
        

        
        # Text Layout
        self.people.grid(row=1, column=3, sticky='w')
        self.violations.grid(row=2, column=3, sticky='w')
        self.face.grid(row=3, column=3, sticky='w')
        self.mask.grid(row=4, column=3, sticky='w')
        self.nomask.grid(row=5, column=3, sticky='w')
        
        #Image view
        self.img_people = PIL.ImageTk.PhotoImage(PIL.Image.open("people3.png"))  
        self.people.create_image(10, 10, anchor='nw', image=self.img_people)
        
        self.img_violations = PIL.ImageTk.PhotoImage(PIL.Image.open("violation.png"))  
        self.violations.create_image(10, 10, anchor='nw', image=self.img_violations)
        
        self.img_face = PIL.ImageTk.PhotoImage(PIL.Image.open("face.png"))  
        self.face.create_image(10, 10, anchor='nw', image=self.img_face)
        
        self.img_mask = PIL.ImageTk.PhotoImage(PIL.Image.open("mask.png"))  
        self.mask.create_image(10, 10, anchor='nw', image=self.img_mask)
        
        self.img_nomask = PIL.ImageTk.PhotoImage(PIL.Image.open("nomask.png"))  
        self.nomask.create_image(10, 10, anchor='nw', image=self.img_nomask)
        
        
    


         # ======= TEXT WIDGET =======
        # Text data
        #self.numofpeople=tk.Label(self.window, text="No. of People = ")
        self.numofpeople_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'), bg = 'gold', width = 6, height = 2)
#         self.numofviolations=tk.Label(self.window, text="No. of Social Distancing Violations = ")
        self.numofviolations_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)
#         self.numofface=tk.Label(self.window, text="No. of Faces = ")
        self.numofface_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)
#         self.numofmask=tk.Label(self.window, text="No. of People wearing masks = ")
        self.numofmask_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)
#         self.numofnomask=tk.Label(self.window, text="No. of People not wearing masks = ")
        self.numofnomask_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)
#        

        self.numofpeople_stat=tk.Label(self.frame2, text="NORMAL", font=('Helvetica',20,'bold'),bg = 'green', width = 8, height = 2)
        self.numofviolations_stat=tk.Label(self.frame2, text="NORMAL", font=('Helvetica',20,'bold'),bg = 'green', width = 8, height = 2)
        #self.numofface_stat=tk.Label(self.frame2, text="NORMAL", font=('Helvetica',20,'bold'),bg = 'green', width = 8, height = 2)
        #self.numofmask_stat=tk.Label(self.frame2, text="NORMAL", font=('Helvetica',20,'bold'),bg = 'green', width = 8, height = 2)
        self.numofnomask_stat=tk.Label(self.frame2, text="NORMAL", font=('Helvetica',20,'bold'),bg = 'green', width= 8, height = 2)


 
        #Text Layout
        
#         #self.numofpeople.grid(row=1, column=2, sticky='e')
        self.numofpeople_val.grid(row=1, column=4)
#         self.numofviolations.grid(row=2, column=2, sticky='e')
        self.numofviolations_val.grid(row=2, column=4)
#         self.numofface.grid(row=3, column=2, sticky='e')
        self.numofface_val.grid(row=3, column=4)
#         self.numofmask.grid(row=4, column=2, sticky='e')
        self.numofmask_val.grid(row=4, column=4)
#         self.numofnomask.grid(row=5, column=2, sticky='e')
        self.numofnomask_val.grid(row=5, column=4)
        
        self.numofpeople_stat.grid(row=1, column=5)
        self.numofviolations_stat.grid(row=2, column=5)
        #self.numofface_stat.grid(row=3, column=5)
        #self.numofmask_stat.grid(row=4, column=5)
        self.numofnomask_stat.grid(row=5, column=5)

        
        


        # ======= BUTTON WIDGET =======
        # Button Data
        self.btn_snapshot=tk.Button(self.frame1, text="Snapshot", bg = '#ffb3fe', command=self.snapshot, width=15, height=2)  
        #self.btn_quit=tk.Button(window, text='QUIT', command=quit, width=15, height=2)
        # Button Layout
        self.btn_snapshot.grid(row=11, column=1, padx=10, pady=10)
        #self.btn_quit.grid(row=11, column=3, padx=10, pady=10)
        
         # ======= SLIDER WIDGET =======
        self.slider = tk.Scale(self.frame2, from_=0, to=50, orient = HORIZONTAL, sliderlength = 5, command = self.check_people)
        #self.slider.tk.HORIZONTAL
        self.slider.grid(row=0, column=4 )
        
        



        # ======== WEBCAM DISPLAY WIDGET =======
        self.video_source = video_source
        # Canvas to fit above video source widget size
        self.canvas = tk.Canvas(self.frame1, width = 640, height = 550)
        # Widget Layout
        self.canvas.grid(row=1, column=1, rowspan=10)
        # Open webcam
        self.vid = VideoCapture(self.video_source)
        # Update frame from webcam and also detection info
        self.delay = 1 # update frame in x millisecond + detection delay
        self.update()



        # ======= LEAVE THIS AT THE END =======
        # This method listens for events, such as button clicks or keypresses, and blocks any code that comes after it from running until the window it's called on is closed.
        self.window.mainloop()
        


    # >METHOD TO UPDATE FRAME AND DATAS IN APP GUI
    def update(self):
        ret, frame = self.vid.get_frame()   # Get a frame from the video source
        frame, faces = goDetect(frame)      # Call method for detection

        self.numofface_val.config(text=str(faces))
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.delay,self.update)



    # >METHOD TO TAKE SNAPSHOT
    def snapshot(self):
        ret,frame = self.vid.get_frame()      # Get a frame from the video source
        frame, faces = goDetect(frame)             # Call method for detection
        if ret:
            cv2.imwrite("frame-"+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))



    # >METHOD TO CHECK AND COMPARE VALUES
    
# =============================================================================
    def check_people(self):
        r = slider.get()
        
        test = 5
        
        if r>= test:
            change_people(self)
            
        else:
            
            reset_people(self)
        
         
     
   # def check_violations(self):
         
     
    #def check_nomask (self):

    
    
    # >METHOD TO CHANGE STATUS
    
    def change_people(self):
         numofpeople_stat.config(text="ALERT", bg = "red")
         
    def change_violations(self):
         numofviolations_stat.config(text="ALERT", bg = "red") 
         
    def change_nomask(self):
         numofnomask_stat.config(text="ALERT", bg = "red")
        
    
    # >METHOD TO RESET STATUS
    
    def reset_people(self):
        numofpeople_stat.config(text="NORMAL", bg = "green")
        
    def reset_people(self):
        self.numofviolations_stat.config(text="NORMAL", bg = "green")    
        
    def reset_people(self):
        self.numofnomask_stat.config(text="NORMAL", bg = "green")


    

    