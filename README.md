# Data\_Science\_Project

A small end‑to‑end data science project demonstrating:

1. **Data Collection** via web scraping (BeautifulSoup, Scrapy, Selenium).
2. **Data Storage** of raw and processed files in `data/`.
3. **Exploratory Data Analysis** and visualization in a Jupyter notebook.

---

## Table of Contents

* [Project Structure](#project-structure)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)

  * [Ad‑hoc Python Scrapers](#ad‑hoc-python-scrapers)
  * [Scrapy Spiders](#scrapy-spiders)
  * [Exploratory Data Analysis](#exploratory-data-analysis)
* [Directory Layout](#directory-layout)
* [Contributing](#contributing)
* [License](#license)

---

## Project Structure

```plaintext
Data_Science_Project/
├── data/                   # Raw and processed datasets (CSV, JSON, etc.)
├── scraping/               # Standalone Python scripts (BeautifulSoup, Selenium)
├── spider/                 # Scrapy project and spider definitions
├── data_analysis.ipynb     # Jupyter notebook for EDA & visualization
└── README.md               # Project overview and instructions
```

---

## Prerequisites

* Python 3.8 or higher
* Git (to clone this repository)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/soupond/Data_Science_Project.git
   cd Data_Science_Project
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   > If a `requirements.txt` is not present, install manually:
   >
   > ```bash
   > pip install pandas numpy matplotlib jupyter scrapy beautifulsoup4 requests selenium
   > ```

---

## Usage

### Ad‑hoc Python Scrapers

Standalone scripts using BeautifulSoup or Selenium are located in `scraping/`. To run one:

```bash
python scraping/bs4_scraper.py
```

The script will save output files under `data/` (e.g., `data/raw_listings.csv`).

### Scrapy Spiders

The Scrapy project lives in the `spider/` directory. To crawl and export data:

```bash
cd spider
scrapy crawl dubizzle -o ../data/dubizzle_listings.csv
scrapy crawl bayut    -o ../data/bayut_listings.csv
```

* Each run generates or overwrites the specified CSV in `data/`.
* Modify spider settings or add new spiders under `spider/spiders/` as needed.

### Exploratory Data Analysis

Launch Jupyter Notebook and open the analysis notebook:

```bash
jupyter notebook data_analysis.ipynb
```

Inside, you’ll find:

* Data loading and cleaning steps
* Descriptive statistics and data summaries
* Visualizations (histograms, scatter plots, heatmaps)
* Key insights and recommendations

---

## Directory Layout

```plaintext
├── data/
│   ├── raw/                # Original scraped data
│   └── processed/          # Cleaned and transformed data
├── scraping/
│   ├── bs4_scraper.py      # Example BeautifulSoup scraper
│   └── selenium_scraper.py # Example Selenium-based scraper
├── spider/
│   ├── scrapy.cfg
│   └── spiders/
│       ├── dubizzle.py
│       └── bayut.py
├── data_analysis.ipynb     # Notebook with EDA and charts
├── requirements.txt        # Python package requirements
└── README.md               # This file
```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit with a clear message.
4. Push to your fork and open a Pull Request.

Please ensure:

* Code follows PEP8 style guidelines.
* Dependencies are updated in `requirements.txt`.
* README is kept up to date with any new scripts or features.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
