from flask import Flask, render_template, request, Response
import RPi.GPIO as GPIO                 
import time      
import io
import threading
import picamera

class Camera:
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    start_time = 0  # time of last client access to the camera

def getStreaming(self):
    Camera.start_time = time.time()
    #self.initialize()
    if Camera.thread is None:
        # start background frame thread
        Camera.thread = threading.Thread(target=self.streaming)
        Camera.thread.start()

        # wait until frames start to be available
        while self.frame is None:
            time.sleep(0)
    return self.frame

@classmethod

def streaming(c):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for f in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                c.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - c.start_time > 10:
                    break
        c.thread = None