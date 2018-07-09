from django.db import models
from django.urls import reverse


class ImageRecord(models.Model):

    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(null=True)
    origin_url = models.URLField(null=True)

    class Meta:
        ordering = ('uploaded_at', 'id')

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of an Image
        """
        return reverse('floor_plans:imagerecord-detail', args=[str(self.id)])


class Classification(models.Model):

    image_record = models.ForeignKey('ImageRecord', related_name='classifications', on_delete=models.CASCADE)
    classifier = models.ForeignKey('Classifier', on_delete=models.CASCADE)
    classified_at = models.DateTimeField(auto_now_add=True)
    is_floor_plan = models.BooleanField()

    class Meta:
        ordering = ('classified_at',)


class Classifier(models.Model):

    images = models.ManyToManyField(ImageRecord, through=Classification)
    algorithm = models.CharField(max_length=50)
    description = models.CharField(max_length=512)

