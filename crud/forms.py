from django.forms import ModelForm, MultipleChoiceField, CheckboxSelectMultiple
from .models import Post, Review, Category


class PostForm(ModelForm):
    cat = []
    category_list = Category.objects.all()
    for category in category_list:
        cat.append((category.pk, category.name))

    category_list = cat

    category_post = MultipleChoiceField(label='Categorias', 
                                        choices=category_list, 
                                        widget=CheckboxSelectMultiple(),
                                        required=False)

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
