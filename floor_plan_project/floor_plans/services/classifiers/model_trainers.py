import pickle
from abc import ABC

from io import BytesIO
from floor_plan_project.floor_plans.services.image_downloader import ImageDownloader
from floor_plan_project.floor_plans.services.feature_extractor import RGBBasedFeatureExtractor

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import svm
from sklearn import metrics
import os
from os.path import dirname
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

NOT_FLOOR_IMAGES_FEATURES = [
    os.path.join(dirname(dirname(dirname(__file__))), 'training_data', 'dumped_features', 'apartments.p'),
    os.path.join(dirname(dirname(dirname(__file__))), 'training_data', 'dumped_features', 'rieltor.p'),
    os.path.join(dirname(dirname(dirname(__file__))), 'training_data', 'dumped_features', 'windows.p'),
    # os.path.join(dirname(dirname(dirname(__file__))), 'training_data', 'dumped_features', 'building_images.p')
]


FLOOR_IMAGES_FEATURES = [
    os.path.join(dirname(dirname(dirname(__file__))), 'training_data', 'dumped_features', 'training_images.p'),
    os.path.join(dirname(dirname(dirname(__file__))), 'training_data', 'dumped_features', 'colorful_plans.p')
]


class BaseModelTrainer(ABC):

    def train(self, *args, **kwargs):
        raise NotImplementedError


class SVMTrainer(BaseModelTrainer):

    def train(self, features_a, features_b, print_metrics=True):
        """
        Choosing the best parameters and trains a classifier using skleran.svm.SVC module
        :param features_a: list of files with pickled features (floor plans)
        :param features_b: list of files with pickled features (other)
        :param print_metrics: True or False for printing to console statistics about best training results
                              http://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html
        :return: sklearn.svm.SVC object
        """

        training_a = self.get_features_from_files(features_a)
        training_b = self.get_features_from_files(features_b)
        print('First group: ' + str(len(training_a)))
        print('Zero group: ' + str(len(training_b)))

        data = training_a + training_b
        target = [1] * len(training_a) + [0] * len(training_b)
        x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.20)

        parameters = {'kernel': ['linear', 'rbf'], 'C': [1, 5, 10, 100, 1000],
                      'gamma': [1, 0.5, 0.1, 0.01, 0.001, 0.0001]}

        # using GridSearch to find best parameters
        # http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
        clf = GridSearchCV(svm.SVC(), parameters).fit(x_train, y_train)
        classifier = clf.best_estimator_

        if print_metrics:
            print('Best parameters:', clf.best_params_, '\n')
            print('Classifier: ', clf.best_estimator_, '\n')
            print('Best classifier score:')
            print(metrics.classification_report(y_test, classifier.predict(x_test)))
        return classifier

    def get_features_from_files(self, paths):
        fv = []
        for path in paths:
            fv.extend(pickle.load(open(path, 'rb')))

        return fv

    def dump(self, path, classifier):
        with open(path, 'wb') as f:
            pickle.dump(classifier, f)


# if __name__ == '__main__':
#     classifier = SVMTrainer().train(FLOOR_IMAGES_FEATURES, NOT_FLOOR_IMAGES_FEATURES)

    # # Usage Example 1
    # test_features = pickle file with features
    # classifier.predict([test_features])

    # # Usage Example 2
    # url = "http://storage.googleapis.com/lun_ua/412215070.jpg"
    # response = ImageDownloader.download_from_url(url=url)
    #
    # if response.status_code == 200:
    #     bytes_obj = BytesIO(response.content)
    #     bytes_obj.seek(0)
    #
    #     img = Image.open(bytes_obj)
    #     features = RGBBasedFeatureExtractor().process_image(img)
    #     res = classifier.predict([features])
    #     print(res)
