"""
Web scraper for reading data from https://apps.worldagroforestry.org/treedb2/.

All rights for content and research to original authors (citation below):

C, Mutua A, Kindt R, Jamnadass R, Simons A. 2009. Agroforestree Database: a tree reference and selection guide version 4.0. World Agroforestry Centre, Kenya. https://www.worldagroforestry.org/output/agroforestree-database

Purpose of this scraping exercise is to get the data into a more readable and easily navigable format. As well as introducing semantic search for easier knowledge discovery.

Work to be hosted on personal Github page and can be removed as requested by authors of content. 

Verbose documentation as practice for production-readiness.

"""

from typing import Iterator, NamedTuple, List 
import requests
from bs4 import BeautifulSoup
import re

class Scraper:

    """
    Basic web scraper that utilizes bs4 and requests.

    Attributes
    ----------
    base_url: str - base url for the scraper instance 
    req_delay: int - delay (ms) between requests
    """
    
    def __init__(self, url: str, req_delay: int=0):
        self.base_url = url
        self.req_delay = req_delay
    
    def fetch_html(self, url_add_on: str='') -> str:
        """Returns the html contents of url."""
        return requests.get(self.base_url + url_add_on).text


    def find_link_paths(self, html: str, match_str: str='') -> Iterator[str]:
        """
        Discovers all link paths in provided html document that (optionally) match
        match_str.
        """
        soup = BeautifulSoup(html, 'html.parser')
        href = re.compile(match_str) if match_str else True
        links = soup.find_all('a', href=href)
        return (l.get('href') for l in links)

    def parse_species_content(self, html: str, species_id: int) -> dict:
        soup = BeautifulSoup(html, 'html.parser')
        return {
            'species_name': self.parse_species_name(soup),
            'species_id': species_id,
            'products_and_services': [],
            'native_range': self.parse_native_range(soup)
        }

    def parse_species_name(self, soup: BeautifulSoup) -> str:
        try:
           return soup.find('h2').text
        except Exception as err:
            print(err)
            return 'species name not found'

    def parse_native_range(self, soup: BeautifulSoup) -> List[str]:
        rel_pre =  soup.find_all(lambda x: x.name == 'pre' and 'Native range' in x.text)[0]
        return rel_pre.find('br').next_sibling.split(',')


s = Scraper('https://apps.worldagroforestry.org/treedb2/speciesprofile.php')

html = s.fetch_html('?Spid=404')
print(s.parse_species_content(html, 404))
