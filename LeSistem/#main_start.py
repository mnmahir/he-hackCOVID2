# Import module
from appgui import *

vid_source = 0 #' change tp 'test.mp4' for video OR 0 for camera
vid_size = (640,550)

def main():
    # ======= TO CREATE A WINDOW AND PASS TO APP OBJECT =======
    App(tk.Tk(),'COVID-19 SOP Monitoring', video_source=vid_source, frame_size = vid_size)

main()   