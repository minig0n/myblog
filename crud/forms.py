from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'thumbnail_url',
            'content',
        ]
        labels = {
            'name': 'Título',
            'thumbnail_url': 'URL da thumbnail',
            'content': 'Conteúdo em HTML',
        }