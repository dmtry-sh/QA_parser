from selenium import webdriver
from bs4 import BeautifulSoup
BASE_SEARCH_URL = 'https://otvet.mail.ru/search/'
BASE_URL = 'https://otvet.mail.ru'


# запуск браузера Firefox в headless режиме (без графической оболочки)
def start_browser():
	options = webdriver.FirefoxOptions()
	 # задаю опции браузера
	options.set_headless(headless=True)
	 # запускаю сессию браузера
	browser = webdriver.Firefox(executable_path='./geckodriver')
	return browser

def close_browser(browser):
	# заканчиваю сессию браузера
	browser.close()


#
def get_link_by_query(browser, query):
	try:
		query = query.replace(' ', '%20')
		browser.get(BASE_SEARCH_URL + query)
		html = browser.page_source
		soup = BeautifulSoup(html, 'lxml')
		link = soup.find('div', class_='gray-line dotted item item_ava item_similiar').find('a', class_='blue item__text').attrs['href']
		return str(link)
	except Exception as err:
		print(err)
		print('закрываю браузер')
		browser.close()

def get_answers(browser, link):
	try:
		browser.get(BASE_URL + link)
		html = browser.page_source
		#print(html)
		soup = BeautifulSoup(html, 'lxml')
		#print(soup)
		div_of_best = soup.find('div', class_='answer hentry a--box ' + r'aid-[0-9]+' + ' answer-selected')
		name_of_best = div_of_best.find('a', class_='author a--author').text
		answer_of_best = div_of_best.find('div', class_='a--atext-value').text
	
		others = []
		other_divs = soup.find_all('div', class_='answer hentry a--box')
		for div in other_divs:
			name = div.find('a', class_='author a--author').text
			answer = div.find('div', class_='a--atext-value').text
			others.append({'name': name, 'answer': answer})

		answers = {
			'best' : { 'name': name_of_best, 'answer': answer_of_best },
			'others': others
		}

		return answers
	except Exception as err:
		print(err)
		print('закрываю браузер')
		browser.close()


def main():
	browser = start_browser()
	link = get_link_by_query(browser, 'привет как дела')
	answers = get_answers(browser, link)
	close_browser(browser)
	print(answers)


if __name__ == '__main__':
	main()




