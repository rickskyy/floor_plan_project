from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status, generics, exceptions

from floor_plan_project.floor_plans.models import ImageRecord, Classification, Classifier
from floor_plan_project.floor_plans.pagination import PageNumberExtendedPagination
from floor_plan_project.floor_plans.serializers import ImageRecordSerializer, ClassificationGetSerializer, \
    ClassifierSerializer, ClassifierTypeSerializer, ClassificationPostSerializer
from floor_plan_project.floor_plans.services.classifier_service import ClassificationService


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'image_records': reverse('floor_plans:imagerecord-list', request=request, format=format),
        'classifications': reverse('floor_plans:classification-list', request=request, format=format),
        'classifiers': reverse('floor_plans:classifier-list', request=request, format=format),
        'classifiers-types': reverse('floor_plans:classifier-types-list', request=request, format=format)
    })


class MethodSerializerView(object):
    """
    Utility class for get different serializer class by method.
    For example:
    method_serializer_classes = {
        ('GET', ): MyModelListViewSerializer,
        ('PUT', 'PATCH'): MyModelCreateUpdateSerializer
    }
    """
    method_serializer_classes = None

    def get_serializer_class(self):
        assert self.method_serializer_classes is not None, (
            'Expected view %s should contain method_serializer_classes '
            'to get right serializer class.' %
            (self.__class__.__name__, )
        )
        for methods, serializer_cls in self.method_serializer_classes.items():
            if self.request.method in methods:
                return serializer_cls

        raise exceptions.MethodNotAllowed(self.request.method)


class ImageRecordList(generics.ListCreateAPIView):
    """
    Get list of images or upload an image.
    """
    queryset = ImageRecord.objects.all().order_by("-uploaded_at")
    serializer_class = ImageRecordSerializer
    pagination_class = PageNumberExtendedPagination


class ImageRecordDetail(generics.RetrieveAPIView):
    """
    Get image details.
    """
    queryset = ImageRecord.objects.all()
    serializer_class = ImageRecordSerializer


class ClassificationList(MethodSerializerView, generics.ListCreateAPIView):
    """
    List all classified images, or classify an image.
    Managing representation by using GetSerializer to get all important information about the image
    including classification and classifiers details to avoid additional get requests when displaying data.
    At same time it is essential to create classifications by just referring the classifier and image
    instances so the PostSerializer is used.
    """
    queryset = Classification.objects.all()
    pagination_class = PageNumberExtendedPagination
    method_serializer_classes = {
        ('GET', ): ClassificationGetSerializer,
        ('POST', ): ClassificationPostSerializer,
    }

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ClassificationGetSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ClassificationPostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            response_data = ClassificationService(request.data).process_data()
            if response_data['classifier_res'] is not None and not response_data['errors']:
                serializer.save(is_floor_plan=response_data['classifier_res'])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif response_data['errors']:
                return Response(response_data['errors'], status=response_data['status'])
            else:
                return Response('Something bad happened', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassificationDetail(generics.RetrieveAPIView):
    """
    Get details about specific classification
    """
    queryset = Classification.objects.all()
    serializer_class = ClassificationGetSerializer


class ClassifierList(generics.ListAPIView):
    """
    List all image classifiers.
    """
    queryset = Classifier.objects.all()
    serializer_class = ClassifierSerializer
    pagination_class = PageNumberExtendedPagination


class ClassifierTypeList(generics.ListAPIView):
    """
    List all classifiers without listed images. No pagination due to assumption of not a big number of classifiers
    """
    queryset = Classifier.objects.all()
    serializer_class = ClassifierTypeSerializer
    pagination_class = None


class ClassifierDetail(generics.RetrieveAPIView):
    """
    Get classifier details
    """
    queryset = Classifier.objects.all()
    serializer_class = ClassifierSerializer
    pagination_class = PageNumberExtendedPagination
