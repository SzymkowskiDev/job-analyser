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


def get_snapshot(url: str) -> dict:
    """Scrapes all currently loaded job offers visible on a justjoin.it page"""
    response = requests.get(url)
    container = {}
    status = None
    if response.status_code == 200:
        if 'We did not find any offers for the above search criteria.' in response.text:
            logging.debug("We did not find any offers for the above search criteria.")
            status = 'We did not find any offers for the above search criteria.'
        if status != 'We did not find any offers for the above search criteria.':
            soup = BeautifulSoup(response.content, "html.parser")
            job_elements = soup.select('div[data-index][data-known-size][data-item-index][item]')
            for element in job_elements:
                job_title_element = element.select_one('h2.css-16gpjqw')
                job_title = job_title_element.text.strip() if job_title_element else 'N/A'
                link_element = element.select_one('a.css-4lqp8g')
                link = link_element.get('href') if link_element else 'N/A'
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                container.update({"https://justjoin.it/" + link: {"job_title": job_title, "created_at": created_at}})
            logging.debug(f"Snapshot for URL:({url}) resulted with output of lenght: {len(container)}")
    else:
        logging.error(f"Failed to fetch the page. Status code: {response.status_code}")
    return container, status


def do_snapshots(url: str, max_index: int = 500, interval: int = 50) -> dict:
    """Scrapes all job offers from given justjoin.it job board using get_snapshot() function by travelling over url path indexes"""
    data = {}    
    for i in range(0, max_index, interval):
        logging.info(f"{int((i)/interval)} / {int(max_index/interval)} snapshot in progress ...")
        url_with_index = url+str(i)
        snapshot, status = get_snapshot(url_with_index)
        logging.info(f"{len(snapshot)} job offers in snapshot for: {url_with_index}")
        data.update(snapshot)
        if status == 'We did not find any offers for the above search criteria.':
            logging.debug(f"{i} index no more results (breaking the loop).")
            break
    logging.info(f"{len(data)} job offers have been scraped from URL: {url}")
    return data


def scrape_infinite_scroll(output, max_index=4500, website = 'https://justjoin.it/?index='):
    """Scrapes urls from inifnite scroll and saves them to current_snapshot.json"""
    start_time = time.time()
    current_snapshot = load_file(input_filename=output, create=True)
    len_current_snapshot_before = len(current_snapshot)
    logging.info(f"Scraping of {website} in progress ...")
    snapshots = do_snapshots(website, max_index)
    repeated_items_count = 0
    new_items_count = 0
    for key, value in snapshots.items():
        if key not in current_snapshot:
            current_snapshot[key] = value
            new_items_count += 1
        else:
            repeated_items_count += 1
    logging.info(f"{repeated_items_count} job offers have been scraped before (these offers will not be updated)")
    logging.info(f"{new_items_count} new job offers have been scraped from this site and added to the current_snapshot")
    logging.info(f"{len(current_snapshot)} is the total number of job offers in current_snapshot")
    len_current_snapshot_after = len(current_snapshot)
    logging.info(f"{len_current_snapshot_after - len_current_snapshot_before} scraped_new job offers")
    logging.info(f"------------------------------------------")
    persist_file(input_data=current_snapshot, output_filename=output)
    end_time = time.time()
    logging.info(f"{round(end_time - start_time, 2)} sec scrape_infinite_scroll()")


if __name__ == '__main__':
	scrape_infinite_scroll(output='data/current_snapshot.json', max_index=5000, website='https://justjoin.it/?index=')