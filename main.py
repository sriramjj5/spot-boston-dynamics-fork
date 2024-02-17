import os
import time
import socket
from websocket import create_connection

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

def main():
    if True:
    # from spot_controller import SpotController
    # with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:
        ws = create_connection("wss://6093-171-66-12-11.ngrok-free.app")
        ws.send("Hello, World")
        while True:
            try:
                cmd =  ws.recv()
                res = eval(cmd)
                if res:
                    ws.send(str(res))
                else:
                    ws.send("No response") 
            except Exception as e:
                ws.send(str(e))


if __name__ == '__main__':
    main()
