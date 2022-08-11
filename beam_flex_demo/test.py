from pathlib import Path
import requests

if __name__ == '__main__':
    element=
    country_code='per'
    response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}?fields=name')
    print(response.json()['name']['common'])