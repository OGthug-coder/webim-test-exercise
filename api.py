# Подключаем библиотеку для выполнения запросов
import requests
import os


# Базовый url api Вконтакте
BASE_URL = "http://api.vk.com/method/friends.get"


def get_list(user_id):
    '''
        Функция извличения списка друзей
    '''
    # Параметры запроса
    params = {
        'user_id': user_id,
        'access_token': os.environ['TOKEN'],
        'fields': 'photo_200_orig',
        'v': 5.21, 
    }
    
    # Обработка запроса - декодинг и извлечение JSONа
    r = requests.get(BASE_URL, params=params)
    r.encoding = 'utf-8'
    print(r.json())
    return r.json()