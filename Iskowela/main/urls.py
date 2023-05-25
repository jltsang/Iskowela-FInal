from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('<int:profile_id>', views.index, name='main-index'),
    path('main_update', views.main_update, name='main-update'),
    path('<int:profile_id>/post/new', login_required(views.PostCreateView.as_view()), name='post-create'),
    path('<int:profile_id>/post/delete/<pk>/', login_required(views.PostDeleteView.as_view()), name='post-delete'),
    path('<int:profile_id>/post/update/<pk>/', login_required(views.PostUpdateView.as_view()), name='post-update'),
]