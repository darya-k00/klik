import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, original_url):
    api_url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'url': original_url,
        'access_token': token,
        'v': '5.199'
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    response_data = response.json()
    short_url = response_data.get('response', {}).get('short_url')
    short_link_key = urlparse(short_url).path.split('/')[-1]
    return short_url


def get_click_stats(token, short_link_key, interval='forever', intervals_count=1, extended=0):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'v': '5.199',
        'key': short_link_key,
        'access_token': token,
        'interval': interval,
        'intervals_count': intervals_count,
        'extended': extended
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    response_data = response.json()
    return response_data['response']['stats']


def is_shorten_link(original_url):
    parsed_url = urlparse(original_url)
    response = requests.get(
        'https://api.vk.com/method/utils.resolveScreenName',
        params={
            'screen_name': original_url.split('/')[-1], 
            'access_token': token,
            'v': 5.199
        }
    )
    response_data = response.json()
    return bool(response_data.get('response'))


def main():
    load_dotenv()
    token = os.environ['VK_TOKEN']   
    original_url = input("Введите ссылку, которую хотите сократить: ")

    if is_shorten_link(original_url):
        short_link_key = is_shorten_link(original_url)
        clicks = get_click_stats(token, shorten_link)
        print('Количество кликов по ссылке :', clicks)
    else:
        shortened_link = shorten_link(token, original_url)
        print('Сокращенная ссылка:', shortened_link)


if __name__ == "__main__":
    main()
