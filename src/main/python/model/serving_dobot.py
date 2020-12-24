from PyQt5.QtCore import pyqtSignal, QObject, QThread
import threading
import RPi.GPIO as GPIO
import os
import glob
import time

class ServingDobot(QObject):
    __default_instance = None
    dobot_req = pyqtSignal()

    @classmethod
    def default(cls):
        """returns default instance of LearningModel class."""
        if cls.__default_instance is None:
            cls.__default_instance = ServingDobot()
        return cls.__default_instance

    def __init__(self):
        QObject.__init__(self)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(19, GPIO.HIGH)
        GPIO.output(26, GPIO.HIGH)
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.HIGH)

        self.is_waiting_req = True
        self.__waiting_dobot_req_thread = threading.Thread(target=self.waiting_dobot_req, daemon=True)
        self.__waiting_dobot_req_thread.start()

    def waiting_dobot_req(self):
        self.is_waiting_req = True
        print("--- Waiting ---")
        while self.is_waiting_req:
            if len(glob.glob('/home/pi/gazo*')) > 0:
                print("!!! GAZO exist 1 !!!")
                self.dobot_req.emit()
                self.is_waiting_req = False
                print("!!! GAZO exist 2 !!!")

    def sending_inspection_result(self, result, result_sw, image_path):
        if not self.is_waiting_req:
            print(result)
            print(result_sw)
            print('image_path = ' + image_path)
            key_word = image_path[image_path.rfind('/')+1:image_path.rfind('_')]
            print('key_word = ' + key_word)
            if result_sw:
                if 'topleft' in image_path:
                    GPIO.output(20, GPIO.LOW)
                    print("!!! OK topleft !!!")
                    time.sleep(0.1)
                    GPIO.output(20, GPIO.HIGH)
                elif 'botleft' in image_path:
                    GPIO.output(21, GPIO.LOW)
                    print("!!! OK botleft !!!")
                    time.sleep(0.1)
                    GPIO.output(21, GPIO.HIGH)
                elif 'topright' in image_path:
                    GPIO.output(19, GPIO.LOW)
                    print("!!! OK topright !!!")
                    time.sleep(0.1)
                    GPIO.output(19, GPIO.HIGH)
                elif 'botright' in image_path:
                    GPIO.output(26, GPIO.LOW)
                    print("!!! OK botright !!!")
                    time.sleep(0.1)
                    GPIO.output(26, GPIO.HIGH)
                else:
                    print("NO any 4 direction cameras !!!")
            gazo_list = glob.glob('/home/pi/' + key_word + '*')
            remove_image_path = gazo_list[0]
            os.remove(remove_image_path)
            self.__waiting_dobot_req_thread = threading.Thread(target=self.waiting_dobot_req, daemon=True)
            self.__waiting_dobot_req_thread.start()



