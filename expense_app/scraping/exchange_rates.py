import requests
from bs4 import BeautifulSoup

def get_usd_to_eur_rate():
    url = "https://www.xe.com/currencyconverter/convert/?From=USD&To=EUR"
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to fetch rate"

    soup = BeautifulSoup(response.text, 'html.parser')
    rate_element = soup.find('span', class_='result__BigRate-sc-1bsijpp-1')
    if rate_element:
        return rate_element.text.strip()
    else:
        return "Rate not found"