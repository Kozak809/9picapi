# 9picapi

Пример работы

```
python .\main.py image.jpg                                                    
Загрузка изображения: image.jpg
Срок хранения: бессрочно

Изображение успешно загружено!

Ссылка: https://9pic.ru/HHeXY
Прямая ссылка: https://9pic.ru/HHeXY/image.jpg
Markdown: ![Image](https://9pic.ru/HHeXY/image.jpg)
Для форума: [IMG]https://9pic.ru/HHeXY/image.jpg[/IMG]
Для сайта (HTML-код): <img src="https://9pic.ru/HHeXY/image.jpg" alt="image.jpg">
Ссылка для удаления: https://9pic.ru/delete.php?uuid=HHeXY&secret=ee73687a81615d42ab9cd96c163d2b9c
```
Доступные флаги

```
python .\main.py -h       
usage: main.py [-h] [--deleteafter30days] [--link-type {link,direct,markdown,forum,html,delete}] image_path

Загрузка изображений на https://9pic.ru/

positional arguments:
  image_path            Путь к изображению для загрузки

options:
  -h, --help            show this help message and exit
  --deleteafter30days   Удалить изображение через 30 дней (по умолчанию: никогда не удалять)
  --link-type {link,direct,markdown,forum,html,delete}
                        Тип ссылки для вывода (можно указать несколько раз). Если не указано, выводятся все   
                        ссылки

Примеры использования:
  python upload_image.py image.jpg
  python upload_image.py image.png --deleteafter30days
  python upload_image.py image.jpg --link-type direct
  python upload_image.py image.jpg --link-type direct --link-type markdown

```
