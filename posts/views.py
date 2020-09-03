from django.shortcuts import render
from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .forms import PostForm
from .serializers import PostSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)


@api_view(['GET'])
def post_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def post_create_view(request, *args, **kwargs):
    serializer = PostSerializer(data=request.POST)
    if serializer.is_valid():
        obj = serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


# is POST good?
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def post_delete_view(request, post_id, *args, **kwargs):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'message': '404 post not found'}, status=404)
    if not post.user == request.user:
        return Response({'message': '401 you are not authorized to delete this post'}, status=401)
    post.delete()
    return Response({'message': 'Delete successful'}, status=200)


# is UPDATE good?
@api_view(['POST'])
@authentication_classes([SessionAuthentication])
def post_like_view(request, post_id, *args, **kwargs):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'message': '404 post not found'}, status=404)
    post_likes_list = post.likes
    if request.user in post_likes_list.all():
        post_likes_list.remove(request.user)
        return Response({'message':'You canceled your like'}, status=200)
    else:
        post_likes_list.add(request.user)
        return Response({'message':'You liked this post'}, status=200)


@api_view(['GET'])
def post_details(request, post_id, *args, **kwargs):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({}, status=404)
    serializer = PostSerializer(post)
    return Response(serializer.data, status=200)
