from rest_framework import serializers
from .models import User,Profile,Post,Comment

class UserSerializer(serializers.ModelSerializer): 
    id = serializers.ReadOnlyField()
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=255,required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = User
        fields = ('id','email', 'password','first_name','posts','comments')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        Profile.objects.create(user=instance)
        return instance

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.first_name')
    comments = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Post
        fields = ('id','title','description','owner','comments')

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.first_name')
    
    class Meta:
        model = Comment
        fields = ('id','comment','owner','post')