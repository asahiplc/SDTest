# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inspection.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_inspection(object):
    def setupUi(self, inspection):
        inspection.setObjectName("inspection")
        inspection.resize(842, 532)
        font = QtGui.QFont()
        font.setPointSize(9)
        inspection.setFont(font)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(inspection)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.camera_preview = QCameraViewFinderWithGuide(inspection)
        self.camera_preview.setMinimumSize(QtCore.QSize(152, 102))
        self.camera_preview.setStyleSheet("background-color: #f5f5f5;\n"
"border: 1px solid #aaaaaa;\n"
"border-radius: 8px;\n"
"margin: 0px;\n"
"min-width: 150px;\n"
"min-height: 100px;\n"
"")
        self.camera_preview.setObjectName("camera_preview")
        self.verticalLayout.addWidget(self.camera_preview)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalWidget = QtWidgets.QWidget(inspection)
        self.horizontalWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.horizontalWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.horizontalWidget.setStyleSheet("")
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_4.setContentsMargins(-1, 1, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.inspect_button = QtWidgets.QPushButton(self.horizontalWidget)
        self.inspect_button.setObjectName("inspect_button")
        self.horizontalLayout_4.addWidget(self.inspect_button)
        self.inspect_existing_image_button = QtWidgets.QPushButton(self.horizontalWidget)
        self.inspect_existing_image_button.setObjectName("inspect_existing_image_button")
        self.horizontalLayout_4.addWidget(self.inspect_existing_image_button)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout.addWidget(self.horizontalWidget)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.loader_label = QtWidgets.QLabel(inspection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loader_label.sizePolicy().hasHeightForWidth())
        self.loader_label.setSizePolicy(sizePolicy)
        self.loader_label.setMinimumSize(QtCore.QSize(30, 0))
        self.loader_label.setMaximumSize(QtCore.QSize(30, 16777215))
        self.loader_label.setText("")
        self.loader_label.setObjectName("loader_label")
        self.horizontalLayout_7.addWidget(self.loader_label)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.result = QtWidgets.QStackedWidget(inspection)
        self.result.setMinimumSize(QtCore.QSize(300, 0))
        self.result.setStyleSheet("margin: 0px;")
        self.result.setObjectName("result")
        self.default_result = QtWidgets.QWidget()
        self.default_result.setAutoFillBackground(False)
        self.default_result.setStyleSheet("background-color: #f5f5f5;\n"
"border: 1px solid #aaaaaa;\n"
"border-radius: 6px;\n"
"margin: 0;")
        self.default_result.setObjectName("default_result")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.default_result)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.default_label = QtWidgets.QLabel(self.default_result)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.default_label.setFont(font)
        self.default_label.setStyleSheet("color:#aaaaaa;\n"
"border:none;\n"
"")
        self.default_label.setAlignment(QtCore.Qt.AlignCenter)
        self.default_label.setObjectName("default_label")
        self.verticalLayout_3.addWidget(self.default_label)
        self.result.addWidget(self.default_result)
        self.OK = QtWidgets.QWidget()
        self.OK.setStyleSheet("background-color: #193FDA68;\n"
"border: 1px solid #3FDA68;\n"
"border-radius: 6px;\n"
"color: #3FDA68;\n"
"margin: 0;\n"
"")
        self.OK.setObjectName("OK")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.OK)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem5)
        self.OK_big_icon_label = QtWidgets.QLabel(self.OK)
        self.OK_big_icon_label.setStyleSheet("border: none;\n"
"background-color: #00000000;")
        self.OK_big_icon_label.setText("")
        self.OK_big_icon_label.setPixmap(QtGui.QPixmap(":/icon/resources/base/fonts/fontawesome/large_check-circle_correctGreen.png"))
        self.OK_big_icon_label.setScaledContents(False)
        self.OK_big_icon_label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.OK_big_icon_label.setObjectName("OK_big_icon_label")
        self.verticalLayout_4.addWidget(self.OK_big_icon_label)
        self.OK_message_label = QtWidgets.QLabel(self.OK)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.OK_message_label.setFont(font)
        self.OK_message_label.setStyleSheet("color: #3FDA68;\n"
"background-color: transparent;\n"
"border: none;")
        self.OK_message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.OK_message_label.setObjectName("OK_message_label")
        self.verticalLayout_4.addWidget(self.OK_message_label)
        self.ok_score = QtWidgets.QLabel(self.OK)
        self.ok_score.setStyleSheet("color: #777777;\n"
"background-color: #00000000;\n"
"border: none;")
        self.ok_score.setText("")
        self.ok_score.setAlignment(QtCore.Qt.AlignCenter)
        self.ok_score.setObjectName("ok_score")
        self.verticalLayout_4.addWidget(self.ok_score)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem6)
        self.result.addWidget(self.OK)
        self.NG = QtWidgets.QWidget()
        self.NG.setStyleSheet("background-color: #19e66643;\n"
"border: 1px solid #e66643;\n"
"border-radius: 6px;\n"
"margin: 0;")
        self.NG.setObjectName("NG")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.NG)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem8)
        self.ng_image = QtWidgets.QLabel(self.NG)
        self.ng_image.setMinimumSize(QtCore.QSize(140, 140))
        self.ng_image.setMaximumSize(QtCore.QSize(140, 140))
        self.ng_image.setStyleSheet("color: #e66643;\n"
"border: none;\n"
"background-color: #00000000;")
        self.ng_image.setText("")
        self.ng_image.setAlignment(QtCore.Qt.AlignCenter)
        self.ng_image.setObjectName("ng_image")
        self.horizontalLayout_6.addWidget(self.ng_image)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem9)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem10)
        self.NG_message_label = QtWidgets.QLabel(self.NG)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.NG_message_label.setFont(font)
        self.NG_message_label.setStyleSheet("color: #e66643;\n"
"border: none;\n"
"background-color: transparent;")
        self.NG_message_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.NG_message_label.setObjectName("NG_message_label")
        self.verticalLayout_5.addWidget(self.NG_message_label)
        self.ng_score = QtWidgets.QLabel(self.NG)
        self.ng_score.setStyleSheet("color: #777777;\n"
"background-color: #00000000;\n"
"border: none;")
        self.ng_score.setAlignment(QtCore.Qt.AlignCenter)
        self.ng_score.setObjectName("ng_score")
        self.verticalLayout_5.addWidget(self.ng_score)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem11)
        self.result.addWidget(self.NG)
        self.verticalLayout_2.addWidget(self.result)
        self.widget = QtWidgets.QWidget(inspection)
        self.widget.setObjectName("widget")
        self.verticalLayout_2.addWidget(self.widget)
        self.counter = QtWidgets.QWidget(inspection)
        self.counter.setStyleSheet("background-color: #f5f5f5;\n"
"border: 1px solid #aaaaaa;\n"
"border-radius: 6px;\n"
"margin: 0;")
        self.counter.setObjectName("counter")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.counter)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.total_header_label = QtWidgets.QLabel(self.counter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.total_header_label.setFont(font)
        self.total_header_label.setStyleSheet("color: #3e3e3e;\n"
"border:none;\n"
"")
        self.total_header_label.setObjectName("total_header_label")
        self.horizontalLayout_2.addWidget(self.total_header_label)
        self.OK_icon_label = QtWidgets.QLabel(self.counter)
        self.OK_icon_label.setStyleSheet("border:none;\n"
"")
        self.OK_icon_label.setText("")
        self.OK_icon_label.setPixmap(QtGui.QPixmap(":/icon/resources/base/fonts/fontawesome/small_check-circle_correctGreen.png"))
        self.OK_icon_label.setObjectName("OK_icon_label")
        self.horizontalLayout_2.addWidget(self.OK_icon_label)
        self.OK_counter_label = QtWidgets.QLabel(self.counter)
        self.OK_counter_label.setStyleSheet("color: #3FDA68;\n"
"font-weight: bold;\n"
"font-size: 14px;\n"
"border:none;\n"
"")
        self.OK_counter_label.setText("")
        self.OK_counter_label.setScaledContents(False)
        self.OK_counter_label.setObjectName("OK_counter_label")
        self.horizontalLayout_2.addWidget(self.OK_counter_label)
        self.NG_icon_label = QtWidgets.QLabel(self.counter)
        self.NG_icon_label.setStyleSheet("border:none;\n"
"")
        self.NG_icon_label.setText("")
        self.NG_icon_label.setPixmap(QtGui.QPixmap(":/icon/resources/base/fonts/fontawesome/times-circle_errorRed.png"))
        self.NG_icon_label.setObjectName("NG_icon_label")
        self.horizontalLayout_2.addWidget(self.NG_icon_label)
        self.NG_counter_label = QtWidgets.QLabel(self.counter)
        self.NG_counter_label.setStyleSheet("color: #E66643;\n"
"font-weight: bold;\n"
"font-size: 14px;\n"
"border:none;\n"
"")
        self.NG_counter_label.setText("")
        self.NG_counter_label.setObjectName("NG_counter_label")
        self.horizontalLayout_2.addWidget(self.NG_counter_label)
        self.verticalLayout_2.addWidget(self.counter)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        spacerItem12 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem12)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        spacerItem13 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem13)

        self.retranslateUi(inspection)
        self.result.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(inspection)

    def retranslateUi(self, inspection):
        _translate = QtCore.QCoreApplication.translate
        inspection.setWindowTitle(_translate("inspection", "Form"))
        self.inspect_button.setText(_translate("inspection", "Take Photo"))
        self.inspect_existing_image_button.setText(_translate("inspection", "Photo Library"))
        self.default_label.setText(_translate("inspection", "The inspection result <br/> is displayed here."))
        self.OK_message_label.setText(_translate("inspection", "OK"))
        self.NG_message_label.setText(_translate("inspection", "NG"))
        self.ng_score.setText(_translate("inspection", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.total_header_label.setText(_translate("inspection", "Total"))

from view.q_camera_view_finder_with_guide import QCameraViewFinderWithGuide
from qrc import icon_rc
