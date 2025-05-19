from curl_cffi import requests
from bs4 import BeautifulSoup

# url = 'https://panlasangpinoy.com/recipes/page/1/'

def get_request(url):
    s = requests.Session()
    try:
        resp = s.get(url, impersonate='chrome', timeout=5)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        print('ERROR: Request timed out. Check your internet connection or try again later.')
        return
    except Exception as e:
        print(f'ERROR: {e}')
        return
    return resp.text

def main():


if __name__ == '__main__':
    main()
