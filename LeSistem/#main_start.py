# Import module
from appgui import *


def main():
    # ======= TO CREATE A WINDOW AND PASS TO APP OBJECT =======
    App(tk.Tk(),'COVID-19 SOP Monitoring', video_source=0) #' change tp 'test.mp4' for video OR 0 for camera

main()   