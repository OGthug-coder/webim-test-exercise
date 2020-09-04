# Подключаем библиотеку для выполнения запросов
import requests


# Базовый url api Вконтакте
BASE_URL = "http://api.vk.com/method/friends.get"


def get_list(user_id):
    '''
        Функция извличения списка друзей
    '''
    # Параметры запроса
    params = {
        'count': 5,
        'user_id': user_id,
        'access_token': '972dc7f7972dc7f7972dc7f75d975e04479972d972dc7f7c87fdfe198bec228ec844c67',
        'fields': 'photo_200_orig',
        'v': 5.21, 
    }
    
    # Обработка запроса - декодинг и извлечение JSONа
    r = requests.get(BASE_URL, params=params)
    r.encoding = 'utf-8'
    print(r.json())
    return r.json()