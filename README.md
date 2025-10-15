# pic9 - Загрузчик изображений для 9pic.ru

Простая и удобная Python библиотека для загрузки изображений на сервис https://9pic.ru/

## Установка

### Из PyPI:
```bash
pip install pic9
```

### Из исходников:
```bash
git clone https://github.com/Kozak809/9picapi
cd pic9
pip install -e .
```

### Локальная установка:
```bash
pip install .
```

## Использование

### CLI (командная строка)

После установки станет доступна команда `pic9`:

```bash
# Загрузить изображение
pic9 image.jpg

# Загрузить с автоудалением через 30 дней
pic9 image.png --deleteafter30days

# Вывести только прямую ссылку
pic9 image.jpg --link-type direct

# Вывести несколько типов ссылок
pic9 image.jpg --link-type direct --link-type markdown
```

### Как библиотека в Python коде

```python
from pic9 import upload_image, format_links

# Загрузить изображение
result = upload_image('path/to/image.jpg', delete_after='never')

if result:
    # Получить отформатированные ссылки
    links = format_links(result)
    
    print(f"Прямая ссылка: {links['direct']}")
    print(f"Markdown: {links['markdown']}")
    print(f"HTML: {links['html']}")
```

## API

### `upload_image(image_path, delete_after='never')`

Загружает изображение на 9pic.ru.

**Параметры:**
- `image_path` (str): Путь к файлу изображения
- `delete_after` (str): 'never' или '30' (дней)

**Возвращает:**
- dict с результатом загрузки или None в случае ошибки

### `format_links(result)`

Форматирует ссылки из результата загрузки.

**Параметры:**
- `result` (dict): Результат от `upload_image()`

**Возвращает:**
- dict со ссылками в различных форматах:
  - `link` - ссылка на страницу просмотра
  - `direct` - прямая ссылка на изображение
  - `markdown` - формат Markdown
  - `forum` - формат для форумов (BBCode)
  - `html` - HTML код
  - `delete` - ссылка для удаления

## Требования

- Python >= 3.7
- requests >= 2.25.0

## Лицензия

MIT License

## Автор

Your Name

## Вклад в проект

Pull requests приветствуются! Для больших изменений, пожалуйста, сначала откройте issue для обсуждения.
