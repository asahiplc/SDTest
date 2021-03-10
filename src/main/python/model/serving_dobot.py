from PyQt5.QtCore import pyqtSignal, QObject, QThread
import threading
import smbus
import os
import glob
import time
import csv
import subprocess
from operator import itemgetter

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

        DEVICE_BUS = 1
        DEVICE_ADDR = 0x10
        bus = smbus.SMBus(DEVICE_BUS)
        for i in range(1,4):
            bus.write_byte_data(DEVICE_ADDR, i, 0x00)

        self.is_waiting_req = True
        self.__waiting_dobot_req_thread = threading.Thread(target=self.waiting_dobot_req, daemon=True)
        self.__waiting_dobot_req_thread.start()

    def waiting_dobot_req(self):
        self.is_waiting_req = True
        print("--- Waiting ---")
        while self.is_waiting_req:
            if len(glob.glob('/home/pi/gazo*')) > 0:
                print("!!! GAZO exist 1 !!!")
                global s1
                s1 = time.time()
                print("s1 = ", s1)
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
                DEVICE_BUS = 1
                DEVICE_ADDR = 0x10
                bus = smbus.SMBus(DEVICE_BUS)
                if 'topleft' in image_path:
                    bus.write_byte_data(DEVICE_ADDR, 3, 0xFF)
                    print("!!! OK topleft !!!")
                    time.sleep(0.1)
                    bus.write_byte_data(DEVICE_ADDR, 3, 0x00)
                elif 'botleft' in image_path:
                    bus.write_byte_data(DEVICE_ADDR, 4, 0xFF)
                    print("!!! OK botleft !!!")
                    time.sleep(0.1)
                    bus.write_byte_data(DEVICE_ADDR, 4, 0x00)
                elif 'topright' in image_path:
                    bus.write_byte_data(DEVICE_ADDR, 1, 0xFF)
                    print("!!! OK topright !!!")
                    time.sleep(0.1)
                    bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
                elif 'botright' in image_path:
                    bus.write_byte_data(DEVICE_ADDR, 2, 0xFF)
                    print("!!! OK botright !!!")
                    time.sleep(0.1)
                    bus.write_byte_data(DEVICE_ADDR, 2, 0x00)
                else:
                    print("NO any 4 direction cameras !!!")
            gazo_list = glob.glob('/home/pi/' + key_word + '*')
            remove_image_path = gazo_list[0]
            os.remove(remove_image_path)

            global s1, s2
            s2 = time.time()
            print("s2 = ", s2)
            s_time = '{:.3g}'.format(s2 - s1)
            print("s_time = ", s_time)

            file = open('/home/pi/SDTest_result.csv', 'a')
            w = csv.writer(file)

            gCpuUsage = CpuUsage()       # ???
            CpuRateList = gCpuUsage.get()
            CpuRate     = CpuRateList[0]
            CpuRate_str = "  CPU:%3d" % CpuRate
            del CpuRateList[0]
            CpuTemp     = GetCpuTemp()
            CpuTempNum = CpuTemp.replace("temp=", "").replace("'C", "")
            CpuVolts     = GetCpuVolts()
            CpuVoltsNum = CpuVolts.replace("volt=", "").replace("V", "")
            CpuFreq     = int(GetCpuFreq()/1000000)
            CpuFreq_str = "ARM %4dMHz  " % CpuFreq
            Info_str = CpuFreq_str + CpuTemp + CpuVolts + CpuRate_str + "%"
            print(Info_str, CpuRateList)
            w.writerow([image_path, s_time, CpuTempNum, CpuVoltsNum, CpuRate])
            file.close()

            # OLD result image remove
            DIR = '/home/pi/Seal_inspection_keyencecamera/inspection_results/images'
            print("Result images = ", sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR)))
            filelists = []
            for file in os.listdir(DIR):
                base, ext = os.path.splitext(file)
                if ext == '.bmp':
                    filelists.append([DIR + '/' + file, os.path.getctime(DIR + '/' + file)])
            filelists.sort(key=itemgetter(1), reverse=True)
            MAX_CNT = 1000
            for i,file in enumerate(filelists):
                if i > MAX_CNT - 1:
                    print("Remove Result file = ", file[0])
                    os.remove(file[0])

            self.__waiting_dobot_req_thread = threading.Thread(target=self.waiting_dobot_req, daemon=True)
            self.__waiting_dobot_req_thread.start()

# CPU parameters get
def GetCpuFreq():
    Cmd = 'vcgencmd measure_clock arm'
    result = subprocess.Popen(Cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    Rstdout ,Rstderr = result.communicate()
    CpuFreq = Rstdout.split('=')
    return int(CpuFreq[1])

def GetCpuTemp():
    Cmd = 'vcgencmd measure_temp'
    result = subprocess.Popen(Cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    Rstdout ,Rstderr = result.communicate()
    CpuTemp = Rstdout.split()
    return CpuTemp[0]

def GetCpuVolts():
    Cmd = 'vcgencmd measure_volts'
    result = subprocess.Popen(Cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    Rstdout ,Rstderr = result.communicate()
    CpuVolts = Rstdout.split()
    return CpuVolts[0]

def GetCpuStat():
    Cmd = 'cat /proc/stat | grep cpu'
    result = subprocess.Popen(Cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    Rstdout ,Rstderr = result.communicate()
    LineList = Rstdout.splitlines()
    #
    TckList = []
    for Line in LineList:
        ItemList = Line.split()
        TckIdle = int(ItemList[4])
        TckBusy = int(ItemList[1])+int(ItemList[2])+int(ItemList[3])
        TckAll  = TckBusy + TckIdle
        TckList.append( [ TckBusy ,TckAll ] )
    return  TckList


class CpuUsage:
    def __init__(self):
        self._TckList    = GetCpuStat()

    def get(self):
        TckListPre       = self._TckList
        TckListNow       = GetCpuStat()
        self._TckList    = TckListNow
        CpuRateList = []
        for (TckNow, TckPre) in zip(TckListNow, TckListPre):
            TckDiff = [ Now - Pre for (Now , Pre) in zip(TckNow, TckPre) ]
            TckBusy = TckDiff[0]
            TckAll  = TckDiff[1]
            if TckAll == 0:
                CpuRate = 100
            else:
                CpuRate = int(TckBusy*100/TckAll)
            CpuRateList.append( CpuRate )
        return CpuRateList



