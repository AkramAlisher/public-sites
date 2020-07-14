import json
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import Cargo as Cargo_model
from api.serializers import CargoSerializer


class List(generics.ListCreateAPIView):
    queryset = Cargo_model.objects.all()
    serializer_class = CargoSerializer


class Details(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo_model.objects.all()
    serializer_class = CargoSerializer


@api_view(['POST'])
def search(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        resumes = Cargo_model.objects.filter(post__icontains=data.get('post').strip(), top=data.get('top'), city=data.get('city'))
        if data.get('post').islower():
            resumes |= Cargo_model.objects.filter(post__icontains=data.get('post').capitalize().strip(), top=data.get('top'), city=data.get('city'))
        serializer = CargoSerializer(resumes, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def pinned(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        resumes = Cargo_model.objects.filter(pin=True, city=data.get('city'))
        serializer = CargoSerializer(resumes, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my(request):
    data = json.loads(request.body.decode('utf-8'))
    resumes = Cargo_model.objects.filter(user_id=data.get('user_id'))
    serializer = CargoSerializer(resumes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def send_to_email(request):
    data = json.loads(request.body.decode('utf-8'))
    send_mail(
        'Резюме {}'.format(data.get('post')),
        ' id: {},\n ФИО: {},\n Почта: {},\n Дата рождения: {},\n Телефон: {},\n Город: {},\n Семейное положение: {},\n '
        'Образование: {},\n Опыт работы: {},\n Знание языков: {},\n Желаемая должность: {},\n Личные качества: {},\n '
        'Закреп на главную страницу(VIP): {},\n Топ объявление: {},\n Поиск: {},\n Id пользователя: '
        '{},\n Дата создания: {}'.format(data.get('id'),
            data.get('name'), data.get('email'), data.get('date'),
            data.get('phone'), data.get('city'), data.get('familyStatus'), data.get('education'),
            data.get('experience'), data.get('languages'), data.get('post'), data.get('qualities'),
            data.get('pin'), data.get('top'), data.get('search'), data.get('user_id'), data.get('created')),
        'report@gmail.com',
        ['report@gmail.com'],
        fail_silently=False,
    )
    return Response(status=status.HTTP_204_NO_CONTENT)