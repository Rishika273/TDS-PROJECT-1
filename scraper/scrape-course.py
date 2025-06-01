import requests
from bs4 import BeautifulSoup
def scrape_course_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # Adjust the selector based on the actual HTML structure of the course content
    content = soup.find_all('div', class_='course-content')  # Example class
    return [item.text.strip() for item in content]
url='https://tds.s-anand.net/#/2025-01/'
scrape_course_content(url)