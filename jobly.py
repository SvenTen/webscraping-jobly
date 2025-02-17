import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_job_details():
    url = "https://www.jobly.fi/tyopaikat?search=it&job_geo_location=&Etsi+ty%C3%B6paikkoja=Etsi+ty%C3%B6paikkoja&lat=&lon=&country=&administrative_area_level_1="
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    job_elements = soup.find_all('div', class_='views-row')
    print(f"Found {len(job_elements)} job listings.")
    
    job_data = []

    for job in job_elements:
        try:
            title = job.find('h2', class_='node__title').text.strip()
        except:
            title = 'No title'
        
        try:
            date = job.find('span', class_='date').text.strip()
        except:
            date = 'No date'
        
        try:
            company = job.find('span', class_='recruiter-company-profile-job-organization').text.strip()
        except:
            company = 'No company'
        
        try:
            location = job.find('div', class_='location').text.strip()
        except:
            location = 'No location'
        
        try:
            logo_url = job.find('img')['src']
        except:
            logo_url = 'No logo'

        job_data.append([title, date, company, location, logo_url])

    return job_data

def save_to_excel(job_data):
  
    df = pd.DataFrame(job_data, columns=['Job Title', 'Date Published', 'Company', 'Location', 'Logo URL'])

    df.to_excel('job_listings.xlsx', index=False, engine='openpyxl')

if __name__ == '__main__':
   
    job_data = scrape_job_details()

    if job_data:
        save_to_excel(job_data)
        print(f"Data saved to 'job_listings.xlsx' with {len(job_data)} job listings.")
    else:
        print("No job data found.")
