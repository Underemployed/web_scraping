import requests
from bs4 import BeautifulSoup
import time

def find_internships():
    # Prompt user to enter unfamiliar skills
    url="https://internshala.com/internships/work-from-home-internships/"
    unfamiliar_skills = input("Enter comma-separated list of unfamiliar skills\n>").split(',')
    print(f"\nFiltering Out {', '.join(unfamiliar_skills)}\n")

    # Send request and parse HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    internships = soup.find_all('div', class_='internship_meta')

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
            skills_list = ['N/A']

        # Check if unfamiliar skills are present
        is_unfamiliar_present = False
        for skill in unfamiliar_skills:
            if skill in skills_list:
                is_unfamiliar_present = True
                break

        if not is_unfamiliar_present:
            print(f'Title: {title}\nCompany: {company}\nDuration: {duration}\nStipend: {stipend}\nLocation: {location}\nLink: {link}\nSkills: {", ".join(skills_list)}\n{"<"+"=" * 100+">"}\n')

if __name__ == '__main__':
    while True:
        find_internships()
        time_wait=10
        print(f'Waiting Time {time_wait} minutes...')
        time.sleep(time_wait*60)
