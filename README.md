# Climate Challenge Week 0

This document describes how to reproduce the development environment for this project.

## Prerequisites

- Git
- Python 3.11
- pip
- (Optional) Conda

## 1. Clone the repository

```bash
git clone https://github.com/Melki123shi/climate-challenge-week0.git
cd climate-challenge-week0
```

## 2. Create and activate an environment

### Option A: Python venv

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Option B: Conda

```bash
conda create -n climate-week0 python=3.10 -y
conda activate climate-week0
```
## 3. Install dependencies

Use the dependency file present in the repository.

If `requirements.txt` exists:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Verify setup

```bash
python --version
pip --version
```

## Troubleshooting

- Activate the environment before running installs or scripts.
- If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

- If `python` is not the expected version, try `python3`.

# Streamlit dashboard Setup

To fetch, clean, and prepare climate data for the Streamlit dashboard.

## How to run the application

From the project root:

1. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
2. Start the Streamlit app:
	```bash
	streamlit run app.py
	```

## Features

- Data loading and preparation helpers
- Interactive charts and visual summaries
- Filtering by variable, location, or time range
- Metric cards and trend views
- Reusable scripts for repeatable data preparation
