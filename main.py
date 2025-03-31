import os
import requests
from bs4 import BeautifulSoup

def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type')
        extension = ''
        if 'image/jpeg' in content_type:
            extension = '.jpg'
        elif 'image/png' in content_type:
            extension = '.png'
        elif 'image/gif' in content_type:
            extension = '.gif'
        elif 'image/webp' in content_type:
            extension = '.webp'
        else:
            print(f"Unsupported content type: {content_type} for URL: {url}")
            return

        file_name = url.split('/')[-1].split('?')[0] + extension
        file_path = os.path.join(save_path, file_name)

        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def download_images_from_html(html_content, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')

    for img in img_tags:
        url = img.get('src')
        if url:
            download_image(url, save_path)

if __name__ == "__main__":
    html_file = 'example.html'  # Путь к HTML-файлу
    save_path = 'downloaded_images'  # Папка для сохранения скачанных изображений

    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    download_images_from_html(html_content, save_path)
