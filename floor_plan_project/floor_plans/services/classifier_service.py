from __future__ import division
from __future__ import print_function

from io import BytesIO
import os

from rest_framework import status
from floor_plan_project.floor_plans.services.image_downloader import ImageDownloader
from floor_plan_project.floor_plans.services.classifiers.classifiers import implemented_classifiers
from floor_plan_project.floor_plans.services.utils import get_image_record_id_from_url
from floor_plan_project.floor_plans.models import ImageRecord, Classification, Classifier

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class ClassificationService:

    def __init__(self, data):
        self.data = data

    def process_data(self, data=None):
        if data:
            self.data = data

        image_record_id = get_image_record_id_from_url(self.data["image_record"])
        classifier_id = get_image_record_id_from_url(self.data["classifier"])

        try:
            image_record = ImageRecord.objects.get(id=image_record_id)
        except ImageRecord.DoesNotExist:
            return self._create_response(errors="Image with id = {id} does not exist".format(id=image_record_id),
                                         status=status.HTTP_404_NOT_FOUND)

        if image_record.file:
            service_response = self.classify(image_record.file.read(), classifier_id)

        elif not image_record.file and image_record.origin_url:
            get_response = ImageDownloader.download_from_url(image_record.origin_url)

            if get_response.status_code == 200:
                service_response = self.classify(get_response.content, classifier_id)

                if service_response['status'] == status.HTTP_200_OK:
                    self._update_record_with_image(image_record, get_response.content)
            else:
                return self._create_response(
                    errors="Image url in image record with id = {id} is invalid".format(id=image_record_id),
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return self._create_response(
                errors="Image record with id = {id} is corrupted".format(id=image_record_id),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if service_response['status'] == status.HTTP_200_OK:
            self._delete_if_classified(image_record_id, classifier_id)

        return service_response

    def _delete_if_classified(self, image_record_id, classifier_id):
        """
        Check if image already classified by the algorithm
        :return: id of classification record if exist, None otherwise
        """
        try:
            classification = Classification.objects.get(image_record=image_record_id, classifier=classifier_id)
        except Classification.DoesNotExist:
            return

        classification.delete()

    def classify(self, file, classifier_id):
        try:
            classifier = Classifier.objects.get(id=classifier_id)
        except Classifier.DoesNotExist:
            return {'errors': 'Classifier with id = {id} does not exist', 'status': status.HTTP_404_NOT_FOUND}

        # get feature extractor and classifier
        extractor, cls = implemented_classifiers[classifier.algorithm]

        bytes_obj = BytesIO(file)
        bytes_obj.seek(0)

        img = Image.open(bytes_obj)
        features = extractor.process_image(img)
        res = cls.predict([features])

        if res[0] == 0:
            return self._create_response(classifier_res=False)
        else:
            return self._create_response(classifier_res=True)

    def _update_record_with_image(self, image_record, file):
        bytes_obj = BytesIO(file)
        bytes_obj.seek(0)

        name = os.path.basename(image_record.origin_url)
        image_record.file.save(name, bytes_obj)

    def _create_response(self, **kwargs):
        response = {'classifier_res': '', 'errors': '', 'status': status.HTTP_200_OK}
        for arg, val in kwargs.items():
            response[arg] = val
        return response


# extractor, cls = implemented_classifiers['rgb-svm']
# features = extractor.process_image_file("/home/rick/Projects/lun/floor_plan_project/floor_plan_project/floor_plans/services/test_pickle/folder2/412215064.jpg")
# print(cls.predict([features]))


