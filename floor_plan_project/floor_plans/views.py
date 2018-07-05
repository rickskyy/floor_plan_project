from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status, generics

from floor_plan_project.floor_plans.models import ImageRecord, Classification, Classifier
from floor_plan_project.floor_plans.serializers import ImageRecordSerializer, ClassificationSerializer, \
    ClassifierSerializer
from floor_plan_project.floor_plans.services.classifier_service import ClassificationService


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'image_records': reverse('floor_plans:imagerecord-list', request=request, format=format),
        'classifications': reverse('floor_plans:classification-list', request=request, format=format),
        'classifiers': reverse('floor_plans:classifier-list', request=request, format=format)
    })


class ImageRecordList(generics.ListCreateAPIView):
    """
    List all uploaded images, or upload an image.
    """
    queryset = ImageRecord.objects.all()
    serializer_class = ImageRecordSerializer
    pagination_class = PageNumberPagination


class ImageRecordDetail(generics.RetrieveAPIView):
    """
    Get image details
    """
    queryset = ImageRecord.objects.all()
    serializer_class = ImageRecordSerializer


class ClassificationList(generics.ListCreateAPIView):
    """
    List all classified images, or classify an image.
    """
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ClassificationSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ClassificationSerializer(data=request.data, context={'request': request})
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     documents = Document.objects.all()
    #     context['documents'] = documents
    #     return context


class ClassificationDetail(generics.RetrieveAPIView):
    """
    Get classified image details
    """
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer


class ClassifierList(generics.ListAPIView):
    """
    List all classifiers images.
    """
    queryset = Classifier.objects.all()
    serializer_class = ClassifierSerializer
    pagination_class = PageNumberPagination


class ClassifierDetail(generics.RetrieveAPIView):
    """
    Get classifier details
    """
    queryset = Classifier.objects.all()
    serializer_class = ClassifierSerializer
    pagination_class = PageNumberPagination

# class DocumentCreateView(CreateView):
#     model = Document
#     fields = ['upload', ]
#     success_url = reverse_lazy('file-upload')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         documents = Document.objects.all()
#         context['documents'] = documents
#         return context
