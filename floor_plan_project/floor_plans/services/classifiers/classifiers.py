import os
import pickle

from floor_plan_project.floor_plans.services.feature_extractor import RGBBasedFeatureExtractor



RGB_FEATURE = os.path.join(os.path.dirname(__file__), "dumps", "rgb_features_classifier.p")

rgb_feature_classifier = pickle.load(open(RGB_FEATURE, 'rb'))

implemented_classifiers = {
    'rgb-svm': (RGBBasedFeatureExtractor(), rgb_feature_classifier),
}
