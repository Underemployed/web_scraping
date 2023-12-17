import requests
from bs4 import BeautifulSoup
import json


def scrape_table_data(
    link="https://www.ktuqbank.com/2020/07/first-year-year-1-syllabus_20.html",
):
    data_dict = {}
    response = requests.get(link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all(
            "table",
            {"class": "table table-bordered table-striped table-hover table-mc-blue"},
        )

        if tables:
            # Extract data from the table
            for rows in tables:
                rows = rows.find_all("tr")[1:]  # Exclude header row
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) == 2:
                        course_name = cells[0].find("center").text.strip()
                        try:
                            drive_link = (
                                cells[1].find("button").get("onclick").split("'")[1]
                            )
                        except AttributeError as e:
                            # If an error occurs, store the entire element
                            print(f"Error extracting link for {course_name}: {e}")
                            drive_link = "nil"

                        data_dict[course_name] = drive_link

        else:
            print("Table not found on the webpage.")
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)

    return data_dict


# Call the function with the provided link
# scrape_table_data()
