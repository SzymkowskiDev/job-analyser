import streamlit as st
from io_skills_to_skills import io_skills_to_skills
from io_skills_to_titles import io_skills_to_titles
from io_title_to_skills import io_title_to_skills
from util import load_file, persist_file, merge_dicts_without_overwrite
import logging
from annotated_text import annotated_text

log_format = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

annotated_text(
    "Skills you need: ",
    ("java", "229"),
    ("spring", "117"),
    ("sql", "71"),
    ("javascript", "59"),
    ("kubernetes", "23"),
    ("microservices", "34")
)

st.image('assets/logo_new.png', caption="https://career-advice.it/market-research/")

st.header('What skills do I need to be X?')
st.write('Enter job title you are interested in and the program will output skills that are required in this position.')
input_wanted_title = st.text_input("Desired job title e.g. Java Developer")
n_skills = st.slider("Number of most frequently asked for skills to display", min_value=1, max_value=100, value=15)
n_most_frequent_skills, sample_size = io_title_to_skills(title=input_wanted_title, n_skills=n_skills)
st.write('Skills you need:')
st.json(n_most_frequent_skills, expanded=True)
st.write(f"{sample_size} sample size/job offers")
st.divider()

st.header('What positions match my experience?')
st.write('Provide skills that you already have and the program will output job titles you can hunt for.')
input_possessed_skills = st.text_input("Provide skills you have separated by comma e.g. css,html,javascript")
possessed_skills = input_possessed_skills.split(',')
n_titles = st.slider("Number of most frequent job titles matching these skills", min_value=1, max_value=100, value=15)
n_most_frequent_skills2, sample_size2 = io_skills_to_titles(possessed_skills, n_titles)
st.write('Your experience is a good match for:')
st.json(n_most_frequent_skills2, expanded=True)
st.write(f"{sample_size2} sample size/job offers")
st.divider()

st.header('What new skills will allow me to apply for more job offers?')
st.write('Provide skills you already have and the program will output other skills worth learnig that would enable you to be a good match for more job openings.')
input_possessed_skills2 = st.text_input("Provide skills you have separated by comma e.g. python,sql")
possessed_skills2 = input_possessed_skills2.split(',')
n_skills2 = st.slider("Number of skills to display:", min_value=1, max_value=100, value=15)
n_most_frequent_skills3, sample_size3 = io_skills_to_skills(input_skills=possessed_skills2, n_skills = 15)
st.write('Other skills worth learning to match more jobs:')
st.json(n_most_frequent_skills3, expanded=True)
st.write(f"{sample_size3} sample size/job offers")
st.divider()

st.markdown('''[https://github.com/SzymkowskiDev/job-analyser](https://github.com/SzymkowskiDev/job-analyser) :balloon:''')

