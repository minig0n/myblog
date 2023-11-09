from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect

from .forms import PostForm


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
            post = Post(**post_form.cleaned_data)
            post.active = True
            post.save()
            
            return HttpResponseRedirect(
                reverse('crud:detail', args=(post.pk, )))
        
    else:
        post_form = PostForm()

    context = {'post_form': post_form}
    return render(request, 'crud/create.html', context)

def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post.name = form.cleaned_data['name']
            post.date_posted = form.cleaned_data['date_posted']
            post.thumbnail_url = form.cleaned_data['thumbnail_url']
            post.save()
            return HttpResponseRedirect(
                reverse('crud:detail', args=(post.id, )))
    else:
        form = PostForm(
            initial={
                'name': post.name,
                'date_posted': post.date_posted,
                'thumbnail_url': post.thumbnail_url
            })

    context = {'post': post, 'form': form}
    return render(request, 'crud/update.html', context)