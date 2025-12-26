import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(user_url):
    result = True
    if urlparse(user_url).netloc == 'vk.cc':
        result = False
    return result

def shorten_link(vk_token, user_url):
    payload = {
        'url': user_url,
        'access_token': vk_token,
        'v': '5.199'
    }
    url_api = 'https://api.vk.ru/method/utils.getShortLink'
    response = requests.get(url_api, params=payload)
    response.raise_for_status()
    return response.json()['response']['short_url']

def count_click(vk_token, link):
    payload = {
        'key': link,
        'access_token': vk_token,
        'v': '5.199'
    }
    url_api = 'https://api.vk.ru/method/utils.getLinkStats'
    response = requests.get(url_api, params=payload)
    response.raise_for_status()
    return response.json()['response']['stats'][0]['views']

def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    user_url = input('Введи ссылку: ')
    try:
        response = requests.get(user_url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print('Некорректная ссылка!')
        raise SystemExit
    check_url = is_shorten_link(user_url)
    if check_url == True:
        try:
            short_link = shorten_link(vk_token, user_url)
        except KeyError:
            print('Ошибка VK API (getShortLink)!')
            raise SystemExit
        else:
            print('Сокращенная ссылка: ', short_link)
    else:
        link = urlparse(user_url).path[1:]
        try:
            number_of_views = count_click(vk_token, link)
        except KeyError:
            print('Ошибка VK API (getLinkStats)!')
            raise SystemExit
        else:
            print('Количество кликов по ссылке: ', number_of_views)


if __name__ == '__main__':
    main()

