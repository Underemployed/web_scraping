
import requests
from bs4 import BeautifulSoup
url =('https://internshala.com/internships/python-django-internship/')

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
internships = soup.find_all(class_="individual_internship")

for internship in internships:
    title = internship.find("a", class_="view_detail_button").text.strip()
    company = internship.find("a", class_="link_display_like_text").text.strip()
    duration = internship.find("div", class_="item_body").text.strip()
    stipend = internship.find("span", class_="stipend").text.strip()
    location = internship.find("a", class_="location_link").text.strip()
    link = "https://internshala.com" + internship.find("a", class_="view_detail_button")["href"]
    
    print("Title:", title)
    print("Company:", company)
    print("Duration:", duration)
    print("Stipend:", stipend)
    print("Location:", location)
    print("Link:", link)
    print()
