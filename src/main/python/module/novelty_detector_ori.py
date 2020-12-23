import glob
import os
import pathlib
import numpy as np

from sklearn.decomposition import PCA
from keras import backend as K
from keras.models import Model
from keras.layers import GlobalAveragePooling2D, GlobalMaxPooling2D, Flatten
from model.project import Project
import numpy as np
import imageio
import skimage.transform
import joblib
import pyod

class NoveltyDetector:

    def __init__(self, nth_layer=18, nn_name='lobe', detector_name='svm', pool=None, pca_n_components=None):
        """
        Extract feature by neural network and detector train normal samples then predict new data
        nn_name: 'Xception', 'ResNet'(Default), 'InceptionV3',
        'InceptionResNetV2', 'MobileNet', 'MobileNetV2', 'DenseNet', 'NASNet'
        detector_name: 'RobustCovariance', 'IsolationForest, 'LocalOutlierFactor, ABOD, kNN(Default)'
        """
        self.nth_layer = nth_layer
        self.nn_name = nn_name
        self.pool = pool
        self.pca_n_components = pca_n_components
        self.input_shape = None
        self.pretrained_nn = None
        self.extracting_model = None

        K.clear_session()

        detector_name_lower = detector_name.lower()
        if detector_name_lower == 'robustcovariance':
            self.detector_name = 'rc'
            from sklearn.covariance import EllipticEnvelope
            self.clf = EllipticEnvelope()
            print('Novelty Detector: Robust covariance')
        elif detector_name_lower in ['localoutlierfactor', 'lof']:
            self.detector_name = 'lof'
            from sklearn.neighbors import LocalOutlierFactor
            self.clf = LocalOutlierFactor(novelty=True)
            print('Novelty Detector: Local Outlier Factor')
        elif detector_name_lower in ['abod', 'fastabod', 'anglebasedoutlierdetection']:
            self.detector_name = 'abod'
            from pyod.models.abod import ABOD
            self.clf = ABOD()
            print('Novelty Detector: Angle Based Outlier Detection')
        elif detector_name_lower in ['iforest', 'isolationforest']:
            self.detector_name = 'iforest'
            from sklearn.ensemble import IsolationForest
            self.clf = IsolationForest()
            print('Novelty Detector: Isolation Forest')
        elif detector_name_lower in ['knn', 'median_knn']:
            self.detector_name = 'median_kNN'
            from pyod.models.knn import KNN
            self.clf = KNN(method='median', contamination=0.1)
            print('Novelty Detector: Median K Nearest Neighbors')
        elif detector_name_lower == 'svm':
            from sklearn.svm import OneClassSVM
            self.clf = OneClassSVM(gamma='scale')
            print('SVM')
        else:
            print(self.detector_name_lower)
            raise ValueError

    def _load_NN_model(self, input_shape=(229, 229, 3)):
        """
        This method should be called after loading images to set input shape.
        """
        
        self.input_shape = input_shape
        print('Input image size is', self.input_shape)

        if self.nn_name == 'Xception':
            from keras.applications.xception import Xception
            pretrained_func = Xception
            print('Neural Network: {}'.format(self.nn_name))
        elif self.nn_name == 'InceptionV3':
            from keras.applications.inception_v3 import InceptionV3
            pretrained_func = InceptionV3
            print('Neural Network: {}'.format(self.nn_name))
        elif self.nn_name == 'InceptionResNetV2':
            from keras.applications.inception_resnet_v2 import InceptionResNetV2
            pretrained_func = InceptionResNetV2
            print('Neural Network: {}'.format(self.nn_name))
        elif self.nn_name == 'MobileNet':
            from keras.applications.mobile_net import MobileNet
            pretrained_func = MobileNet
            print('Neural Network: {}'.format(self.nn_name))
        elif self.nn_name == 'MobileNetV2':
            from keras.applications.mobilenet_v2 import MobileNetV2
            pretrained_func = MobileNetV2
            print('Neural Network: {}'.format(self.nn_name))
        elif self.nn_name == 'DenseNet':
            from keras.applications.densenet import DenseNet201
            pretrained_func = DenseNet201
            print('Neural Network: {}'.format(self.nn_name))
        elif self.nn_name == 'NASNet':
            from keras.applications.nasnet import NASNetLarge
            pretrained_func = NASNetLarge
            print('Neural Network: {}'.format(self.nn_name))
        elif self.nn_name == 'vgg':
            from keras.applications.vgg16 import VGG16
            pretrained_func = VGG16
            print('VGG')
        elif self.nn_name == 'lobe':
            from lobe import ImageModel
            model = ImageModel.load(Project.project_path() + '/models/')
            print('lobe')
        elif self.nn_name == 'ResNet':
            from keras.applications.resnet50 import ResNet50
            pretrained_func = ResNet50
            print('Neural Network: {}'.format(self.nn_name))

        self.extracting_model = model
        return self.extracting_model

    def fit(self, imgs):
        self._load_NN_model(imgs[0].shape)
        feature = self.extracting_model.predict(imgs)
        if self.pca_n_components:
            pca = PCA(n_components=self.pca_n_components)
            feature = pca.fit_transform(feature)
        self.clf.fit(feature)

    def fit_paths(self, paths):
        imgs = self._read_imgs(paths)
        self.fit(imgs)
        
    def fit_in_dir(self, dir_path, kernel='rbf', nu=0.05, gamma='scale'):
        """
        Fit to images in a directory. Training can take minutes depending on a dataset.
        dir_path: A path to directory containing training images
        """
        paths = self._get_paths_in_dir(dir_path)
        self.fit_paths(paths)

    def predict(self, imgs):
        """ Return the list of score. Higher the score, the more likely normal.
        Keyword arguments:
        paths -- list of image paths like [./dir/img1.jpg, ./dir/img2.jpg, ...]
        """
        if self.extracting_model is None:
            self._load_NN_model(imgs[0].size)
        feature = self.extracting_model.predict(imgs[0])
        print(feature.prediction)
        if self.pca_n_components:
            pca = PCA(n_components=self.pca_n_components)
            feature = pca.fit_transform(feature)
        predicted_scores = feature.labels[0][1]
        print(predicted_scores)

        if self.clf.__module__.startswith('pyod.models'):
            # Tricky, the higher pyod's predicts score, the more likely anormaly. We want higher the score,  more likely normal.
            predicted_scores *= -1
        return predicted_scores, feature.prediction

    def predict_paths(self, paths):
        imgs = self._read_imgs(paths)
        return self.predict(imgs)

    def predict_in_dir(self, dir_path):
        dir_path = os.path.expanduser(dir_path)
        paths = self._get_paths_in_dir(dir_path)
        return paths, self.predict_paths(paths)

    def _read_imgs(self, paths):
        paths = [ os.path.expanduser(path) for path in paths]
        if self.input_shape is None:
            self.input_shape = imageio.imread(paths[0], as_gray=False, pilmode='RGB').shape
        imgs = []
        from PIL import Image
        for path in paths:
            img = Image.open(path)
            imgs.append(img)
        return imgs

    def _get_paths_in_dir(self, dir_path):
        dir_path = os.path.expanduser(dir_path)
        if not os.path.exists(dir_path):
            raise IOError(dir_path, 'does not exist')
        imgs = []
        paths = glob.glob(os.path.join(dir_path, '*.jpg'))
        paths.extend(glob.glob(os.path.join(dir_path, '*.jpeg')))
        paths.extend(glob.glob(os.path.join(dir_path, '*.png')))
        paths.extend(glob.glob(os.path.join(dir_path, '*.gif')))
        paths.extend(glob.glob(os.path.join(dir_path, '*.bmp')))
        return paths

    def save(self, path):
        path = os.path.expanduser(path)
        joblib.dump(self.clf, path, compress=True)

    def load(self, path):
        path = os.path.expanduser(path)
        self.clf = joblib.load(path)
        return self
