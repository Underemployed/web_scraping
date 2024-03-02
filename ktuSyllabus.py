import requests
from bs4 import BeautifulSoup
import json

import yr_scrapper


def scrape_table_data(links_file="Branch.json", data_dict={}):
    with open(links_file, "r") as file:
        links_data = json.load(file)

    for branch_name, year_links in links_data.items():
        print(f"|||||||||||||{branch_name}||||||||||", year_links)
        branch_data = {}

        for year, link in year_links.items():
            year_data = yr_scrapper.scrape_table_data(link)
            branch_data[year] = year_data

        data_dict[branch_name] = branch_data

    with open("scraped_data.json", "w") as output_file:
        json.dump(data_dict, output_file, indent=2)

    print("Data saved as 'scraped_data.json'")


# Call the function with the provided link
scrape_table_data()
