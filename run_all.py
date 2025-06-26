# run_all.py – Full Setup Script for Film Success Analysis Project
# Author: Bria Tran
# Description: This script orchestrates the complete local setup process for the project,
# including virtual environment creation, dependency installation, data ingestion, enrichment,
# machine learning model training, and launching the final Streamlit dashboard.

import os
import subprocess
import sys
import platform
import venv

# Define Project Folder Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, "venv")
DATABASE_DIR = os.path.join(BASE_DIR, "database")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
API_DIR = os.path.join(BASE_DIR, "api_modules")
APP_DIR = os.path.join(BASE_DIR, "streamlit_app")

# Pipeline Script Sequence
# Each script performs a modular task in the pipeline:
# 1. Schema setup → 2. Country metadata → 3. GDP fetching → 4. Filling tables
# 5. Core transformations → 6. ML training for hit prediction
PIPELINE_STEPS = [
    os.path.join(DATABASE_DIR, "init_db.py"),
    os.path.join(API_DIR, "country_api.py"),
    os.path.join(API_DIR, "world_bank_api.py"),
    os.path.join(SCRIPTS_DIR, "fetch_gdp_data.py"),
    os.path.join(SCRIPTS_DIR, "populate_missing_tables.py"),
    os.path.join(SCRIPTS_DIR, "data_pipeline.py"),
    os.path.join(SCRIPTS_DIR, "train_model.py")
]

# Create Virtual Environment
def create_virtualenv():
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
    else:
        print("Virtual environment already exists.")

# Install Dependencies from requirements.txt
def install_requirements():
    print("Installing requirements...")
    pip_path = os.path.join(VENV_DIR, "Scripts" if platform.system() == "Windows" else "bin", "pip")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])

# Run Any Python Script Inside the Venv Interpreter
def run_script(script_path):
    python_path = os.path.join(VENV_DIR, "Scripts" if platform.system() == "Windows" else "bin", "python")
    result = subprocess.run([python_path, script_path])
    if result.returncode != 0:
        print(f"Failed at: {script_path}")
        sys.exit(1)

# Launch Final Dashboard UI
def launch_dashboard():
    print("Launching Streamlit dashboard...")
    streamlit_path = os.path.join(VENV_DIR, "Scripts" if platform.system() == "Windows" else "bin", "streamlit")
    app_path = os.path.join(APP_DIR, "app.py")
    subprocess.Popen([streamlit_path, "run", app_path])  # Use Popen to launch independently

# Main Orchestration Function
def main():
    print("Starting full local setup for Film Success Analysis...\n")
    create_virtualenv()
    install_requirements()

    print("\nRunning full data pipeline...\n")
    for step in PIPELINE_STEPS:
        print(f"Running: {os.path.basename(step)}")
        run_script(step)
        print("Done\n")

    print("\nSetup complete! Launching dashboard...")
    launch_dashboard()

if __name__ == "__main__":
    main()