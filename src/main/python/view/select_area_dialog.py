﻿from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsItem, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsProxyWidget, QLabel, QFrame
from PyQt5.QtGui import QPixmap, QColor, QPen, QPalette
from PyQt5.QtCore import QRectF, QSize, Qt, pyqtSignal, QPoint
from view.ui.select_area_dialog import Ui_SelectAreaDialog
from model.dataset import Dataset
from model.project import Project
from model.supporting_model import TrimmingData
import os, cv2
from pathlib import Path


class SelectAreaDialog(QDialog):

    finish_selecting_area = pyqtSignal(TrimmingData)

    def __init__(self):
        super().__init__()
        self.ui = Ui_SelectAreaDialog()
        self.ui.setupUi(self)

        self.width = 200
        self.height = 200
        self.h, self.w = None, None
        self.select_area = None
        self.original_image_scene = None
        self.size_flag = True
        self.select_area_label = None
        self.select_area_label_proxy = None
        self.start_position = None

        self.get_ng_sample_image_path()

        if self.h <= self.height and self.w <= self.width:
            self.size_flag = False

        if self.size_flag:
            self.show_select_area_at_default_position()
        else:
            self.ui.notation_label.setText('Since the image size is small enough, we will train on the whole image.'
                                           '\nPlease push the training start button.')
            pass

        self.ui.ok_button.clicked.connect(self.on_clicked_ok_button)
        self.ui.cancel_button.clicked.connect(self.on_clicked_cancel_button)

    def get_ng_sample_image_path(self):
        test_ng_path = str(Dataset.images_path(Dataset.Category.TEST_NG))
        test_ng_images = os.listdir(test_ng_path)
        test_ng_images = [img for img in test_ng_images if Path(img).suffix in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']]
        if not test_ng_images:
            return
        original_image_path = os.path.join(test_ng_path, test_ng_images[0])
        original_image = cv2.imread(original_image_path)
        h, w, c = original_image.shape
        self.h, self.w = h, w
        original_image_shape = QSize(w+2, h+10)
        original_image_item = QGraphicsPixmapItem(QPixmap(original_image_path))
        original_image_item.setZValue(0)
        self.original_image_scene = QGraphicsScene()
        self.original_image_scene.addItem(original_image_item)
        self.ui.original_image_view.setScene(self.original_image_scene)
        self.ui.original_image_view.setBaseSize(original_image_shape)
        self.ui.original_image_view.setMaximumSize(original_image_shape)
        self.resize(self.w+32, self.h+72)

    def show_select_area_at_default_position(self):
        trimming_data = Project.latest_trimming_data()
        if trimming_data.position:
            self.start_position = QPoint(trimming_data.position[0], trimming_data.position[1])
            rect = QRectF(trimming_data.position[0], trimming_data.position[1], self.width, self.height)
        else:
            self.start_position = QPoint((self.w-self.width)//2, (self.h-self.height)//2)
            rect = QRectF((self.w-self.width)//2, (self.h-self.height)//2, self.width, self.height)
        self.select_area = QGraphicsRectItem(rect)
        self.select_area.setZValue(1)
        pen = QPen(QColor('#ffa00e'))
        pen.setWidth(4)
        pen.setJoinStyle(Qt.RoundJoin)
        self.select_area.setPen(pen)
        self.select_area.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.original_image_scene.addItem(self.select_area)
        self.select_area_label_proxy = QGraphicsProxyWidget(self.select_area)
        self.select_area_label = SelectAreaLabel()
        self.select_area_label.set_label()
        self.select_area_label_proxy.setWidget(self.select_area_label)
        self.select_area_label_proxy.setPos(self.select_area.boundingRect().left()+2, self.select_area.boundingRect().bottom()-self.select_area_label.height()-2)

    def on_clicked_ok_button(self):
        if not self.size_flag:
            trimming_data = TrimmingData(position=(0, 0), size=(self.w, self.h), needs_trimming=False)
            self.finish_selecting_area.emit(trimming_data)
            self.close()
        else:
            rel_position = self.select_area.pos()
            position = (self.start_position.x()+rel_position.x(), self.start_position.y()+rel_position.y())
            if position[0] < 0 or position[0] > self.w - self.width - 1 or position[1] < 0 or position[1] > self.h - self.height - 1:
                print('Error: Please set area contained in the image.')
                self.ui.notation_label.setText('Error: crop area must fit within image.')
            else:
                trimming_data = TrimmingData(position=position, size=(self.width, self.height), needs_trimming=True)
                self.finish_selecting_area.emit(trimming_data)
                self.close()

    def on_clicked_cancel_button(self):
        self.close()

    def closeEvent(self, QCloseEvent):
        self.close()

class SelectAreaLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.label_palette = QPalette()

    def set_label(self):
        self.setText('Inspection area')
        self.setAutoFillBackground(True)

        # TODO: Check the appearance on win or not
        # self.setFrameShape(QFrame.WinPanel)

        self.setStyleSheet("border: 4px solid #ffa00e;"
                           "background-color: #ffa00e;"
                           "color: #f5f5f5")
        self.setPalette(self.label_palette)
