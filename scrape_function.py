
import requests
from bs4 import BeautifulSoup
import json


def scrape_and_save(name, link):
    response = requests.get(link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", {"class": "table-mc-blue"})

        if table:
            links_dict = {}

            rows = table.find_all("tr")

            for row in rows:
                cells = row.find_all("td")

                if len(cells) >= 3:
                    branch_name = cells[1].text.strip()
                    year_buttons = cells[2].find_all("button")

                    branch_links = {}

                    for button in year_buttons:
                        year = button.find("span").text
                        link = button.get("onclick").split("'")[1]
                        branch_links[year] = link

                    links_dict[branch_name] = branch_links

            with open(f"{name}_links.json", "w") as file:
                json.dump(links_dict, file, indent=2)

        else:
            print(f"Table not found on the webpage: {link}")

    else:
        print(
            f"Failed to retrieve the webpage {link}. Status code: {response.status_code}"
        )


scrape_and_save(
    "branch and yr links",
    "https://www.ktuqbank.com/p/ktu-2019-batch-btech-syllabus.html",
)
