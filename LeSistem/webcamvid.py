import cv2

class VideoCapture:
    def __init__(self, video_source=0):
        # ======= TO OPEN VIDEO SOURCE =======
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

    # >METHOD TO GET FRAME FROM VIDEO SOURCE (WEBCAM)
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:     # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # >METHOD TO RELEASE VIDEO SOURCE WHEN OBJECT IS DESTROYED
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            cv2.destroyAllWindows()