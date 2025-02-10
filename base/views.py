import os
import requests
from datetime import datetime, timedelta
import shutil

from pathlib import Path

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .utils import get_ip_country_city
from django.utils.timezone import now
from django.conf import settings

from .models import *
from analytics.models import *


from django.conf import settings
from datetime import datetime as dt

# views.py
from datetime import datetime, timedelta
from django.http import JsonResponse

def discount_timer(request):
    # Define the initial timer duration: 6 hours, 43 minutes
    initial_duration = timedelta(hours=6, minutes=43)

    # Get the user's IP address
    user_ip = request.META.get('REMOTE_ADDR')

    # Check if the cookie exists
    expiry_time_cookie = request.COOKIES.get(user_ip)
    if expiry_time_cookie:
        # Convert cookie expiry time to datetime
        expiry_time = datetime.fromtimestamp(float(expiry_time_cookie))
        # Check if current time is past the expiry time
        if datetime.now() > expiry_time:
            # Reset the timer if expired
            expiry_time = datetime.now() + initial_duration
    else:
        # If cookie doesn't exist, set initial expiry time
        expiry_time = datetime.now() + initial_duration

    # Prepare the response with the updated expiry time
    response = JsonResponse({'expiry_time': expiry_time.timestamp()})
    # Set the cookie with the new or updated expiry time
    response.set_cookie(user_ip, expiry_time.timestamp(), max_age=initial_duration.total_seconds())

    return response

# Функция для отправки сообщения в Telegram

# Основная функция представления
def landing(request):
    url = request.META.get('HTTP_REFERER')
    ip = request.META.get('REMOTE_ADDR')

    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

    # Проверка, является ли устройство мобильным
    mobile = any(keyword in user_agent for keyword in ['mobile', 'android', 'iphone', 'ipad'])

    # Получение страны и города по IP
    ip, country, city = get_ip_country_city(request)
    
    # Установка московского времени
    utc_offset = timedelta(hours=0)  # Смещение Московского времени относительно UTC
    current_time_msk = now() + utc_offset

    # Формирование сообщения для отправки в Telegram
    message = (
        f"URL: {url}\n"
        f"IP: {ip}\n"
        f"Страна: {country}\n"
        f"Город: {city}\n"
        f"Мобильный: {mobile}\n"
        f"Время входа: {current_time_msk.strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
    }

    response = requests.post(url, data=data)
    
    if response.status_code != 200:
        print("Failed to send message:", response.text)

    visit = Visit.objects.create(
        url=url,
        ip=ip,
        country=country,
        city=city,
        mobile=mobile,
        entered_at=timezone.now()
    )

    context = {
        'i': visit.id,
    }

    return render(request, 'l_neu.html', context)

@csrf_exempt
def save_leave_time(request):

    session_id = request.POST.get('i')
    leave_time = request.POST.get('t')

    visit = Visit.objects.get(id = session_id)

    visit.left_at = parse_datetime(leave_time)
    visit.save()

    return HttpResponse('K')

def button_click(request):

    ButtonClick.objects.create()

    return HttpResponse('K')

def receive_contact_info(request):

    website_type = request.POST.get('t')
    name = request.POST.get('n')
    email = request.POST.get('e')
    phone = request.POST.get('p')

    Customer.objects.create(

        website_type = website_type, 
        name = name, 
        email = email, 
        phone = phone

    )

    utc_offset = timedelta(hours=0)  # Смещение Московского времени относительно UTC
    current_time_msk = now() + utc_offset

    message = (
        f"Тип сайта: {website_type}\n"
        f"Имя: {name}\n"
        f"Почта: {email}\n"
        f"Телефон: {phone}\n"
        f"Время входа: {current_time_msk.strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_LOG_TOKEN}/sendMessage"
    
    data = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
    }

    response = requests.post(url, data=data)
    
    if response.status_code != 200:

        print("Failed to send message:", response.text)

    return HttpResponse('K')


def test(request):

    return render(request, 'test.html')