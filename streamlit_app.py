import streamlit as st
from io_skills_to_skills import io_skills_to_skills
from io_skills_to_titles import io_skills_to_titles
from io_title_to_skills import io_title_to_skills
from util import load_file, persist_file, merge_dicts_without_overwrite
# io_title_to_skills(title='devops', n_skills=15)
# io_skills_to_skills(input_skills=['SQL', 'Python', 'AWS'], n_skills = 15)
# io_skills_to_titles(input_skills=['React'])

st.write('What positions match my experience?')
st.write('Provide skills that you already have and the program will output job titles you can hunt for.')

st.write('What new skills will allow me to apply for more job offers?')
st.write('Provide skills you already have and the program will output other skills worth learnig that would enable you to be a good match for more job openings.')

st.write('What skills do I need to be X?')
st.write('Enter job title you are interested in and the program will output skills required.')