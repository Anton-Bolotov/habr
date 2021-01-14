# Парсинг
#
# Задание:
# спарсить 55 случайных статей с сайта https://habr.com/ru/
#
# Выходной набор данных - файл формата .txt, в нем таблица:
#
# link	title	body	tags
#
# link - url татьи
# title - название статьи
# body - текст статьи
# tags - тэги, размещаемые под статьей, например, Math.Sin C# ряды Тейлора double
#
# Обратите внимание: в тексте не должны присутствовать
# - комментарии под статьей
# - вставки кода (см https://habr.com/ru/post/472300/)

import random

import requests
from bs4 import BeautifulSoup


with open(file='output.txt', mode='w', encoding='utf-8') as file:
    file.write('№\t' + 'link\t' + 'title\t' + 'body\t' + 'tags\n')

article_count = 0
need_articles = 55

while True:
    if article_count >= need_articles:
        break
    article_count += 1

    page_number = random.randint(1, 50)
    title_number = random.randint(1, 19)

    r = requests.get(f'https://habr.com/ru/page{page_number}/')
    soup = BeautifulSoup(r.text, 'html.parser')

    try:
        result_url = soup.find_all('a', attrs={'class', 'post__title_link'})[title_number]['href']
    except IndexError:
        article_count -= 1
        continue

    r2 = requests.get(result_url)
    soup2 = BeautifulSoup(r2.text, 'html.parser')

    title = soup2.find('h1').text.replace('\n', '')
    body = soup2.find('div', attrs={'id': 'post-content-body'})

    body_without_tag_pre = ''
    for tag in body:
        if '<pre>' not in str(tag):
            body_without_tag_pre += str(tag)

    clear_body = BeautifulSoup(body_without_tag_pre, 'html.parser').text.replace('\r', '').replace('\n', '')

    tags = soup2.find('ul', attrs={'class', 'inline-list inline-list_fav-tags js-post-tags'}).text.split('\n')
    clear_tags = ', '.join(tags[1:-1])

    with open(file='output.txt', mode='a', encoding='utf-8') as file:
        file.write(str(article_count) + '\t' + result_url + '\t' + title + '\t' + clear_body + '\t' + clear_tags + '\n')

    print(f'Собрано и записано статей - {article_count} из {need_articles}')
