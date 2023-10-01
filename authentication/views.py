from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from helpers.decorators import auth_user_should_not_access

@auth_user_should_not_access
def register(request):
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')


        if len(password) < 8:
            messages.add_message(request, messages.ERROR, 
                                'Пароль должен быть более 8 символов')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR, 
                                'Пароли не совпадают')
            context['has_error'] = True
        
        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 
                                'Введите корректный E-mail адрес')
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR, 
                                'Неправильный формат имени')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 
                                'Имя уже используется, выберите другое')
            context['has_error'] = True

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 
                                'E-mail уже зарегестрирован')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'authentication/register.html')
        
        user = User.objects.create_user(username=username,email=email)
        user.set_password(password)
        user.save()

        messages.add_message(request, messages.SUCCESS, 
                                'Регистрация прошла успешно!')
        
        return redirect('login')

    return render(request, 'authentication/register.html')


@auth_user_should_not_access
def login_user(request):

    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.add_message(request, messages.ERROR, 'Неверные данные учетной записи')

            return  render(request, 'authentication/login.html', context)
        
        login(request, user)

        messages.add_message(request, messages.SUCCESS, f'Добро пожаловать {user.username}')
        
        return redirect(reverse('home'))

    return  render(request, 'authentication/login.html')



def logout_user(request):

    logout(request)
    messages.add_message(request, messages.SUCCESS, f'Вы вышли из системы')
    return redirect(reverse('login'))