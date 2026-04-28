# Climate Challenge Week 0

This document explains how to reproduce the development environment, run the project, and understand the implementation details and individual contributions.

---

## Project Overview

The Climate Challenge Week 0 project focuses on analyzing historical climate data from multiple African countries to generate insights about temperature, rainfall, humidity, and other environmental variables.

The project includes:

- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Statistical comparison across countries
- Visual dashboards using Streamlit
- Reproducible development workflow

---

## Countries Included

- Ethiopia
- Kenya
- Sudan
- Tanzania
- Nigeria

---

## Main Variables Used

- **T2M** – Temperature at 2 meters
- **RH2M** – Relative Humidity at 2 meters
- **WS2M** – Wind Speed at 2 meters
- **PRECTOTCORR** – Corrected Precipitation
- **T2M_RANGE** – Temperature Range

---

# Development Environment Setup

## Prerequisites

- Git
- Python 3.11
- pip
- (Optional) Conda

---

## 1. Clone the Repository

```bash
git clone https://github.com/Melki123shi/climate-challenge-week0.git
cd climate-challenge-week0
```

---

## 2. Create and Activate an Environment

### Option A: Python venv

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Option B: Conda

```bash
conda create -n climate-week0 python=3.10 -y
conda activate climate-week0
```

---

## 3. Install Dependencies

If `requirements.txt` exists:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Verify Setup

```bash
python --version
pip --version
```

---

# Streamlit Dashboard Setup

## Run the Application

From the project root:

1. Install dependencies

```bash
pip install -r requirements.txt
```

1. Start the Streamlit app

```bash
streamlit run app.py
```

---

## Dashboard Features

- Interactive climate charts
- Country comparison tools
- Time-series trend analysis
- Filtering by variable and date
- Summary metric cards
- Clean and reusable data pipeline

---

# Project Implementation

## Data Processing Workflow

1. Load raw climate datasets
2. Handle missing values
3. Convert dates into datetime format
4. Standardize column names
5. Handle Outliers
6. Save the cleaned datasets
7. Load and merge the cleaned datasets
8. Apply Cross-Country Comparison & Climate Vulnerability Ranking
9. Provide interactive dashboard with streamlit

---

## Analysis Performed

### Exploratory Data Analysis

- Monthly average temperature trends
- Rainfall seasonality
- Correlation analysis between variables
- Outlier detection

### Statistical Testing

Used significance testing to compare countries:

- **One-Way ANOVA** for comparing mean T2M values
- **Kruskal-Wallis Test** for comparing distributions when normality assumptions may not hold

These tests help determine whether temperature differences across countries are statistically significant.

---

# My Contributions

The following contributions were completed as part of this project:

## Data Engineering

- Cleaned and merged climate datasets from five countries
- Prepared reusable preprocessing scripts
- Structured datasets for dashboard integration

## Analysis

- Created monthly and yearly trend comparisons
- Performed correlation analysis across climate variables
- Added ANOVA and Kruskal-Wallis significance testing for T2M

## Dashboard Development

- Built interactive Streamlit dashboard
- Added filters and visual comparisons
- Designed user-friendly metric summaries

## Documentation

- Improved README setup instructions
- Added reproducibility steps
- Documented implementation workflow and contributions

---

# Troubleshooting

## PowerShell Blocks Activation

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Wrong Python Version

Try:

```bash
python3 --version
```

## Missing Packages

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

# Future Improvements

- Add forecasting models
- Deploy dashboard online
- Add geospatial climate maps
- Automate daily data refresh pipeline

---

# Author

Melkishi Tesfaye
```
