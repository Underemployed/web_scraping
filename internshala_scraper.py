import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.ktuqbank.com/p/ktu-2019-batch-btech-syllabus.html"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table with the specified ID
    table = soup.find("table", {"class": "table-mc-blue"})

    # Check if the table is found
    if table:
        # Create a dictionary to store links for each branch and year
        links_dict = {}

        # Extract data from the table
        rows = table.find_all("tr")

        for row in rows:
            # Extract data from each cell in the row
            cells = row.find_all("td")

            # Check if there are at least 3 cells (branch, year, and buttons)
            if len(cells) >= 3:
                # Extract branch name and year
                branch_name = cells[1].text.strip()
                year_buttons = cells[2].find_all("button")

                # Create a dictionary to store links for the current branch
                branch_links = {}

                for button in year_buttons:
                    year = button.find("span").text
                    link = button.get("onclick").split("'")[
                        1
                    ]  # Extract link from onclick attribute
                    branch_links[year] = link

                # Add the branch and its links to the main dictionary
                links_dict[branch_name] = branch_links

        # Convert the dictionary to a pandas DataFrame
        df = pd.DataFrame.from_dict(links_dict, orient="index")

        # Export the DataFrame to an Excel file
        excel_filename = "ktu_links.xlsx"
        df.to_excel(excel_filename)
        print(f"Data has been exported to {excel_filename}")

    else:
        print("Table not found on the webpage.")

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
