import requests
from bs4 import BeautifulSoup


def scrape_table_data(year=2, link="http://www.ktuqbank.com/2020/07/first-year-year-1-syllabus_20.html"):
    data_dict = {}
    response = requests.get(link,timeout=2000)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table", {"class": "table table-bordered table-striped table-hover table-mc-blue"})

        if tables:
            # Extract data from the table
            for i, table in enumerate(tables):
                semester = f"s{(year-1)*2+i+1}"  # Calculate semester based on year
                data_dict[semester] = {}
                rows = table.find_all("tr")[1:]  # Exclude header row

                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) == 2:
                        course_name = cells[0].find("center").text.strip()
                        try:
                            drive_link = cells[1].find("button").get("onclick").split("'")[1]
                        except AttributeError as e:
                            # If an error occurs, store the entire element
                            print(f"Error extracting link for {course_name}: {e}")
                            drive_link = link 

                        data_dict[semester][course_name] = drive_link

        else:
            print("Table not found on the webpage.")
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)

    return data_dict
# Call the function with the provided link
# data_dict = scrape_table_data()
# for semester, courses in data_dict.items():
#     print("Semester:", semester)
#     for course_name, drive_link in courses.items():
#         print("Course:", course_name)
#         print("Drive Link:", drive_link)
#         print()

