﻿from fbs_runtime.application_context.PyQt5 import ApplicationContext
from math import ceil
from PyQt5.QtWidgets import QWidget, QToolTip
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie, QCursor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
import seaborn as sns
from view.ui.test import Ui_Test
from model.learning_model import LearningModel
from model.test_report_model import TestReportModel
from model.project import Project


class TestWidget(QWidget):
    def __init__(self):
        self.learning_model = LearningModel.default()  # initの引数で渡したい…

        super().__init__()
        self.ui = Ui_Test()
        self.ui.setupUi(self)

        appctxt = ApplicationContext()
        loader_gif_path = appctxt.get_resource('images/loader.gif')
        self.loader = QMovie(loader_gif_path)
        self.loader.setScaledSize(QSize(30, 8))
        self.ui.loading_gif_label.setMovie(self.loader)
        self.loader.start()

        self.ui.about_threshold_button.clicked.connect(self.on_clicked_about_threshold_button)
        self.ui.threshold_slider.valueChanged.connect(self.on_threshold_changed)
        self.ui.details_button.clicked.connect(self.on_clicked_details_button)

        self.distance_figure: Figure = plt.figure(figsize=(3.7, 2.3))
        self.distance_canvas = FigureCanvas(self.distance_figure)
        self.distance_canvas.setParent(self.ui.distance_chart_widget)
        # sns.set_palette(['#3FDA68', '#E66643'])

        performance_figure = Figure(figsize=(3, 3))
        self.performance_axes: Axes = performance_figure.add_subplot(111)
        performance_figure.patch.set_alpha(0)
        self.performance_axes.set_position(pos=[0, 0.1, 1, 1])  # FIXME: adjust position automatically
        self.performance_center_circle = plt.Circle(xy=(0, 0), radius=0.6, fc='#F5F5F5', linewidth=1.25)
        self.performance_canvas = FigureCanvas(performance_figure)
        self.performance_canvas.setParent(self.ui.performance_chart_widget)

        self.test_report_widget = TestReportWidget()

    def show_loading(self):
        self.ui.stacked_widget.setCurrentIndex(0)

    def reload_test_results(self, show_training=False):
        self.ui.stacked_widget.setCurrentIndex(1)  # TODO: Refactor
        results = self.learning_model.test_results
        self.show_overfitting_alert(results.t_value)

        # reload distance chart
        plt.clf()
        sns.set()
        sns.set_context("paper")
        if show_training:
            sns.distplot(results.distances_of_train_images, kde=False, rug=False, hist_kws=dict(alpha=1, linewidth=0), label='TRAIN OK', color='b')
        sns.distplot(results.distances_of_ok_images, kde=False, rug=False, hist_kws=dict(alpha=1, linewidth=0), label='TEST OK', color='g')  # FIXME: label
        sns.distplot(results.distances_of_ng_images, kde=False, rug=False, hist_kws=dict(alpha=1, linewidth=0), label='TEST NG', color='r')
        plt.legend()
        self.threshold_line: Line2D = plt.axvline(x=self.learning_model.threshold,
                                                     color='#FFA00E',
                                                     linestyle='dashed')

        # preset slider value
        distance_range = results.max_distance - results.min_distance
        if distance_range != 0:
            slider_min = self.ui.threshold_slider.minimum()
            slider_range = self.ui.threshold_slider.maximum() - slider_min
            threshold = self.learning_model.threshold
            slider_value = ceil(slider_min + (threshold - results.min_distance) * slider_range / distance_range)
        else:
            slider_value = self.ui.threshold_slider.maximum()
        self.ui.threshold_slider.setValue(slider_value)

        self.__reload_performance()

    def __reload_performance(self):
        results = self.learning_model.test_results
        self.performance_axes.clear()
        accuracy_percentage = results.accuracy * 100
        false_positive_percentage = results.false_positive_rate * 100
        false_negative_percentage = results.false_negative_rate * 100
        self.performance_axes.pie(x=[accuracy_percentage, false_positive_percentage, false_negative_percentage],
                                  colors=['#3FDA68', '#FFA00E', '#E66643'],
                                  startangle=90,
                                  counterclock=False)
        self.performance_axes.add_artist(self.performance_center_circle)
        self.performance_canvas.draw()

        self.ui.accuracy_label.setText(f'{round(accuracy_percentage, 1)}%')
        self.ui.false_positive_rate_label.setText(f'{round(false_positive_percentage, 1)}%')
        self.ui.false_negative_rate_label.setText(f'{round(false_negative_percentage, 1)}%')

    def on_clicked_about_threshold_button(self):
        QToolTip.showText(QCursor.pos(), self.ui.about_threshold_button.toolTip())



    def on_threshold_changed(self):
        # calculate threshold
        slider_value = self.ui.threshold_slider.value()
        results = self.learning_model.test_results
        slider_min = self.ui.threshold_slider.minimum()
        slider_range = self.ui.threshold_slider.maximum() - slider_min
        distance_range = results.max_distance - results.min_distance
        new_threshold = results.min_distance + (slider_value - slider_min) * distance_range / slider_range

        # update threshold
        self.learning_model.threshold = new_threshold
        self.__reload_performance()

        # display threshold
        thresh_round = round(self.learning_model.threshold, 4)
        self.ui.threshold_label.setText(str(thresh_round))
        self.threshold_line.set_xdata(self.learning_model.threshold)
        self.threshold_line.axes.figure.canvas.draw()

        self.test_report_widget.reload_html()

    def show_overfitting_alert(self, t_value):
        if t_value > 1.96:
            self.ui.overfitting_alert_label.setEnabled(True)
            self.ui.overfitting_alert_label.setVisible(True)
        else:
            self.ui.overfitting_alert_label.setEnabled(False)
            self.ui.overfitting_alert_label.setVisible(False)

    def on_clicked_details_button(self):
        self.test_report_widget.reload_html()
        self.test_report_widget.show()
        self.test_report_widget.activateWindow()
        self.test_report_widget.raise_()


class TestReportWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'性能評価 詳細 - {Project.project_name()}')
        self.test_report_model = TestReportModel()

        self.web_view = QWebEngineView(self)
        html_size = QSize(890, 390)
        self.web_view.setFixedSize(html_size)
        self.setFixedSize(html_size)

    def reload_html(self):
        html = self.test_report_model.generate_test_details()
        self.web_view.setHtml(html)
