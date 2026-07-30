# Course Equivalence Analyzer

![Status](https://img.shields.io/badge/status-completed-brightgreen?style=for-the-badge)

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.27%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)

## Overview

The **Course Equivalence Analyzer** is an interactive tool designed to simplify and speed up the process of checking course equivalence rules between different universities or curricula.

The project was developed to automate an existing course equivalence analysis process at the Institute of Computing at the Federal University of Rio de Janeiro (IC/UFRJ), replacing manual searches in complex documents and spreadsheets with a simple web interface.

The application allows coordinators, administrators, or students to upload a centralized spreadsheet containing equivalence rules. Based on this data, users can select the institution of origin, enter a list of course codes, instantly find their equivalent courses, and generate a formal PDF report at the end of the process.

## Key Features

- **Flexible data source:** upload a spreadsheet (`.xlsx` or `.csv`) containing course equivalence rules, allowing the tool to adapt to different institutions or curricula.
- **Dynamic search:** select the institution of origin and enter multiple course codes for simultaneous analysis.
- **Immediate results:** the search logic displays course equivalence results directly on the page.
- **PDF report generation:** export a clean and formal `.pdf` report with the analysis results.
- **Simple interface:** built with Streamlit to provide a focused and straightforward user experience.

## How to Use

The workflow is divided into clear steps inside the interface:

1. **Upload the equivalence rules spreadsheet**
   - In the upload section, select the spreadsheet (`.xlsx` or `.csv`) containing the equivalence rules.
   - The application loads and prepares the data for analysis.

2. **Select the institution and enter course codes**
   - Choose the **institution of origin** from the dropdown menu.
   - Enter the **course codes** you want to analyze. Codes can be separated by spaces, commas, or line breaks.

3. **Analyze the results**
   - Click the analysis button.
   - The system searches for matching equivalence rules and displays the results on the page.

4. **Download the PDF report**
   - If all inserted courses are found, a download button becomes available.
   - Click it to save a formal report with the analysis results.

## Project Structure

The project is modularized to improve maintainability and scalability.

- `main.py`: Streamlit application entry point. It orchestrates the interface flow, manages `st.session_state`, and calls the other modules.
- `/components`: UI components such as header, sidebar, file uploader, and other interface elements.
- `data_loader.py`: functions for loading, validating, and preprocessing the uploaded spreadsheet.
- `core.py`: main application logic, including the `find_equivalencies` function that searches for equivalence rules.
- `pdf_generator.py`: generates the PDF report from the analysis results.
- `/assets`: static files such as favicon and application logo.
