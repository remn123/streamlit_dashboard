# Streamlit Dashboard

A simple dashboard sketch.

## Installation

Open a terminal and clone the repository:

```bash
git clone https://github.com/remn123/st_dashboard.git
```

Get into the project root folder with:

```bash
cd st_dashboard
```

## Create a virtual environment

### via python

Then you should create a virtual environment named .venv

```bash
python -m venv .venv
```

and activate the environment.

On Linux, OsX or in a Windows Git Bash terminal it's

```bash
source .venv/Scripts/activate
```

or alternatively

```bash
source .venv/bin/activate
```

In a Windows terminal it's

```bash
.venv/Scripts/activate.bat
```

## Install all dependencies

After your virtualenv has been activated, a `(.venv)` will appear on the left side of your terminal. Then, you may install the local requirements inside its virtual environment with:

```bash
pip install -r requirements.txt
```

## Run

### Run the application locally

```bash
streamlit run app.py
```

## Images

### Main Panel

![](docs/main.png?raw=true "Main Panel")

### BarPlot

![](docs/barplot.png?raw=true "BarPlot")
