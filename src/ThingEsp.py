import paho.mqtt.client as mqtt
import json
from threading import Thread, Lock
import json
import requests
import cv2

thingesp_server = 'thingesp.siddhesh.me'


class Client(Thread):
    def __init__(self, username, projectName, password):
        Thread.__init__(self)
        self.username = username
        self.projectName = projectName
        self.password = password
        self.initalized = False
        self.mqtt_client = mqtt.Client(client_id=projectName+"@"+username)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.username_pw_set(
            username=projectName+"@"+username, password=password)
        self.mqtt_client.connect(thingesp_server, 1893, 60)

    def setCallback(self, func):
        self.callback_func = func
        self.initalized = True
        return self

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to thingesp with result code ", rc)
        self.mqtt_client.subscribe(self.projectName + "/" + self.username)

    def on_message(self, client, userdata, msg):
        if self.initalized != True:
            print('Please set the callback func!')
            return
        else:
            payload = json.loads(msg.payload.decode("utf-8"))
            print(payload)
            if payload['action'] == 'query':
                out = self.callback_func(payload['query'].lower()) or ""
                sendr = {
                    "msg_id": payload['msg_id'], "action": "returned_api_response", "returned_api_response": out}
                self.mqtt_client.publish(
                    self.projectName + "/" + self.username, json.dumps(sendr))

    def device_call(self, to_num, msg):
        out = {"action": "device_call", "to_number": to_num, "msg": msg}
        self.mqtt_client.publish(
            self.projectName+"/"+self.username, json.dumps(out))

    def sendImage(self, img_name, to_num, msg):
        url = f"https://{thingesp_server}/api/v1/user/{self.username}/project/{self.projectName}/img"
        if not msg:
            msg = ""
        resp = requests.post(url, data={'credentials': self.password, 'to_number': to_num, "msg": msg}, files={
            'img': (img_name, open(img_name, 'rb')),
        })
        print("Image sent! thingesp server response: " + str(resp.text))

    def run(self):
        self.mqtt_client.loop_forever()


class WebcamVideoStream():
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            print("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self):
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self):
        self.started = False
        self.thread.join()

    def saveImage(self, name="img.jpg"):
        cv2.imwrite(name, self.frame)
        print("{} written!".format(name))

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()
        self.stop()
        cv2.destroyAllWindows()