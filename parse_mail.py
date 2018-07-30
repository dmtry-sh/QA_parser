from selenium import webdriver
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import PatternFill


BASE_SEARCH_URL = 'https://otvet.mail.ru/search/'
BASE_URL = 'https://otvet.mail.ru'


def start_browser():
	# инициализирует сессию браузера в режиме headless
	# (без граф. оболочки) 
	options = webdriver.FirefoxOptions()
	options.set_headless(headless=True)
	br = webdriver.Firefox(firefox_options = options, executable_path='./geckodriver.exe')
	return br

def close_browser(br):
	# заканчивает сессию браузера
	br.close()

def get_links(br, query):
	# браузер переходит по ссылке https://otvet.mail.ru/search/query
	# сохраняет ссылки на первые 3 ответов, найденных по запросу
	# возвращает список найденных ссылок на ответы
	br.get(BASE_SEARCH_URL + query)
	html = br.page_source
	soup = BeautifulSoup(html, "html.parser")
	links = soup.find_all('a', class_='blue item__text')
	links = [link.attrs['href'] for link in links]
	return links[:3]

def parse_answers(html):
	soup = BeautifulSoup(html, "html.parser")
	divs = soup.find_all('div', class_='answer')
	answers = []
	for div in divs:
		answer = div.find('div', class_='a--atext-value').text
		answers.append(answer)
	return answers


def parse_question(html):
	soup = BeautifulSoup(html, "html.parser")
	question = ' '
	try:
		question = soup.find('h1', class_='q--qtext entry-title').text
		question += '\n'
		question += soup.find('div', class_='q--qcomment h4 entry-content').text
	except:
		pass
	return question 


def get_answers(br, link):
	# браузер переходит по каждой из ссылок https://otvet.mail.ru/link
	# сохраняет все ответы на вопрос в список
	# возвращает список с ответами
	br.get(BASE_URL + link)
	answers = parse_answers(br.page_source)
	return answers
	

def get_qa(br, link):
	br.get(BASE_URL + link)
	answers = parse_answers(br.page_source)
	question = parse_question(br.page_source)
	return {'quest': question, 'answer': answers}

def parse_answers_mail(br, query):
	links = get_links(br, query)
	answers = []
	for link in links:
		answers.append(get_answers(br,link))
	return answers

def parse_qa(br, query):
	links = get_links(br, query)
	things = []
	for link in links:
		things.append(get_qa(br, link))
	return things



