from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Post, Review, Category


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

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            'text',
        ]
        labels = {
            'text': 'Comentário',
        }

# class CategoryForm(CheckboxSelectMultiple):
#     class Meta:
#         model = Category
#         fields = [
#             '',
#         ]
#         labels = {
#             ''
#         }