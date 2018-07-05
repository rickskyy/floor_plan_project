from __future__ import division
from __future__ import print_function

from abc import ABC, abstractmethod

from PIL import Image
import pickle
import os
from matplotlib.pyplot import plot
import matplotlib.pyplot as plt
import multiprocessing


class BaseFeatureExtractor(ABC):

    @abstractmethod
    def process_image(self, *args, **kwargs):
        raise NotImplementedError

    def process_directories(self, source_directory_path, destination_folder_path, n_processes):
        """
        Extract feature vectors from the given list of directories with images
        and pickle the lists into files stored in the destination folder
        :param source_directory_path: root directory containing other directories to process,
                                      only process first level subdirectories
        :param destination_folder_path: folder to write the result
        """
        if not os.path.isdir(source_directory_path):
            raise ValueError(source_directory_path + "is not a directory")

        if not os.path.isdir(destination_folder_path):
            raise ValueError(destination_folder_path + "is not a directory")

        subfolders = next(os.walk(source_directory_path))[1]
        if len(subfolders) == 0:
            raise ValueError(source_directory_path + "does not contain any subdirectories to process")

        source_folders, destination_folders = [], []
        for folder in subfolders:
            source_folders.append(os.path.join(source_directory_path, folder))
            destination_folders.append(os.path.join(destination_folder_path, folder + ".p"))

        # TODO not super clever solution because the process locked to one directory
        # but it was sufficient for me to boost the feature extraction process
        console_lock = multiprocessing.Lock()
        pool = multiprocessing.Pool(initializer=self._init_pool, initargs=(console_lock,), processes=n_processes)
        pool.map(self._process_directory_task, iterable=zip(source_folders, destination_folders))

    def _process_directory_task(self, params):
        source_file, destination_file = params

        with lock:
            print("Extracting features from " + source_file + " ...")
        feature_vectors = self.process_directory(source_file)

        with lock:
            print("Saving " + destination_file + " ...")
        pickle.dump(feature_vectors, open(destination_file, 'wb'))

    def process_directory(self, directory):
        """
        Returns an array of feature vectors for all the image files in a
        directory (and all its subdirectories). Symbolic links are ignored.
        :param directory: path to the directory
        :return: list of list of float: a list of feature vectors.
        """
        training = []
        for root, _, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                img_feature = self.process_image_file(file_path)
                if img_feature:
                    training.append(img_feature)
        return training

    def process_image_file(self, image_path):
        """
        Given an image path it returns its feature vector.
        :param image_path: string path of the image file to process.
        :return: list of float: feature vector on success, None otherwise.
        """
        try:
            image = Image.open(image_path)
            return self.process_image(image)
        except IOError:
            return

    # TODO better use SyncManager but this is faster to implement
    def _init_pool(self, l):
        global lock
        lock = l

    def dump(self, path, feautures_list):
        with open(path, 'wb') as f:
            pickle.dump(feautures_list, f)

    def plot_feature(self, feature):
        p = plot(feature)
        plt.show()


class RGBBasedFeatureExtractor(BaseFeatureExtractor):

    def process_image(self, image, blocks=4):
        """
        Reference: http://www.ippatsuman.com/2014/08/13/day-and-night-an-image-classifier-with-scikit-learn/
        Given a PIL Image object it returns its feature vector.
        :param image: (PIL.Image) image to process.
        :param blocks: number of block to subdivide the RGB space into.
        :return: list of feature vector if successful. None if the image is not RGB.
        """

        if not image.mode == 'RGB':
            return None
        feature = [0] * blocks * blocks * blocks
        pixel_count = 0
        for pixel in image.getdata():
            ridx = int(pixel[0]/(256/blocks))
            gidx = int(pixel[1]/(256/blocks))
            bidx = int(pixel[2]/(256/blocks))
            idx = ridx + gidx * blocks + bidx * blocks * blocks
            feature[idx] += 1
            pixel_count += 1
        return [x/pixel_count for x in feature]


# source = "/home/rick/Projects/lun/floor_plan_project/floor_plan_project/floor_plans/services/training"
# dest = "/home/rick/Projects/lun/floor_plan_project/floor_plan_project/floor_plans/services/dumped_features"
# csv_file = "/home/rick/Projects/lun/image_urls.csv"
# RGBBasedFeatureExtractor().process_directories(source, dest, 2)


# RGBBasedFeatureExtractor().process_csv_file(csv_file)
