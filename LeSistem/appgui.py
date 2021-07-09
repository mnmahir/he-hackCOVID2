import tkinter as tk
from tkinter.constants import RIGHT, W
import PIL.Image, PIL.ImageTk
import time
import cv2

# Import module
from webcamvid import VideoCapture
from detection import *

class App:
    def __init__(self, window, window_title, video_source=0):
        # ======= APP GUI ATTR =======
        self.window = window
        self.window.title(window_title)
        


        # ======= TEXT WIDGET =======
        # Text data
        self.numofpeople=tk.Label(self.window, text="No. of People = ")
        self.numofpeople_val=tk.Label(self.window, text="N/A", font=('Helvetica',20,'bold'))
        self.numofviolations=tk.Label(self.window, text="No. of Social Distancing Violations = ")
        self.numofviolations_val=tk.Label(self.window, text="N/A", font=('Helvetica',20,'bold'))
        self.numofface=tk.Label(self.window, text="No. of Faces = ")
        self.numofface_val=tk.Label(self.window, text="N/A", font=('Helvetica',20,'bold'))
        self.numofmask=tk.Label(self.window, text="No. of People wearing masks = ")
        self.numofmask_val=tk.Label(self.window, text="N/A", font=('Helvetica',20,'bold'))
        self.numofnomask=tk.Label(self.window, text="No. of People not wearing masks = ")
        self.numofnomask_val=tk.Label(self.window, text="N/A", font=('Helvetica',20,'bold'))
        # Text Layout
        self.numofpeople.grid(row=1, column=2, sticky='e')
        self.numofpeople_val.grid(row=1, column=3)
        self.numofviolations.grid(row=2, column=2, sticky='e')
        self.numofviolations_val.grid(row=2, column=3)
        self.numofface.grid(row=3, column=2, sticky='e')
        self.numofface_val.grid(row=3, column=3)
        self.numofmask.grid(row=4, column=2, sticky='e')
        self.numofmask_val.grid(row=4, column=3)
        self.numofnomask.grid(row=5, column=2, sticky='e')
        self.numofnomask_val.grid(row=5, column=3)
        
        

        # ======= BUTTON WIDGET =======
        # Button Data
        self.btn_snapshot=tk.Button(window, text="Snapshot", command=self.snapshot, width=15, height=2)  
        self.btn_quit=tk.Button(window, text='QUIT', command=quit, width=15, height=2)
        # Button Layout
        self.btn_snapshot.grid(row=11, column=1, padx=10, pady=10)
        self.btn_quit.grid(row=11, column=3, padx=10, pady=10)



        # ======== WEBCAM DISPLAY WIDGET =======
        self.video_source = video_source
        # Canvas to fit above video source widget size
        self.canvas = tk.Canvas(window, width = 640, height = 480)
        # Widget Layout
        self.canvas.grid(row=1, column=1, rowspan=10)
        # Open webcam
        self.vid = VideoCapture(self.video_source)
        # Update frame from webcam and also detection info
        self.delay = 10 # update frame in x millisecond + detection delay
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




    

    