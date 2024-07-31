# Dashboard Candidates


## Overview Project

THis project **Dashboard Candidates** was developed to provide an overview of candidates for Data Analyst, Data Scientist and Data Engineer positions. The candidates are students of the courses **PED - Preparation for Interviews in Data** and **EBA - Statistics from Basic to Advanced**. The dashboard was created using Streamlit and allows recruiters to filter and view candidates according to the requirements of available vacancies.

## Functionalities

- **Overview of Candidates**:
  - View a general distribution of the positions sought by candidates.
  - See the distribution of seniorities.
  - Get the total number of available candidates.
  - See the percentages of candidates available to change.

- **Candidate Filtering**:
  - **Desired Position**: Select the desired positions (Data Analyst, Data Scientist, Data Engineer, etc.).
  - **Working Modality**: Choose between working modalities (in-person, remote, hybrid).
  - **Mastered Tools**: Filter candidates based on mastered tools and skills.
  
- **Data Export**:
  - Export the filtered candidate list to an Excel file.

## Technologies Used

- **Streamlit**: Framework for building interactive web applications in Python.
- **Pandas**: Library for data manipulation and analysis.
- **Openpyxl**: Library for reading and writing Excel files.
- **Plotly**: Library for creating interactive graphs (optional).

## Install and settings:

### Clone the repository:
```bash
git clone https://github.com/VanGaigher/Dashboard_Candidates.git
cd Dashboard_Candidates
```
### Setting the correct Python version using pyenv:

pyenv install 3.11.9
pyenv local 3.11.9

### Setting poetry to Python in 3.11.9 version and activate the virtual enviroment:

poetry env use 3.11.9
poetry shell

### Install all project dependencies: 

poetry install

### Run localy the app streamlit

poetry run streamlit app/1_home.py

### Secrets.toml

Ensure that you have your Google Sheets credentials saved into a .streamlit/secrets.toml in the project roots
