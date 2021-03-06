from fbs_runtime.application_context.PyQt5 import ApplicationContext
from model.camera_model import CameraModel
from model.project import Project
from model.learning_model import LearningModel
from view.ui.inspection import Ui_inspection
from view.camera_list import CameraList
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QMovie
from shutil import move, copy2
import os
from datetime import datetime


class InspectionWidget(QWidget):

    # this signal emit on shortage of ai models
    model_file_not_found_error = pyqtSignal()
    __INSPECTED_IMAGES_DIR_NAME = '/inspection_results/images'

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_inspection()
        self.ui.setupUi(self)
        # camera preview settings
        self.camera_model = CameraModel.default()
        self.camera_model.set_selected_camera_to_view_finder(self.ui.camera_preview)
        self.camera_model.image_saved.connect(self.on_image_saved)

        self.learning_model = LearningModel.default()
        self.learning_model.predicting_finished.connect(self.on_finished_predicting)

        self.select_camera_widget = CameraList()
        self.select_camera_widget.clicked.connect(self.on_clicked_camera_list)
        self.select_camera_widget.closed.connect(self.on_closed_camera_list)

        self.ui.inspect_button.clicked.connect(self.on_clicked_inspect_button)

        self.ui.inspect_existing_image_button.clicked.connect(self.on_clicked_inspection_existing_image_button)

        self.ui.result.setCurrentWidget(self.ui.default_result)

        appctxt = ApplicationContext()
        loader_gif_path = appctxt.get_resource('images/loader.gif')
        self.loader_movie = QMovie(loader_gif_path)
        self.loader_movie.setScaledSize(QSize(30, 8))
        self.loader_movie.start()

        self.__ng_counter = 0
        self.__ok_counter = 0
        self.ui.OK_counter_label.setText(str(self.ok_counter))
        self.ui.NG_counter_label.setText(str(self.ng_counter))

        self.msgBox = None

    @property
    def ok_counter(self):
        return self.__ok_counter

    @ok_counter.setter
    def ok_counter(self, new_value):
        self.__ok_counter = new_value
        self.ui.OK_counter_label.setText(str(self.ok_counter))

    @property
    def ng_counter(self):
        return self.__ng_counter

    @ng_counter.setter
    def ng_counter(self, new_value):
        self.__ng_counter = new_value
        self.ui.NG_counter_label.setText(str(self.ng_counter))

    def on_clicked_select_camera_button(self):
        print("!!! Camera Click !!!")
        if not CameraModel.get_available_camera_names():
            QMessageBox.warning(None, 'error', 'Camera not connected', QMessageBox.Close)
            return

        if self.select_camera_widget.isHidden():
            self.select_camera_widget = CameraList()
            self.select_camera_widget.clicked.connect(self.on_clicked_camera_list)
            self.select_camera_widget.closed.connect(self.on_closed_camera_list)
            self.select_camera_widget.show()
        else:
            self.select_camera_widget.activateWindow()
            self.select_camera_widget.raise_()

    def on_clicked_inspect_button(self):
        self.ui.inspect_button.setDisabled(True)
        self.ui.inspect_existing_image_button.setDisabled(True)
        self.camera_model.capture(Project.project_path() + '/tmp')
        self.ui.loader_label.setMovie(self.loader_movie)

    def on_image_saved(self, image_path):
        # FIXME: refactor the structure of camera model class not to call this function from camera_model.capture
        if os.path.basename(os.path.dirname(image_path)) == 'tmp':
            path = self.learning_model.start_predict([image_path])
            if path:
                self.alert_for_truncated_image(path)

    def on_finished_predicting(self, result):
        image_path = result['image_paths'][0]
        image_name = os.path.basename(image_path)
        inspected_image_dir_path = Project.project_path() + self.__INSPECTED_IMAGES_DIR_NAME
        score = result['scores']
        prediction = result['prediction']
        self.ui.loader_label.clear()
        if prediction == 'good':
            self.ui.result.setCurrentWidget(self.ui.OK)
            move(image_path, inspected_image_dir_path + '/OK_' + image_name)
            self.ui.ok_score.setText('Score: ' + '{:.2%}'.format(score))
            self.ok_counter += 1
        else:
            ng_image = QPixmap(str(image_path))
            self.ui.ng_image.setPixmap(ng_image.scaled(self.ui.ng_image.size()))
            self.ui.result.setCurrentWidget(self.ui.NG)
            self.ui.ng_score.setText('Score: ' + '{:.2%}'.format(score) + '\nLabel: ' +
                                     prediction)
            move(image_path, inspected_image_dir_path + '/NG_' + image_name)
            self.ng_counter += 1
        self.ui.inspect_button.setDisabled(False)
        self.ui.inspect_existing_image_button.setDisabled(False)

    def on_clicked_camera_list(self, camera_name):
        self.camera_model.selected_cam_names = [camera_name]
        self.set_camera_to_camera_preview()

    def on_closed_camera_list(self):
        self.set_camera_to_camera_preview()

    def set_camera_to_camera_preview(self):
        self.camera_model.set_selected_camera_to_view_finder(self.ui.camera_preview)

    def on_clicked_inspection_existing_image_button(self):
        ext_filter = '画像ファイル(*.jpg *.jpeg *.png *.gif *.bmp)'
        original_image_path, _ = QFileDialog.getOpenFileName(self,
                                                             caption='Open Directory',
                                                             filter=ext_filter,
                                                             directory=Project.latest_inspection_image_path())
        Project.save_latest_inspection_image_path(os.path.dirname(original_image_path))
        if original_image_path:
            _, ext = os.path.splitext(original_image_path)
            # TODO: manage image name format (e.x. use Dataset.generate_image_path())
            timestamp = str(datetime.now().isoformat()).replace(':', '-')
            file_name = f'camera_0_{timestamp}.{ext}'
            copied_image_path = Project.project_path() + '/tmp/' + file_name
            copy2(original_image_path, copied_image_path)
            path = self.learning_model.start_predict([copied_image_path])
            if path:
                self.alert_for_truncated_image(original_image_path)
                return
            self.ui.inspect_button.setDisabled(True)
            self.ui.inspect_existing_image_button.setDisabled(True)

    def alert_for_truncated_image(self, path):
        self.msgBox = QMessageBox()
        self.msgBox.setText('This image may be damaged. Inspection will be skipped.\n\n'
                            + 'Please press OK to continue your inspection.')
        self.msgBox.exec()

