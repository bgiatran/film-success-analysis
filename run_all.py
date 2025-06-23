import os
import subprocess
import sys
import platform
import venv
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, "venv")

def create_virtualenv():
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
    else:
        print("Virtual environment already exists.")

def install_requirements():
    print("Installing requirements...")
    pip_path = os.path.join(VENV_DIR, "Scripts" if platform.system() == "Windows" else "bin", "pip")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])

def run_script(script_path):
    python_path = os.path.join(VENV_DIR, "Scripts" if platform.system() == "Windows" else "bin", "python")
    subprocess.run([python_path, script_path])

def launch_dashboard():
    print("Launching Streamlit dashboard...")
    streamlit_path = os.path.join(VENV_DIR, "Scripts" if platform.system() == "Windows" else "bin", "streamlit")
    subprocess.run([streamlit_path, "run", "app.py"])

def main():
    print("Starting full local setup...")

    create_virtualenv()
    install_requirements()

    print("Initializing database and importing data...")
    run_script(os.path.join("scripts", "init_db.py"))
    run_script(os.path.join("scripts", "data_pipeline.py"))

    print("Training machine learning model...")
    run_script("train_model.py")

    print("Setup complete!")
    launch_dashboard()

if __name__ == "__main__":
    main()