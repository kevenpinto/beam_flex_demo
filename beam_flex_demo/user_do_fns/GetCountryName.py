import requests
import apache_beam as beam

# https://restcountries.com/v3.1/alpha/per?fields=name

class GetCountryName(beam.DoFn):
    def process(self, element):
        """
        :param element: Country Code
        :return: List[]
        """
        country_code = element[0]
        response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}?fields=name')
        country_name = str(response.json()['name']['common'])
        yield [country_code,country_name]
