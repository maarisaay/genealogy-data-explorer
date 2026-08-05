# Genealogy Data Explorer

Genealogy Data Explorer is an interactive Streamlit application for exploring and analyzing genealogy data stored in GEDCOM files.

The project aims to provide a simple interface for browsing family tree data without requiring dedicated genealogy software.

## Current Features
- Upload GEDCOM (.ged) files
- Parse individual records
- Display basic person information
- Support multiple file encodings, including:
    - UTF-8
    - UTF-16
    - Windows-1250
    - Windows-1252
    - ISO-8859-2
- Automatic encoding detection
- Basic parser tests with pytest

## Planned Features
- Search people by name, surname, birth date and place
- Advanced filtering
- Person detail view
- Family relationships
- Ancestor and descendant trees
- Duplicate person detection
- Genealogy data quality checks
- Statistics and visualizations
- Location-based analysis

## Installation
Clone the repository:
```bash
git clone https://github.com/maarisaay/genealogy-data-explorer
cd cd genealogy-data-explorer
```

Create a virtual environment:
```bash
python -m venv .venv
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application
Start the Streamlit application:
```bash
python -m streamlit run app.py
```
Then open the local Streamlit address displayed in the terminal.

## Running Tests
```bash
pytest -v
```

## Privacy
GEDCOM files are processed locally by the application. Personal genealogy files should not be committed to the repository.

The `data/` directory is excluded from version control.

## Project Status
Early development - the current version focuses on GEDCOM file parsing and upload support.

