from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'date_posted',
            'thumbnail_url',
        ]
        labels = {
            'name': 'Título',
            'date_posted': 'Data da Publicação',
            'thumbnail_url': 'URL da thumbnail',
        }