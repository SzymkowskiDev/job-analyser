import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging
import os

log_format = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


def get_snapshot(url: str) -> dict:
    """Scrapes all currently loaded job offers visible on a justjoin.it page"""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        job_elements = soup.select('div[data-index][data-known-size][data-item-index][item]')
        container = {}
        for element in job_elements:
            job_title_element = element.select_one('h2.css-16gpjqw')
            job_title = job_title_element.text.strip() if job_title_element else 'N/A'
            link_element = element.select_one('a.css-4lqp8g')
            link = link_element.get('href') if link_element else 'N/A'
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            required_skills = None            
            description = None
            salary_min = None
            salary_mid = None
            salary_max = None
            company = None
            city = None
            container.update({
                "https://justjoin.it/" + link: {
                    "job_title": job_title,
                    "required_skills": required_skills,
                    "description": description,
                    "salary_min": salary_min,
                    "salary_mid": salary_mid,
                    "salary_max": salary_max,
                    "company": company,
                    "city": city,
                    "created_at": created_at
                }
            })
        logging.debug(f"Snapshot for URL:({url}) resulted with output of lenght: {len(container)}")
    else:
        logging.error(f"Failed to fetch the page. Status code: {response.status_code}")

    return container


def do_snapshots(url: str, max_index: int = 500, interval: int = 50) -> dict:
    """Scrapes all job offers from given justjoin.it job board using get_snapshot() function by travelling over url path indexes"""
    data = {}    
    for i in range(0, max_index, interval):
        url_with_index = url+str(i)
        logging.debug(f"url_with_index is: {url_with_index}")
        snapshot = get_snapshot(url_with_index)
        data.update(snapshot)
    logging.info(f"{len(data)} job offers have been scraped from URL: {url}")
    return data


def scrape_details(job_bank):
    job_bank_enhanced = {}
    for job_url, job_details in job_bank.items():
        response = requests.get(job_url)
        soup = BeautifulSoup(response.content, "html.parser")
        field = soup.find('div', class_='MuiBox-root css-8dhpgu').text
        skills_elements = soup.select('div.css-cjymd2 h6.MuiTypography-subtitle2.css-x1xnx3')
        required_skills = [skill.text.strip() for skill in skills_elements]      
        description_element = soup.select_one('div.css-ncc6e2')
        description = description_element.text.strip() if description_element else None
        salary_min = None
        salary_max = None
        salary_mid = None
        company_element = soup.select_one('div.css-1yxroko')
        company = company_element.text.strip() if company_element else None
        city_element = soup.select_one('div.css-e37z09')
        city = city_element.text.strip() if city_element else None
        job_bank_enhanced.update({job_url: {
                "job_title": job_details["job_title"],
                "field": field,
                "required_skills": required_skills,
                "description": description,
                "salary_min": salary_min,
                "salary_mid": salary_mid,
                "salary_max": salary_max,
                "company": company,
                "city": city,
                "created_at": job_details["created_at"]
                }})  
    return job_bank_enhanced


def save_data(data, filename = "job_bank.json"):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        logging.info(f"{len(data)} job offers have been saved to: {filename}")


def scrape_jobs(url="https://justjoin.it/"):
    logging.info("Generating job_bank.json in progress ...")
    snapshots = do_snapshots(url, max_index = 10000)
    save_data(snapshots, "job_bank.json")
    logging.info("Generating job_bank_enhanced.json in progress ...")
    enhanced_data = scrape_details(snapshots)
    save_data(enhanced_data, "job_bank_enhanced.json")

scrape_jobs()


