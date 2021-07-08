import tkinter as tk
import PIL.Image, PIL.ImageTk
import time
import cv2

# Import module
from webcamvid import VideoCapture

class App:
    def __init__(self, window, window_title, video_source=0):
        # ======= APP GUI ATTR =======
        self.window = window
        self.window.title(window_title)
        


        # ======== WEBCAM DISPLAY =======
        self.video_source = video_source
        # Canvas to fit above video source size
        self.canvas = tk.Canvas(window, width = 640, height = 480)
        self.canvas.pack()
        # Open webcam
        self.vid = VideoCapture(self.video_source)
        # Update frame from webcam
        self.delay = 10 # update frame in x millisecond
        self.update()

    
        # ======= BUTTONS IN GUI =======
        #   --Snapshot
        self.btn_snapshot=tk.Button(window, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(side=tk.LEFT)
        #   --Quit
        self.btn_quit=tk.Button(window, text='QUIT', command=quit)
        self.btn_quit.pack(side=tk.RIGHT)


        # ======= LEAVE THIS AT THE END =======
        # This method listens for events, such as button clicks or keypresses, and blocks any code that comes after it from running until the window it's called on is closed.
        self.window.mainloop()
        

    # >METHOD TO TAKE SNAPSHOT
    def snapshot(self):
        ret,frame=self.vid.get_frame()      # Get a frame from the video source
        if ret:
            cv2.imwrite("frame-"+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))

    # >METHOD TO UPDATE FRAME
    def update(self):
        ret, frame = self.vid.get_frame()   # Get a frame from the video source
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.delay,self.update)