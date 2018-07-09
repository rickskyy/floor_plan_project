from rest_framework import serializers
from floor_plan_project.floor_plans.models import ImageRecord, Classification, Classifier
from floor_plan_project.floor_plans.services.image_downloader import ImageDownloader


class ClassifierSerializer(serializers.ModelSerializer):
    """
    Default classifier serializer including all the fields presented in model
    """
    url = serializers.HyperlinkedIdentityField(view_name="floor_plans:classifier-detail")

    class Meta:
        model = Classifier
        fields = ('url', 'id', 'images', 'algorithm', 'description',)


class ClassifierTypeSerializer(serializers.ModelSerializer):
    """
    Classifier serializer which omits image field which may contain large number of images
    returning only info about classifier
    """
    url = serializers.HyperlinkedIdentityField(view_name="floor_plans:classifier-detail")

    class Meta:
        model = Classifier
        fields = ('url', 'id', 'algorithm', 'description',)


class ClassificationPostSerializer(serializers.HyperlinkedModelSerializer):
    is_floor_plan = serializers.BooleanField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="floor_plans:classification-detail")
    image_record = serializers.HyperlinkedRelatedField(queryset=ImageRecord.objects.all(),
                                                       view_name='floor_plans:imagerecord-detail')
    classifier = serializers.HyperlinkedRelatedField(queryset=Classifier.objects.all(),
                                                     view_name='floor_plans:classifier-detail')

    class Meta:
        model = Classification
        fields = ('url', 'id', 'classifier', 'image_record', 'classified_at', 'is_floor_plan',)


class ClassificationGetSerializer(serializers.HyperlinkedModelSerializer):
    is_floor_plan = serializers.BooleanField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="floor_plans:classification-detail")
    image_record = serializers.HyperlinkedRelatedField(queryset=ImageRecord.objects.all(),
                                                       view_name='floor_plans:imagerecord-detail')
    classifier = ClassifierTypeSerializer(read_only=True)

    class Meta:
        model = Classification
        fields = ('url', 'id', 'classifier', 'image_record', 'classified_at', 'is_floor_plan',)


class ImageRecordSerializer(serializers.HyperlinkedModelSerializer):
    classifications = ClassificationGetSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="floor_plans:imagerecord-detail")

    class Meta:
        model = ImageRecord
        fields = ('url', 'id', 'uploaded_at', 'file', 'origin_url', 'classifications')

    def validate(self, attrs):
        """
        Check
        :param attrs: model attributes from request
        :return: same attrs or exception
        """
        if len(attrs) == 0 or \
            (('origin_url' in attrs and attrs['origin_url'] is None) and
             ('file' in attrs and attrs['file'] is None)):
            raise serializers.ValidationError("Either origin_url or file objects might be included!")

        if 'origin_url' in attrs:
            response = ImageDownloader.download_from_url(attrs['origin_url'])
            if response.status_code != 200:
                raise serializers.ValidationError('Provided url is invalid')

        return attrs
