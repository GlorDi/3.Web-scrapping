import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
from fake_headers import Headers



def get_headers():
    return Headers(browser='chrome', os='win').generate()


HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
html = requests.get(HOST, headers=get_headers()).text

soup = BeautifulSoup(html, features='lxml')
all_vacancies = soup.find(id='a11y-main-content')
vacancy = all_vacancies.find_all(class_='serp-item')


description_list = []
for item in vacancy:
    description_vacancy = item.find(class_='vacancy-serp-item__layout')
    description = description_vacancy.find(class_='g-user-content').text
    if 'Django' in description and 'Flask' in description:
        description_list.append(item)


vacancy_list = []
for word in description_list:
    title = word.find('a', class_='serp-item__title').text
    link_tag = word.find('a', class_='serp-item__title')
    link = link_tag['href']
    try:
        salary_tag = word.find('span', class_='bloko-header-section-3')
        salary = salary_tag.text
    except Exception:
        salary = 'Не указана'
    company_tag = word.find('a', class_='bloko-link bloko-link_kind-tertiary')
    company = company_tag.text
    city_tag = word.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'})
    city = city_tag.text

    vacancy_list.append({
        'Название': title,
        'Зарплата': salary,
        'Компания': company,
        'Город': city,
        'Ссылка': link
    })

pprint(vacancy_list)
with open('vacancy.json', 'w') as f:
    json.dump(vacancy_list, f, ensure_ascii=False)