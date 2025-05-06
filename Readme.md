# Project README

This is a Python project with three Python files representing different phases of the project. Below are the instructions for setting up the environment and running the project.

---

## Table of Contents
1. [Environment Setup](#environment-setup)
    - [Using Pipenv](#using-pipenv)
    - [Using Conda](#using-conda)
    - [Using Pip](#using-pip)
2. [Running the Project](#running-the-project)

---

## Environment Setup

### Using Pipenv
Pipenv is a tool that manages dependencies and virtual environments for Python projects.

1. Install Pipenv if you don't have it:
    ```
    pip install pipenv
    ```

2. Navigate to the project directory and create a virtual environment:
    ```
    pipenv install
    ```

3. Activate the virtual environment:
    ```
    pipenv shell
    ```

4. (Optional) Install any additional dependencies:
    ```
    pipenv install <package_name>
    ```

---

### Using Conda
Conda is an open-source package management system and environment management system.

1. Create a new conda environment:
    ```
    conda create -n myenv python=3.9
    ```

2. Activate the environment:
    ```
    conda activate myenv
    ```

3. Install dependencies from `requirements.txt` (if available):
    ```
    pip install -r requirements.txt
    ```

---

### Using Pip
Pip is the standard package installer for Python.

1. Install virtualenv if you don't have it:
    ```
    pip install virtualenv
    ```

2. Create a virtual environment:
    ```
    virtualenv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```
        source venv/bin/activate
        ```

4. Install dependencies from `requirements.txt` (if available):
    ```
    pip install -r requirements.txt
    ```

---

## Running the Project

The project consists of three Python files, each corresponding to a different phase of the project:

### To run the App directly
```
streamlit run main.py
```

### To run app in different phases

1. Phase 1: Run the first phase using:
    ```
    streamlit run frontend.py
    ```

2. Phase 2: Run the second phase using:
    ```
    python vector_database.py
    ```

3. Phase 3: Run the third phase using:
    ```
    python rag_pipeline.py
    ```

Ensure that all dependencies are installed before running the scripts.

---

If you encounter any issues, feel free to reach out or check the documentation for the tools mentioned above.