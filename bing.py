import requests
from bs4 import BeautifulSoup as bs
import httpx
from dotenv import dotenv_values
import trafilatura
config = dotenv_values('.env')

limit_words = 300
async def extract_data(url):
	async with httpx.AsyncClient() as client:
		response = await client.get(url)
		return trafilatura.extract(response.text, timeout=5)

async def google_search(q):
	url = "https://www.googleapis.com/customsearch/v1"
	params = {
		'q': q,
		'key': config.get('csearchkey'),
		'cx': config.get('sengineid')
	}
	async with httpx.AsyncClient() as client:
		response = await client.get(url, params=params, timeout=30)
		print(response.json())
		if response.status_code != 200 or not 'items' in response.json().keys():
			return []
	data = response.json()
	items = data['items']#[:2]
	contents = []
	for i in items:
		name = i['title']
		url = i['link']
		print(url)
		snippet = i['snippet']
		if url.split('.')[1] == 'nasdaq':
			continue
		try:
			extracted = await extract_data(url)
			print(f"{extracted = }")
			if extracted and (len(extracted) > len(snippet)):
				snippet = extracted.replace("\n", '')
		except:pass
		contents.append({'name': name, 'url': url, 'content': snippet})
	return contents


def search_bing(query):
	api_key = config.get('bing_key1')
	endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/suggestions"
	endpoint = "https://api.bing.microsoft.com/v7.0/search"
	headers = {"Ocp-Apim-Subscription-Key": api_key}
	params = {"q": query}
	response = requests.get(endpoint, headers=headers, params=params)
	data = response.json()
	contents = []
	if "webPages" in data and "value" in data["webPages"]:
		print(data["webPages"]['webSearchUrl'] + f' dan {len(data["webPages"]["value"])} topilgan datalar\n\n')
		values = data["webPages"]['value']
		for i in values:
			name = i['name']
			url = i['url']
			content = i['snippet']
			got_content = extract_data(url)
			if got_content and content and len(got_content) > len(content):
				content = got_content
				content = ' '.join(content.split()[:limit_words])
			contents.append({'name': name, 'url': url, 'content': content})
		return contents
	return []

if __name__ == "__main__":
	items = google_search("Total short volume percentage of ‘AAPL’ stock")
	for i in items:
		print(i)
	# print(trafilatura.extract(trafilatura.fetch_url("ismailov.uz")))
