from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view,permission_classes
# Create your views here.
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer,PostSerializer,CommentSerializer
from .models import User,Profile,Post,Comment
from rest_framework.permissions import AllowAny
import jwt,datetime
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    pass
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']
#         user = User.objects.filter(email=email).first()
#         if user is None:
#             raise AuthenticationFailed("User Not Found!!!")

#         if not user.check_password(password):
#             raise AuthenticationFailed("Incorrect Password!!!")
        
#         user = authenticate(email=email, password=password)
#         print(request.user)
#         payload = {
#             'id':user.id,
#             'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat':datetime.datetime.utcnow()
#         }
#         token = jwt.encode(payload,'secret',algorithm='HS256')

#         response = Response()

#         response.set_cookie(key='jwt',value=token,httponly=True)

#         response.data = {
#             "jwt":token,
#         }
#         return response

class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        id = request.user.id
        user = User.objects.filter(id=id).first()
        profile = Profile.objects.filter(user=user).first()
        print(profile)
        payload = {
            "username": user.first_name,
            "followers":profile.followers.all().count(), 
            "followings":profile.followings.all().count()
        }
        return Response(payload)


class FollowView(viewsets.ViewSet):
    queryset = Profile.objects
    def follow(self,request,pk):
        id = self.request.user.id
        own_profile = Profile.objects.get(user=request.user)
        following_user = User.objects.get(id=pk)
        if following_user in own_profile.followings.all():
            return Response({'message':'You already follow this profile!!!'})
        own_profile.followings.add(following_user)
        return Response({'message':'You are following now!!!'})

    def unfollow(self,request,pk):
        id = self.request.user.id
        own_profile = Profile.objects.get(user=request.user)
        following_user = User.objects.get(id=pk)
        if following_user not in own_profile.followings.all():
            return Response({'message':'You did not follow now!!!'})
        own_profile.followings.remove(following_user)
        return Response({'message':'You are unfollowing now!!!'})

class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self,serializer):
        serializer.save(owner = self.request.user)

class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentView(viewsets.ViewSet):
    queryset = Comment.objects
    def comment(self,request,pk):
        post = Post.objects.filter(id=pk).first()
        comment = Comment.objects.create(owner=self.request.user,post=post,comment=request.data['comment'])
        return Response({'comment_id':comment.id})



class LikeView(viewsets.ViewSet):
    queryset = Post.objects
    def like(self,request,pk):
        post = Post.objects.filter(id=pk).first()
        user = request.user
        if user in post.likes.all():
            return Response({'message':'You already Liked!!!'})
        post.likes.add(user)
        return Response({'message':'You Liked the post!!!'})

    def unlike(self,request,pk):
        post = Post.objects.filter(id=pk).first()
        user = request.user
        if user not in post.likes.all():
            return Response({'message':'You already UnLiked!!!'})
        post.likes.remove(user)
        return Response({'message':'You unliked the post!!!'})

# class AllpostsView(viewsets.ViewSet):
#     queryset = Post.objects
@api_view(['GET'])
def return_all_posts(request):
        user = request.user
        posts = Post.objects.filter(owner= user)
        payload = {}
        for post in posts.all():
            comments = {}
            for comment in post.comments.all():
                comments[comment.id]={
                    "comment":comment.comment
                }
            payload[post.id]={
                "title":post.title,
                "desc":post.description,
                "created_at":post.created_time,
                "likes":post.likes.all().count(),
                "comments":comments
            }

        return Response({'posts':payload})
        