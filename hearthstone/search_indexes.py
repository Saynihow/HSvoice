from haystack import indexes
from .models import Image


class ImageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    manavalue = indexes.CharField(model_attr='manavalue')
    attackvalue = indexes.CharField(model_attr='attackvalue')
    bloodvalue = indexes.CharField(model_attr='bloodvalue')
    version = indexes.CharField(model_attr='version')
    race = indexes.CharField(model_attr='race')

    def get_model(self):
        return Image

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()