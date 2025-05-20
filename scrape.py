from curl_cffi import requests
from bs4 import BeautifulSoup
import json


def get_request(url):
    '''
        Make request to the url
    '''
    try:
        resp = requests.get(url, impersonate='chrome', timeout=5)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        print('ERROR: Request timed out. Check your internet connection or try again later.')
        return
    except Exception as e:
        print(f'ERROR: {e}')
        return
    return resp.text

def parse_data(all_recipes, url):
    '''
        Parses the html content and append each recipe into all_recipes
    '''
    html_content = get_request(url)

    if not html_content:
        return

    soup = BeautifulSoup(html_content, 'lxml')
    main_content = soup.select_one('main.content.entries-container')
    recipes = main_content.select('article[class*="recipes"]')

    if not recipes:
        return

    i = len(all_recipes)

    for recipe in recipes:
        recipe_name = recipe.select_one('.entry-title').get_text()
        recipe_link = recipe.select_one('.entry-title-link').get('href')
        recipe_img = recipe.select_one('.entry-image')
        if recipe_img:
            recipe_img = recipe_img.get('data-src')
        else:
            recipe_img = None

        all_recipes.append({
            'id': i,
            'recipe_name': recipe_name or None,
            'recipe_link': recipe_link or None,
            'recipe_img': recipe_img or None
        })
        i += 1

def save_as_json(all_recipes, recipes_file_name):
    '''
        Save recipes into json
    '''

    with open(recipes_file_name, 'w', encoding='utf-8') as f:
        json.dump(all_recipes, f, ensure_ascii=False, indent=4)


def main():
    page_num = 1
    all_recipes = []
    recipes_file_name = 'recipes.json'

    try:
        while page_num < 227:
            url = f'https://panlasangpinoy.com/recipes/page/{page_num}'
            print(f'Scraping page: {url}')
            parse_data(all_recipes, url)
            page_num += 1

    except KeyboardInterrupt:
        print('\nScraping manually interrupted. Saving data...')

    print('=' * 100)
    print('Finish scraping')
    print('=' * 100)
    print(f'Total recipes scraped: {len(all_recipes)}')
    save_as_json(all_recipes, recipes_file_name)
    print(f'Saved all recipes in: {recipes_file_name}')


if __name__ == '__main__':
    main()
