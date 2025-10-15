#!/usr/bin/env python3
"""
Скрипт для загрузки изображений на https://9pic.ru/
Использование: python upload_image.py путь/к/изображению [--deleteafter30days] [--link-type TYPE]
"""

import argparse
import sys
import os
import requests
from pathlib import Path
from urllib.parse import quote


def upload_image(image_path, delete_after='never'):
    """
    Загружает изображение на 9pic.ru
    
    Args:
        image_path: путь к файлу изображения
        delete_after: 'never' или '30' (дней)
    
    Returns:
        dict с ссылками или None в случае ошибки
    """
    url = 'https://9pic.ru/upload.php'
    
    # Проверяем существование файла
    if not os.path.exists(image_path):
        print(f"Ошибка: файл '{image_path}' не найден", file=sys.stderr)
        return None
    
    # Проверяем, что это файл
    if not os.path.isfile(image_path):
        print(f"Ошибка: '{image_path}' не является файлом", file=sys.stderr)
        return None
    
    try:
        # Заголовки для имитации браузера
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://9pic.ru',
            'Referer': 'https://9pic.ru/',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty'
        }
        
        # Открываем файл и подготавливаем данные для отправки
        with open(image_path, 'rb') as f:
            files = {
                'image': (os.path.basename(image_path), f, 'image/jpeg')
            }
            data = {
                'delete_after': delete_after
            }
            
            # Отправляем POST запрос
            response = requests.post(url, files=files, data=data, headers=headers)
            response.raise_for_status()
            
            # Парсим JSON ответ
            result = response.json()
            
            if result.get('success'):
                return result
            else:
                print(f"Ошибка загрузки: {result.get('error', 'Неизвестная ошибка')}", file=sys.stderr)
                return None
                
    except requests.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}", file=sys.stderr)
        return None


def format_links(result):
    """
    Форматирует ссылки из результата загрузки
    
    Args:
        result: dict с результатом загрузки
    
    Returns:
        dict с отформатированными ссылками
    """
    links = {}
    base_url = 'https://9pic.ru'
    
    if 'uuid' in result and 'original' in result:
        uuid = result['uuid']
        original_filename = result['original']
        
        # Ссылка на страницу просмотра
        links['link'] = f"{base_url}/{uuid}"
        
        # Прямая ссылка на изображение (с закодированным именем файла)
        encoded_filename = quote(original_filename)
        links['direct'] = f"{base_url}/{uuid}/{encoded_filename}"
        
        # Формируем различные форматы ссылок
        direct_url = links['direct']
        links['markdown'] = f"![Image]({direct_url})"
        links['forum'] = f"[IMG]{direct_url}[/IMG]"
        links['html'] = f'<img src="{direct_url}" alt="{original_filename}">'
        
        # Ссылка для удаления
        if 'delete_url' in result:
            links['delete'] = result['delete_url']
    
    return links


def print_links(links, link_types=None):
    """
    Выводит ссылки
    
    Args:
        links: dict со ссылками
        link_types: список типов ссылок для вывода (None = все)
    """
    link_labels = {
        'link': 'Ссылка',
        'direct': 'Прямая ссылка',
        'markdown': 'Markdown',
        'forum': 'Для форума',
        'html': 'Для сайта (HTML-код)',
        'delete': 'Ссылка для удаления'
    }
    
    # Если не указаны конкретные типы, выводим все
    if link_types is None:
        link_types = link_labels.keys()
    
    for link_type in link_types:
        if link_type in links:
            label = link_labels.get(link_type, link_type)
            print(f"{label}: {links[link_type]}")


def main():
    parser = argparse.ArgumentParser(
        description='Загрузка изображений на https://9pic.ru/',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python upload_image.py image.jpg
  python upload_image.py image.png --deleteafter30days
  python upload_image.py image.jpg --link-type direct
  python upload_image.py image.jpg --link-type direct --link-type markdown
        """
    )
    
    parser.add_argument(
        'image_path',
        help='Путь к изображению для загрузки'
    )
    
    parser.add_argument(
        '--deleteafter30days',
        action='store_true',
        help='Удалить изображение через 30 дней (по умолчанию: никогда не удалять)'
    )
    
    parser.add_argument(
        '--link-type',
        action='append',
        choices=['link', 'direct', 'markdown', 'forum', 'html', 'delete'],
        help='Тип ссылки для вывода (можно указать несколько раз). Если не указано, выводятся все ссылки'
    )
    
    args = parser.parse_args()
    
    # Определяем параметр delete_after
    delete_after = '30' if args.deleteafter30days else 'never'
    
    print(f"Загрузка изображения: {args.image_path}")
    print(f"Срок хранения: {'30 дней' if delete_after == '30' else 'бессрочно'}")
    print()
    
    # Загружаем изображение
    result = upload_image(args.image_path, delete_after)
    
    if result is None:
        sys.exit(1)
    
    # Форматируем ссылки
    links = format_links(result)
    
    if not links:
        print("Ошибка: не удалось получить ссылки", file=sys.stderr)
        sys.exit(1)
    
    # Выводим ссылки
    print("Изображение успешно загружено!\n")
    print_links(links, args.link_type)


if __name__ == '__main__':
    main()