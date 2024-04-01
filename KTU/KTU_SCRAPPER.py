import requests
from bs4 import BeautifulSoup
import json


def scrape_and_save(
    name="syllabus",
    link="https://www.ktuqbank.com/p/ktu-2019-batch-btech-syllabus.html",
):
    response = requests.get(link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", {"class": "table-mc-blue"})

        if table:
            links_dict = {}
            data_dict = {}

            rows = table.find_all("tr")

            for row in rows:
                cells = row.find_all("td")

                if len(cells) >= 3:
                    branch_name = cells[1].text.strip()
                    semester_buttons = cells[2].find_all("button")

                    branch_links = {}
                    branch_data = {}

                    for button in semester_buttons:
                        semester = button.find("span").text
                        link = button.get("onclick").split("'")[1]
                        branch_links[semester] = link

                        semester_data = {}
                        response = requests.get(link, timeout=2000)

                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, "html.parser")

                            tables = soup.find_all(
                                "table",
                                {
                                    "class": "table table-bordered table-striped table-hover table-mc-blue"
                                },
                            )

                            if tables:
                                for i, table in enumerate(tables):
                                    course_semester = f"s{semester}"
                                    semester_data[course_semester] = {}
                                    rows = table.find_all("tr")[1:]

                                    for row in rows:
                                        cells = row.find_all("td")
                                        if len(cells) == 2:
                                            course_name = (
                                                cells[0].find("center").text.strip()
                                            )
                                            try:
                                                drive_link = (
                                                    cells[1]
                                                    .find("button")
                                                    .get("onclick")
                                                    .split("'")[1]
                                                )
                                            except AttributeError as e:
                                                print(
                                                    f"Error extracting link for {course_name}: {e}"
                                                )
                                                drive_link = link

                                            semester_data[course_semester][
                                                course_name
                                            ] = drive_link

                            else:
                                print("Table not found on the webpage.")
                        else:
                            print(
                                "Failed to retrieve the webpage. Status code:",
                                response.status_code,
                            )

                        branch_data[semester] = semester_data

                    links_dict[branch_name] = branch_links
                    data_dict[branch_name] = branch_data

            new_data = {}
            for course, years in data_dict.items():
                new_data[course] = {}
                for year, semesters in years.items():
                    for semester, subjects in semesters.items():
                        if semester in new_data[course]:
                            new_data[course][semester].extend(subjects)
                        else:
                            new_data[course][semester] = subjects
            with open(f"{name}.json", "w") as output_file:
                json.dump(new_data, output_file, indent=2)

            print("Data saved as 'syllabus.json'")
        else:
            print(f"Table not found on the webpage: {link}")
    else:
        print(
            f"Failed to retrieve the webpage {link}. Status code: {response.status_code}"
        )

    return new_data


scrape_and_save()
