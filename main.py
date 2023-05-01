import requests
from bs4 import BeautifulSoup
unfamiliar_skill=input('Put some skills you dont have\n>')
print(f'Filtering Out {unfamiliar_skill}')
url = 'https://internshala.com/internships/python-django-internship/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
internships = soup.find_all(class_='individual_internship')

for internship in internships:
    title = internship.find('a', class_='view_detail_button').text.strip()
    company = internship.find('a', class_='link_display_like_text').text.strip()
    duration = internship.find('div', class_='item_body').text.strip()
    stipend = internship.find('span', class_='stipend').text.strip()
    location = internship.find('a', class_='location_link').text.strip()
    link = 'https://internshala.com' + internship.find('a', class_='view_detail_button')['href']
    
    # Get skills
    intern_response = requests.get(link)
    intern_soup = BeautifulSoup(intern_response.text, 'html.parser')
    skills = intern_soup.find('div', class_='section_heading heading_5_5 skills_heading')
    if skills is not None:
        skills_container = skills.find_next_sibling('div', class_='round_tabs_container')
        skills_list = []
        for skill in skills_container.find_all('span', class_='round_tabs'):
            skills_list.append(skill.text.strip())
    else:
        skill_list = ['N/A']
    out=1

    if unfamiliar_skill not in skills_list:
        print(f'Title: {title.strip()}')
        print(f'Company: {company.strip()}')
        print(f'Duration: {duration.strip()}')
        print(f'Stipend: {stipend.strip()}')
        print(f'Location: {location.strip()}')
        print(f'Link: {link.strip()}')
        print(f'Skills: {", ".join(skills_list)}')
        print('<=================================================================================================================>')
