import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import math
import logging

class PropertyScraper:
    def __init__(self, base_url, api_key, pagination_url, num_pages=None):
        self.base_url = base_url
        self.api_key = api_key
        self.pagination_url = pagination_url
        self.num_pages = num_pages
        self.all_property_dict_link = {}

    def fetch_total_pages(self):
        # Send a GET request to the proxy with pagination URL to get the total number of pages
        response = requests.get(
            url=self.base_url,
            params={
                'api_key': self.api_key,
                'url': self.pagination_url,
                'country': 'us',
            },
        )

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the span element containing the total number of properties
            properties_found_span = soup.find('span', class_="search-results-listings-header__properties-found__number")

            # Extract the total number of properties and calculate the number of pages
            total_properties = float(properties_found_span.text.strip())
            self.num_pages = math.ceil(total_properties / 11.0)

            logging.info(f"Total number of properties: {total_properties}")
            logging.info(f"Calculated number of pages: {self.num_pages}")

        else:
            logging.error(f"Request to get total properties was not successful. Status code: {response.status_code}")

    def scrape_pagination_links(self):
        
        for page_number in range(1, self.num_pages + 1):
            url = f'{self.pagination_url}?search=true&regions%5B0%5D=8&regions%5B1%5D=1&regions%5B2%5D=17&regions%5B3%5D=114&regions%5B4%5D=12&regions%5B5%5D=9&regions%5B6%5D=5&regions%5B7%5D=11&regions%5B8%5D=14&regions%5B9%5D=15&regions%5B10%5D=13&regions%5B11%5D=4&regions%5B12%5D=6&regions%5B13%5D=16&regions%5B14%5D=31&regions%5B15%5D=10&regions%5B16%5D=7&regions%5B17%5D=115&regions%5B18%5D=3&regions%5B19%5D=2&regions%5B20%5D=257&parent=1&pageNumber={page_number}'

            response = requests.get(
                url=self.base_url,
                params={
                    'api_key': self.api_key,
                    'url': url,
                    'country': 'us',
                },
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                ul_element = soup.find('ul', class_='search-results-listings-list')

                li_elements = ul_element.find_all('li')

                for li_element in li_elements:
                    a_tag = li_element.find('a')
                    
                    if a_tag:
                        self.all_property_dict_link[li_element.get('id')] = a_tag.get('href')
                    else:
                        logging.info(f'No <a> tag found within <li> element.')
            else:
                logging.error(f"Request for page {page_number} was not successful. Status code: {response.status_code}")

    
    def scrape_property_details(self):
        columns = ['URL', 'Date', 'Type', 'Street Address', 'City', 'Region', 'Phone Numbers', 'Solicitation Message', 'Asking Price', 'Municipal Assessment']
        df = pd.DataFrame(columns=columns)

        for listing_id, url in self.all_property_dict_link.items():
            logging.info(f"Visiting {listing_id} - {url}")
            response = requests.get(
                url=self.base_url,
                params={
                    'api_key': self.api_key,
                    'url': url, 
                    'country': 'us', 
                },    
            )

            if response.status_code == 200:
                
                # Initializing the required feilds to scrape
                phoneNumbers = solicitation_message = asking_price = municipal_assessment = type = street = city = region = None

                # set the datetime
                date = datetime.now()

                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                type = soup.find('h3',class_='listing-location__title')
                type = type.text.strip()
                
                address_element = soup.find('div',class_='listing-location__address')
                if address_element:
                    street_address = address_element.find('h1').text.strip()
                    street = street_address

                    span_element = address_element.find('h2')
                    city_element, region_element = span_element.find_all('span', recursive=False)
                    city = city_element.text.strip()
                    region = region_element.text.strip()
                else:
                    logging.info('Address element not found.')
                
                phone_elements = soup.find_all('a',class_='gtm-listing-link-contact-owner-phone')
                phone_numbers = [phone_element.find('span').text.strip() for phone_element in phone_elements]
                unique_phone_numbers = set(phone_numbers)
                phone_numbers = list(unique_phone_numbers)
                phoneNumbers = ', '.join(phone_numbers)

                message = soup.find('p',class_='listing-contact__no-solicitations-body')
                if message:
                    solicitation_message = 'y'
                else:
                    solicitation_message = 'n'

                characteristics_viewports = soup.find_all('div',class_='listing-list-characteristics__viewport')
                for viewport in characteristics_viewports:
                    # Find all the listing-box__dotted-row elements within the current viewport
                    dotted_rows = viewport.find_all('div', class_='listing-box__dotted-row')
                    
                    for dotted_row in dotted_rows:
                        # Extract the text content of the first div (characteristic name)
                        characteristic_name = dotted_row.find('div').text.strip()

                        # Extract the text content of the third div (characteristic value)
                        characteristic_value = dotted_row.find_all('div')[2].text.strip()
                        
                        # Check if the characteristic name is "Asking Price" or "Municipal Assessment"
                        if characteristic_name == 'Asking Price':
                            asking_price1 = characteristic_value
                            asking_price = asking_price1
                        elif characteristic_name == 'Municipal Assessment':
                            municipal_assessment1 = characteristic_value
                            municipal_assessment = municipal_assessment1

                # Append extracted values to the DataFrame
                df = pd.concat([df, pd.DataFrame([{
                    'URL': url,
                    'Date': date,
                    'Type': type,
                    'Street Address': street,
                    'City': city,
                    'Region': region,
                    'Phone Numbers': phoneNumbers,
                    'Solicitation Message': solicitation_message,
                    'Asking Price': asking_price,
                    'Municipal Assessment': municipal_assessment
                }])], ignore_index=True)
            else:
                logging.error(f"Request for {listing_id} was not successful. Status code: {response.status_code}")            
        return df
    
    def saveToCSV(self,df):
        df.to_csv("output.csv", index=False)
        logging.info(f"CSV file saved successfully")
        