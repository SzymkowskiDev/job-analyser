import json
import logging
import os

from scrape_job_details import scrape_jobs
# from report_generator import generate_report
# from io_skills_to_titles import io_skills_to_titles
# from io_skills_to_skills import io_skills_to_skills
# from io_title_to_skills import io_title_to_skills

log_format = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

#scrape_jobs('https://justjoin.it/')
#generate_report('job_bank.json', 'stats.csv')

################################################################# FUNCTIONS FOR FRONTEND INTEGRATION
# can_apply_for = io_skills_to_titles(["Python", "SQL", "AWS"])
# recommended_skills = io_skills_to_skills(["Python", "SQL", "AWS"])
# needed_skills = io_title_to_skills("Data Engineer")