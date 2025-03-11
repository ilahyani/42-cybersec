import argparse
import os
import urllib.parse
import requests
from bs4 import BeautifulSoup
import urllib

supported_files = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

def parse_args():
    parser = argparse.ArgumentParser(description="""
        The spider program allows you to extract all the images from a website, recursively, by providing a url as a parameter
    """)

    parser.add_argument('url', help='Target URL')
    parser.add_argument('-r', '--recursive', action='store_true', help='recursively downloads the images in the received URL')
    parser.add_argument('-l', '--level', type=int, default=5, help='the maximum depth level of the recursive download')
    parser.add_argument('-p', '--path', default='./data/', help='the path where the downloaded files will be saved')

    return parser.parse_args()

def spider(url, base, path, level, recursive, depth = 0, visited = set()):

    if url in visited or depth >= level:
        return
    
    visited.add(url)

    print('page', url, 'depth', depth)

    try:
        res = requests.get(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html.parser")

            for img in soup.find_all('img'):
                if img_src := img.get('src'):
                    ext = os.path.splitext(img_src)[1].lower()
                    if ext in supported_files:
                        print(f'downloading image {img_src} ...')
                        response = requests.get(img_src)
                        if response.status_code == 200:
                            with open(f"{path}/{img_src.split('/')[-1]}", 'wb') as f:
                                f.write(response.content)
            if recursive and level > 1:
                for link in soup.find_all('a'):
                    if href := link.get('href'):
                        next_page_url = urllib.parse.urljoin(url, href)
                        spider(next_page_url, base, path, level, recursive, depth + 1, visited)
        else:
            print("request failed", res.status_code)

    except Exception as e:
        print(f"something went wrong: {e}")
        SystemExit(1)

def main():
    args = parse_args()

    url, recursive, level, path = args.url, args.recursive, args.level, args.path

    os.makedirs(path, exist_ok=True)

    try:
        spider(url, url, path, level, recursive)
    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting gracefully...")
        SystemExit(0)

if __name__ == '__main__':
    main()
