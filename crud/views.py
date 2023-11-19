from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Review, Category
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect

import datetime
import pytz

from .forms import PostForm, ReviewForm


# Create your views here.

def about(request):
    context = {}
    return render(request, 'crud/about.html', context)

class PostListView(generic.ListView):
    model = Post
    ordering = ['-date_posted']

    template_name = 'crud/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'last_viewed' in self.request.session:
            context['last_posts'] = []
            for post_id in self.request.session['last_viewed']:
                new_object = get_object_or_404(Post, pk=post_id)
                if new_object.active and new_object not in context['last_posts']:
                    context['last_posts'].append(new_object)
        return context

def detail_category(request, category_id):
    category_detail = get_object_or_404(Category, pk=category_id)
    context = {'category': category_detail}
    return render(request, 'crud/category-list.html', context)
    
class CategoryListView(generic.ListView):
    model = Category
    ordering = ['name']

    template_name = 'crud/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'last_viewed' in self.request.session:
            context['last_categorys'] = []
            for post_id in self.request.session['last_viewed']:
                new_object = get_object_or_404(Post, pk=post_id)
                if new_object.active and new_object not in context['last_categorys']:
                    context['last_categorys'].append(new_object)
        return context
    
def detail_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if 'last_viewed' not in request.session:
        request.session['last_viewed'] = []
    request.session['last_viewed'] = [post_id
                                      ] + request.session['last_viewed']
    if len(request.session['last_viewed']) > 5:
        request.session['last_viewed'] = request.session['last_viewed'][:-1]
    context = {'post': post}
    return render(request, 'crud/detail.html', context)

@login_required
@permission_required('posts.add_post')
def delete_post(request, post_id=None):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        post.active = False
        post.save()
        return HttpResponseRedirect(reverse('crud:index'))
    
    context = {'post': post}
    return render(request, 'crud/delete.html', context)

@login_required
@permission_required('posts.add_post')
def create_post(request):

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = Post()
            post.name = post_form.cleaned_data['name']
            post.thumbnail_url = post_form.cleaned_data['thumbnail_url']
            post.content = post_form.cleaned_data['content']

            category_list = post_form.cleaned_data['category_post']
            print(category_list)
            
            post.active = True

            current_datetime = datetime.datetime.now()

            post.date_posted = current_datetime

            post.save()

            for cat in category_list:
                category = get_object_or_404(Category, pk=int(cat))
                category.posts.add(post)
            
            return HttpResponseRedirect(
                reverse('crud:detail', args=(post.pk, )))
        
    else:
        post_form = PostForm(initial= {'content': '<p></p>\n<img src="" alt="img_1" style="max-width:400px;">'})

    context = {'post_form': post_form}
    return render(request, 'crud/create.html', context)

@login_required
@permission_required('posts.add_post')
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post.name = form.cleaned_data['name']
            post.thumbnail_url = form.cleaned_data['thumbnail_url']
            post.content = form.cleaned_data['content']

            post.save()

            return HttpResponseRedirect(
                reverse('crud:detail', args=(post.id, )))
    else:
        form = PostForm(
            initial={
                'name': post.name,
                'date_posted': post.date_posted,
                'thumbnail_url': post.thumbnail_url,
                'content': post.content,
            })

    context = {'post': post, 'form': form}
    return render(request, 'crud/update.html', context)

@login_required
def create_review(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review_author = request.user
            review_text = form.cleaned_data['text']
            review = Review(author=review_author,
                            text=review_text,
                            post=post)
            
            current_datetime = datetime.datetime.now()
            review.date_posted = current_datetime
            
            review.save()
            return HttpResponseRedirect(
                reverse('crud:detail', args=(post_id, )))
    else:
        form = ReviewForm()
    context = {'form': form, 'post': post}
    return render(request, 'crud/review.html', context)

def search_posts(request):
    context = {}
    if request.GET.get('query', False):
        search_term = request.GET['query'].lower()
        post_list = Post.objects.filter(name__icontains=search_term, active=True)
        category_list = Category
        context = {"post_list": post_list}
    return render(request, 'crud/index.html', context)