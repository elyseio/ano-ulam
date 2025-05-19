from curl_cffi import requests
from bs4 import BeautifulSoup

# url = 'https://panlasangpinoy.com/recipes/page/1/'

def get_request(url):
    '''
        Make request to the url
    '''
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

def parse_data(url):
    '''
        Parses the html content
    '''
    html_content = get_request(url)

    if not html_content:
        return

    soup = BeautifulSoup(html_content, 'lxml')
    main_content = soup.select_one('main.content.entries-container')
    recipes = main_content.select('article[class*="recipes"]')

    for recipe in recipes:
        recipe_title = recipe.select_one('.entry-title').get_text()
        recipe_link = recipe.select_one('.entry-title-link').get('href')
        recipe_img = recipe.select_one('.entry-image').get('data-src')



def main():
    url = 'https://panlasangpinoy.com/recipes/page/1/'
    parse_data(url)


if __name__ == '__main__':
    main()
