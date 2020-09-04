# Подключаем библиотеку для выполнения запросов
import requests


# Базовый url api Вконтакте
BASE_URL = "http://api.vk.com/method/friends.search"


def get_list(token):
    '''
        Функция извличения списка друзей
    '''
    # Параметры запроса
    params = {
        'count': 5,
        'access_token': token,
        'fields': 'photo_200_orig',
        'v': 5.21, 
    }
    
    # Обработка запроса - декодинг и извлечение JSONа
    r = requests.get(BASE_URL, params=params)
    r.encoding = 'utf-8'
    print(r.json)
    return r.json()