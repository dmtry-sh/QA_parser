import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://www.bolshoyvopros.ru'

# даёт ссылку на страницу поиска по вопросу с http://www.bolshoyvopros.ru
def get_search_link(question):
	return BASE_URL + '/web/search.cgi?query='+ question +'&submitted=1'

# даёт ссылку на страницу первого из найденных вопросов
def get_answer_link(url):
	response = requests.get(url)
	html = response.content.decode('utf-8')
	soup = BeautifulSoup(html, 'lxml')
	a_tag = soup.find('a', class_='f15 b')
	if type(a_tag) == type(None):
		return None
	else:
		return BASE_URL + a_tag.attrs['href']


def find_best_answer(url):
	r = requests.get(url)
	content = r.content.decode('utf-8')
	soup = BeautifulSoup(content, 'lxml')
	name = soup.find('span', class_='l user_name_link').text
	answer = soup.find('div', class_='message context_hrefs_allowed').text
	return {'name' : name[:name.find('\n')],
	 		'message' : answer}


def parse_answer_big(question):
	search_url = get_search_link(question)
	try:
		answer_url = get_answer_link(search_url)
		if answer_url is None:
			raise ValueError('Ответ не найден')
		answer = find_best_answer(answer_url)
		return answer
	except ValueError as err:
		print(err)
