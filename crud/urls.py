from django.urls import path

from . import views

app_name = 'crud'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('posts/<int:post_id>/', views.detail_post, name='detail'),
    path('delete/<int:post_id>/', views.delete_post, name='delete'),
    path('create/', views.create_post, name='create'),
    path('update/<int:post_id>/', views.update_post, name='update'),
    path('review/<int:post_id>/', views.create_review, name='review'),
    path('search/', views.search_posts, name='search'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('category/<int:category_id>', views.detail_category, name='category-list'),
    # path('category/<int:category_id>', views.CategoryPostListView.as_view(), name='category-list'),
]