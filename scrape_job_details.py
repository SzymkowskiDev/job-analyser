import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging
import os
import time
from util import load_file, persist_file, merge_dicts_without_overwrite

log_format = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


current_snapshot = load_file(input_filename='data/current_snapshot.json', create=True)


def scrape_details(current_snapshot):
    current_snapshot_appended = {}
    processed_offer = 0
    for job_url, job_details in current_snapshot.items():
        logging.info(f"{processed_offer} / {len(current_snapshot)} url processed ...")
        processed_offer += 1
        try:
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
            current_snapshot_appended.update({job_url: {
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
        except Exception as ex:
            logging.error(f"Job details not appended for {job_url} error: {ex}")
            continue
    return current_snapshot_appended


def scrape_job_details(output1, output2):
    "Appends current_snapshot.json with additonal attributes and accumulates in sink"
    start_time = time.time()
    current_snapshot_appended = scrape_details(current_snapshot)
    persist_file(input_data=current_snapshot_appended, output_filename=output1)
    existing_sink = load_file(input_filename=output2, create=True, log_success=True)
    sink_old_and_new = merge_dicts_without_overwrite(dict1=existing_sink, dict2=current_snapshot_appended)
    persist_file(input_data=sink_old_and_new, output_filename=output2)
    end_time = time.time()
    logging.info(f"{round(end_time - start_time, 2)} sec scrape_job_details()")


if __name__ == '__main__':
	scrape_job_details(output1='data/current_snapshot.json', output2='data/sink.json')