from PyQt5.QtCore import pyqtSignal, QObject, QThread
import threading
import RPi.GPIO as GPIO
import os
import glob

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
        GPIO.output(19, GPIO.LOW)
        GPIO.output(26, GPIO.LOW)

        self.is_waiting_req = True
        self.__waiting_dobot_req_thread = threading.Thread(target=self.waiting_dobot_req, daemon=True)
        self.__waiting_dobot_req_thread.start()

    def waiting_dobot_req(self):
        self.is_waiting_req = True
        print("--- Waiting ---")
        while self.is_waiting_req:
            if len(glob.glob('/home/pi/kensa_gazo*')) > 0:
                print("!!! GAZO exist 1 !!!")
                self.dobot_req.emit()
                self.is_waiting_req = False
                print("!!! GAZO exist 2 !!!")

    def sending_inspection_result(self, result, result_sw):
        if not self.is_waiting_req:
#            gazo_list = glob.glob('/home/pi/kensa_gazo*')
#            remove_image_path = gazo_list[0]
            print(result)
            print(result_sw)
            remove_image_path = result['image_paths'][0]
            print('remove_image_path = ' + remove_image_path)
            if result_sw:
                print("!!! OK !!!")
                if 'left' in remove_image_path:
                    GPIO.output(19, GPIO.LOW)
                elif 'right' in remove_image_path:
                    GPIO.output(26, GPIO.LOW)
                else:
                    print("NO left/right")
            else:
                print("!!! NG !!!")
                if 'left' in remove_image_path:
                    GPIO.output(19, GPIO.HIGH)
                elif 'right' in remove_image_path:
                    GPIO.output(26, GPIO.HIGH)
                else:
                    print("NO left/right")
            os.remove(remove_image_path)
            self.__waiting_dobot_req_thread = threading.Thread(target=self.waiting_dobot_req, daemon=True)
            self.__waiting_dobot_req_thread.start()



