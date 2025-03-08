import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

SHORTENED_LINK_DOMAINS = ['vk.cc']


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
    return short_url, short_link_key


def get_click_stats(token, short_link_key, interval='forever', intervals_count=1, extended=0):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'v': '5.131',
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
    if parsed_url.netloc in SHORTENED_LINK_DOMAINS:
        return True
    else:
        return False


def main():
    original_url = input("Введите ссылку, которую хотите сократить: ")

    if is_shorten_link(original_url):
        short_link_key = urlparse(original_url).path.split('/')[-1]
        clicks = get_click_stats(token, shorten_link)
        print('Количество кликов по ссылке :', clicks)
    else:
        shortened_link, short_link_key = shorten_link(token, original_url)
        print('Сокращенная ссылка:', shortened_link)


if __name__ == "__main__":
    load_dotenv()
    token = os.environ['VK_TOKEN']
    main()
    
