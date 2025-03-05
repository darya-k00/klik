import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse

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

    if 'response' in response_data:
        short_url = response_data['response']['short_url']
        parsed_url = urlparse(short_url)
        short_link_key = parsed_url.path.split('/')[-1]
        return short_url, short_link_key
    else:
        error_message = response_data['error']['error_msg']
        raise Exception(f"Ошибка API: {error_message}")

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

    if 'response' in response_data:
        return response_data['response']['stats']
    else:
        error_message = response_data['error']['error_msg']
        raise Exception(f"Ошибка API: {error_message}")

def is_shorten_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc in SHORTENED_LINK_DOMAINS

if __name__ == "__main__":
    load_dotenv()
    token=os.environ.get('TOKEN')
    token = 'c5c6f550c5c6f550c5c6f55018c6ecc96ccc5c6c5c6f550a27342508925cf6bbc4cf08c'  
    original_url = input("Введите ссылку, которую хотите сократить: ")
    
    try:
        shortened_link = shorten_link(token, original_url)
        print('Сокращенная ссылка:', shortened_link)
        clicks = get_click_stats(token, shortened_link)
        print('Количество кликов по ссылке :', clicks)
        short_link_key = original_url.split('/')[-1]

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

