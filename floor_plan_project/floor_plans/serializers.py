from rest_framework import serializers
from floor_plan_project.floor_plans.models import ImageRecord, Classification, Classifier


class ImageRecordSerializer(serializers.HyperlinkedModelSerializer):
    classifications = serializers.HyperlinkedRelatedField(many=True,
                                                          view_name='floor_plans:classification-detail',
                                                          read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="floor_plans:imagerecord-detail")

    class Meta:
        model = ImageRecord
        fields = ('url', 'id', 'uploaded_at', 'file', 'origin_url', 'classifications')

    # TODO restrict posting images without either url and file


class ClassificationSerializer(serializers.HyperlinkedModelSerializer):
    is_floor_plan = serializers.BooleanField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="floor_plans:classification-detail")
    image_record = serializers.HyperlinkedRelatedField(queryset=ImageRecord.objects.all(),
                                                       view_name='floor_plans:imagerecord-detail')
    classifier = serializers.HyperlinkedRelatedField(queryset=Classifier.objects.all(),
                                                     view_name='floor_plans:classifier-detail')

    class Meta:
        model = Classification
        fields = ('url', 'id', 'classifier', 'image_record', 'classified_at', 'is_floor_plan',)


class ClassifierSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="floor_plans:classifier-detail")
    # images = serializers.HyperlinkedRelatedField(queryset=ImageRecord.objects.all(),
    #                                              view_name='floor_plans:imagerecord-detail')

    class Meta:
        model = Classifier
        fields = ('url', 'id', 'images', 'algorithm', 'description',)
