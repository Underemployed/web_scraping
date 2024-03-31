import json

with open('scraped_data.json', 'r') as file:
    data = json.load(file)

new_data = {}

for course, years in data.items():
    new_data[course] = {}
    for year, semesters in years.items():
        for semester, subjects in semesters.items():
            if semester not in new_data[course]:
                new_data[course][semester] = {}
            new_data[course][semester].update(subjects)

new_json = json.dumps(new_data, indent=4)

with open('restructured_data.json', 'w') as file:
    file.write(new_json)