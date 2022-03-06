from django.contrib import admin
from django.urls import path,include
from .views import RegisterView,LoginView,FollowView,UserView,PostList,PostDetail,CommentView,LikeView,return_all_posts
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register',RegisterView.as_view()),
    # path('authenticate',TokenObtainPairView,name="login"),
    path('user',UserView.as_view()),
    path('posts',PostList.as_view()),
    path('posts/<int:pk>/',PostDetail.as_view()),
    path('comment/<int:pk>/',CommentView.as_view({'post':'comment'})),
    path('follow/<int:pk>/',FollowView.as_view({'post':'follow'})),
    path('unfollow/<int:pk>/',FollowView.as_view({'post':'unfollow'})),
    path('like/<int:pk>/',LikeView.as_view({'post':'like'})),
    path('unlike/<int:pk>/',LikeView.as_view({'post':'unlike'})),
    path('all_posts',return_all_posts)
]
