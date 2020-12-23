from fbs.builtin_commands import is_windows, is_mac
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QImageEncoderSettings, QCameraInfo
from datetime import datetime
import threading
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QImage
from picamera.array import PiRGBArray
from picamera import PiCamera
import queue, cv2, copy
import time


class CameraModel(QObject):
    __default_instance = None
    """This class provides QCamObjects"""
    image_saved = pyqtSignal(str)
    get_video_image_by_timer = pyqtSignal(dict)
    get_selectable_image_by_timer = pyqtSignal(dict)

    @classmethod
    def default(cls):
        """returns default instance of LearningModel class."""
        if cls.__default_instance is None:
            cls.__default_instance = CameraModel()
        return cls.__default_instance

    # @classmethod
    def get_available_camera_names(self) -> list:
        # print(uvc.device_list())
        # uvc.Capture(uvc.device_list()[0]["uid"])
        return self.__old_device_list
        # return [QCamera.deviceDescription(device_obj) for device_obj in QCamera.availableDevices()]

    def __init__(self):
        super().__init__()
        self.cams = {}
        # self.__cam_image_captures: Dict[str, QCameraImageCapture] = {}
        self.__queues = {}
        self.__old_device_list = []
        self.__fetch_cam()
        self.selected_cam_names = [self.get_available_camera_names()[0]]
        self.images = {}
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_playing_qimage)
        self.timer.start(1000/30)
        cv2.ocl.setUseOpenCL(False)
        try:
            default_camera_name = self.get_available_camera_names()[0]
            if default_camera_name is not '':
                self.selected_cam_names.append(default_camera_name)
        # TODO: Find correct error by using the computer which has no default camera
        except Exception:
            print('No default camera')

    def __fetch_cam(self):
        if not self.__old_device_list:
            cam = PiCamera()
            PiCamera.CAPTURE_TIMEOUT = 60
            self.cams[cam.revision] = cam
            print(cam.revision)
            self.is_running = True
            self.uvc_thread = threading.Thread(target=self.grab_uvc, args=(cam.revision, cam), daemon=True)
            self.uvc_thread.start()
            self.__old_device_list.append(cam.revision)

    def grab_uvc(self, device_name, uvc_capture):
        width, height, fps = 640, 480, 90
        print((width, height, fps))
        uvc_capture.resolution = (width, height)
        # uvc_capture.framerate = fps
        capture = PiRGBArray(uvc_capture)
        stream = uvc_capture.capture_continuous(capture, format="bgr", use_video_port=True)
        # time.sleep(2.0)
        while self.is_running:
            frame = stream.__next__()
            self.images[device_name] = frame.array
            capture.truncate(0)

    def img_converter(self, image):
        image_preview = copy.copy(cv2.cvtColor(image, cv2.COLOR_BGR2BGRA))
        height, width, bpc = image_preview.shape
        bpl = bpc * width
        q_image = QImage(image_preview.data, width, height, bpl, QImage.Format_ARGB32)
        return q_image

    def get_playing_qimage(self):
        q_cams_image = {}
        for device_name in self.get_available_camera_names():
            if device_name not in self.images:
                pass
            else:
                image = copy.copy(self.images[str(device_name)])
                q_image = self.img_converter(image)
                q_cams_image[device_name] = q_image
        if len(q_cams_image) == 0:
            return
        self.get_video_image_by_timer.emit(q_cams_image)


    def capture(self, directory: str):
        print('capture')
        # TODO: manage image name format (e.x. use Dataset.generate_image_path())
        timestamp = str(datetime.now().isoformat()).replace(':', '-')
        file_name = f'camera_{0}_{timestamp}.jpg'
        image_path = directory + '/' + file_name
        if self.images[self.selected_cam_names[0]] is not None:
            cv2.imwrite(image_path, self.images[self.selected_cam_names[0]])
            self.on_image_saved(image_path)
        self.on_image_saved(image_path)


    def on_image_saved(self, image_path):
        img = cv2.imread(image_path)
        cv2.imwrite(image_path, img)
        self.image_saved.emit(image_path)

    def close(self):
        self.is_running = False
        self.uvc_thread.join()
        for key, val in self.cams.items():
            val.close()

    def set_selected_camera_to_view_finder(self, view_finder_obj):
        # TODO:Handle many cameras on version 2.0 or more
        if len(self.selected_cam_names) > 0:
            self.__fetch_cam()
            # cam: QCamera = self.cams[self.selected_cam_names[0]]
            # cam.setViewfinder(view_finder_obj)

    def connect_view_finders_with_all_cameras(self, selectable_camera_view_list):
        self.__fetch_cam()
        # for selectable_camera_view in selectable_camera_view_list:
        #     selectable_camera_view.set_q_cam(self.cams[selectable_camera_view.get_cam_name()])
