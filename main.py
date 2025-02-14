import os
import time
import socket
import subprocess
import cv2
import base64
import sys
import traceback
from wormholelite import CameraVideo
from websocket import create_connection
from ai_pipeline.input_delegator import delegate_input
from ai_pipeline.recognize_speech import listen_for_keyword
from ai_pipeline.bot_handler import playAudio

def start(spot):
    playAudio(delegate_input(listen_for_keyword(), spot))

ROBOT_IP = "10.0.0.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']

"""
4 different states:

Two methods to activate Spot:
- Use Tensorflow 
- Use Audio from Webcam (triggered by 'hey spot')

Listening
1. use object detection API to walk towards object
2. take snapshot of project, send image to code processing Open AI
2.5 (if extra time) crop image before sending

Processing
3. Once response is recieved, return back info in text
Responding
4. Turn to person
5. Convert response into Text-to-speech, play through speaker
6. if possible, look at person and point to object 
Idling
""" 

# def voice_callback(message):
    # get

def main():
    # if True:
    from spot_controller import SpotController
    with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:
        globals()["spot_global"] = spot
        ws = create_connection("wss://737c-171-66-13-247.ngrok-free.app", ping_timeout=None)
        ws.send("Hello, World")
        # cam = CameraVideo(0, max_fps=1, height=360, width=480)
        while True:
            try:
                cmd =  ws.recv()
                # if cmd == "[CAM]":
                #     frame = cam.get_frame()
                #     _, enc = cv2.imencode('.jpg', frame)
                #     jpg_as_text = base64.b64encode(enc)
                #     # print(jpg_as_text)
                #     ws.send(jpg_as_text)
                #     continue
                if cmd == "[PAYLOAD]":
                    with open("/tmp/payload.py", "w+") as f:
                        f.seek(0)
                        f.truncate()
                        f.write(ws.recv())
                    try:
                        process = subprocess.Popen(["python3", "/tmp/payload.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                        for line in process.stdout:
                            ws.send(line.strip())
                        for line in process.stderr:
                            ws.send(line.strip())
                        process.wait()
                    except Exception as e:
                        ws.send(f"Error executing command: {e}")
                    ws.send("[EOL]")
                    continue
                res = eval(cmd)
                if res:
                    ws.send(str(res))
                else:
                    ws.send("None") 
            except Exception as e:
                print(traceback.format_exc())
                ws.send(str(e))


if __name__ == '__main__':
    main()

import time
time.sleep(50)
