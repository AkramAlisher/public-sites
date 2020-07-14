import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import UserSerializer, ProfileSerializer


class List(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Details(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def log_in(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})


@api_view(['POST'])
def sign_up(request):
    data = json.loads(request.body.decode('utf-8'))
    data['password'] = make_password(data.get('password'));
    userSerializer = UserSerializer(data=data)
    if userSerializer.is_valid():
        userSerializer.save()
        return Response(userSerializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': userSerializer.errors},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_out(request):
    request.auth.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_info_by_token(request):
    user = Token.objects.get(key=request.data['token']).user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def send_secret_key(request):
    data = json.loads(request.body.decode('utf-8'))
    send_mail(
        'Вы сбрасываете пароль от сайта',
        'Это ваш секретный код: {}. Никому его не говорите!'.format(data.get('key')),
        'report@kz',
        [data.get('email')],
        fail_silently=False,
    )
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def send_email(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        user = User.objects.get(username=data.get('username'))
    except User.DoesNotExist as e:
        return Response({'error': 'Такого логина не существует!'})
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['PUT'])
def password_reset(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        user = User.objects.get(username=data.get('username'))
    except User.DoesNotExist as e:
        return Response({'error': str(e)})

    data['password'] = make_password(data.get('password'));
    serializer = UserSerializer(instance=user, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({'error': serializer.errors})


@api_view(['PUT', 'GET'])
def profile(request, pk):
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        data['user'] = pk
        user = User.objects.get(pk=pk)

        serializer = ProfileSerializer(instance=user.profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors})
    elif request.method == 'GET':
        user = User.objects.get(pk=pk)
        serializer = ProfileSerializer(user.profile)
        return Response(serializer.data)

