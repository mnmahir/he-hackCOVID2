import tkinter as tk
from tkinter.constants import RIGHT, W
import PIL.Image, PIL.ImageTk
import time
import cv2

# Import module
from webcamvid import VideoCapture
from detection import *

class App:
    def __init__(self, window, window_title, video_source=0, frame_size = (640,480)):
        # ======= APP GUI ATTR =======
        self.window = window
        self.window.title(window_title)
        window.iconbitmap('icon/Far.ico')
        
        #============FRAME============
        self.frame1 = tk.Frame(self.window, padx = 40, pady=40, bg = 'DeepSkyBlue4')
        self.frame1.grid(row=1, column =1, rowspan=11)
        self.frame2 = tk.Frame(self.window, padx = 10, pady=10)
        self.frame2.grid(row=1, column =2, rowspan=11 , columnspan =3)

        # ======= IMAGE WIDGET =======
        # Image layout size
        self.people=tk.Canvas(self.frame2, width = 130, height =100)
        self.violations=tk.Canvas(self.frame2, width = 130, height =100)
        self.face=tk.Canvas(self.frame2, width = 130, height =110)
        self.mask=tk.Canvas(self.frame2, width = 130, height =100)
        self.nomask=tk.Canvas(self.frame2, width = 130, height =100)
        self.logo=tk.Canvas(self.frame2, width = 250, height =70)
        # Image layout
        self.people.grid(row=3, column=2, sticky='w')
        self.violations.grid(row=4, column=2, sticky='w')
        self.face.grid(row=5, column=2, sticky='w')
        self.mask.grid(row=6, column=2, sticky='w')
        self.nomask.grid(row=7, column=2, sticky='w')
        self.logo.grid(row=8, column=2, columnspan=3)
        # Image data
        self.img_people = PIL.ImageTk.PhotoImage(PIL.Image.open("icon/people3.png"))  
        self.people.create_image(10, 10, anchor='nw', image=self.img_people)
        self.img_violations = PIL.ImageTk.PhotoImage(PIL.Image.open("icon/violation.png"))  
        self.violations.create_image(10, 10, anchor='nw', image=self.img_violations)
        self.img_face = PIL.ImageTk.PhotoImage(PIL.Image.open("icon/face.png"))  
        self.face.create_image(10, 10, anchor='nw', image=self.img_face)
        self.img_mask = PIL.ImageTk.PhotoImage(PIL.Image.open("icon/mask.png"))  
        self.mask.create_image(10, 10, anchor='nw', image=self.img_mask)
        self.img_nomask = PIL.ImageTk.PhotoImage(PIL.Image.open("icon/nomask.png"))  
        self.nomask.create_image(10, 10, anchor='nw', image=self.img_nomask)
        self.img_logo = PIL.ImageTk.PhotoImage(PIL.Image.open("icon/Far.png"))  
        self.logo.create_image(10, 10, anchor='nw', image=self.img_logo)
        
        # ======= SLIDER WIDGET =======
        self.slider = tk.Scale(self.frame2, from_=0, to=30, orient = tk.HORIZONTAL, sliderlength = 10)
        #self.slider.tk.HORIZONTAL
        self.slider.grid(row=1, column=3 )

        # ======= TEXT WIDGET =======
        # Text data
        self.maxpeople=tk.Label(self.frame2, text="Max people:", font=('Helvetica',10,'bold'), width = 10, height = 2)
        self.numofpeople_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'), bg = 'gold', width = 6, height = 2)
        self.numofviolations_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)
        self.numofface_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)
        self.numofmask_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)
        self.numofnomask_val=tk.Label(self.frame2, text="N/A", font=('Helvetica',20,'bold'),bg = 'gold', width = 6, height = 2)

        self.numofpeople_stat=tk.Label(self.frame2, text="NORMAL", font=('Helvetica',20,'bold'),bg = 'green', width = 8, height = 2)
        self.numofviolations_stat=tk.Label(self.frame2, text="NORMAL", font=('Helvetica',20,'bold'),bg = 'green', width = 8, height = 2)
        self.numofnomask_stat=tk.Label(self.frame2, text="NORMAL", font=('Helvetica',20,'bold'),bg = 'green', width= 8, height = 2)

        #Text Layout
        self.maxpeople.grid(row=1, column=2)
        self.numofpeople_val.grid(row=3, column=3)
        self.numofviolations_val.grid(row=4, column=3)
        self.numofface_val.grid(row=5, column=3)
        self.numofmask_val.grid(row=6, column=3)
        self.numofnomask_val.grid(row=7, column=3)
        
        self.numofpeople_stat.grid(row=3, column=4)
        self.numofviolations_stat.grid(row=4, column=4)
        self.numofnomask_stat.grid(row=7, column=4)
        

        # ======= BUTTON WIDGET =======
        # Button Data
        self.btn_snapshot=tk.Button(self.frame1, text="Snapshot", bg = '#ffb3fe', command=self.snapshot, width=15, height=2)  
        self.btn_quit=tk.Button(self.frame2, text='QUIT', command=quit, width=15, height=2)
        # Button Layout
        self.btn_snapshot.grid(row=11, column=1, padx=10, pady=10)
        self.btn_quit.grid(row=11, column=3, padx=10, pady=10)
        
         


        # ======== WEBCAM DISPLAY WIDGET =======
        self.frame_size = frame_size
        self.video_source = video_source
        # Canvas to fit above video source widget size
        self.canvas = tk.Canvas(self.frame1, width = frame_size[0], height = frame_size[1])
        # Widget Layout
        self.canvas.grid(row=1, column=1, rowspan=8)
        # Open webcam
        self.vid = VideoCapture(self.video_source)
        # Update frame from webcam and also detection info
        self.delayupdate = 5 # update frame in x millisecond + detection delay
        self.update()
        self.delay_snap = 2000 # check every 2 second
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