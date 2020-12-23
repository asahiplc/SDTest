# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ai_optimization.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AIOptimization(object):
    def setupUi(self, AIOptimization):
        AIOptimization.setObjectName("AIOptimization")
        AIOptimization.resize(842, 532)
        AIOptimization.setMinimumSize(QtCore.QSize(780, 321))
        font = QtGui.QFont()
        font.setPointSize(9)
        AIOptimization.setFont(font)
        AIOptimization.setStyleSheet("")
        self.main_area = QtWidgets.QVBoxLayout(AIOptimization)
        self.main_area.setObjectName("main_area")
        self.tab_widget = QtWidgets.QTabWidget(AIOptimization)
        self.tab_widget.setStyleSheet("")
        self.tab_widget.setObjectName("tab_widget")
        self.dataset_tab = DatasetWidget()
        self.dataset_tab.setStyleSheet("")
        self.dataset_tab.setObjectName("dataset_tab")
        self.tab_widget.addTab(self.dataset_tab, "")
        self.main_area.addWidget(self.tab_widget)

        self.retranslateUi(AIOptimization)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AIOptimization)

    def retranslateUi(self, AIOptimization):
        _translate = QtCore.QCoreApplication.translate
        AIOptimization.setWindowTitle(_translate("AIOptimization", "Learning"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.dataset_tab), _translate("AIOptimization", "Dataset"))

from view.dataset import DatasetWidget
from view.test import TestWidget
