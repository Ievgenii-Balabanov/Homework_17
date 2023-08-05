from django.urls import path

from . import views


app_name = "blog"


urlpatterns = [
    path("", views.index, name="index"),
    path("registration/", views.RegisterFormView.as_view(), name="register"),
    path("create_post/", views.WritePostView.as_view(), name="create_post"),
    path("all_post_list/", views.AllPostsListView.as_view(), name="all_post"),
    path("all_user_list/", views.AllUserProfileListView.as_view(), name="all_user"),
    path("user_profile/<int:pk>", views.PublicUserProfileDetailView.as_view(), name="public_profile"),
    path("post_list/<int:pk>/", views.UserPostDetailView.as_view(), name="post_detail"),
    path("post_list/<int:pk>/update/", views.UserPostUpdateView.as_view(), name="update_post"),
    path("post_list/", views.PostedPostByUserListView.as_view(), name="post_list"),
    # path('post_list/<int:pk>/', views.post_detail, name='post_detail'),
    path('add_comment/<int:pk>', views.add_comment, name='add_comment'),
    path("contact_admin/", views.contact_admin, name="contact_admin"),
]
