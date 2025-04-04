# Climate of the Earth - Lecture Repository

This repository contains all materials and resources for the lecture **Climate of the Earth**. The main branch triggers a CI/CD pipeline (`.drone.yml`) to automatically deploy the website hosted at [Climate of the Earth Website](https://iow-lectures.pages.io-warnemuende.de/climateoftheearth/).

## Repository Structure

- **additional/**  
  Contains supplementary materials for the lecture.

- **exercise/**  
  Includes exercises for students, reorganized for easier navigation.

- **figures/**  
  A collection of figures used throughout the lecture content.

- **homework/**  
  Homework assignments for the lecture, reorganized for clarity.

- **prepare_project_work/**  
  Includes a Jupyter Notebook for preprocessing data, useful for project work.

- **project_files/**
  Files related to projects and further resources.

- **_config.yml**  
  Configuration file for the website.

- **_toc.yml**  
  Table of contents for structuring the website content.

- **.drone.yml**  
  CI/CD pipeline configuration file for automating deployment.

- **environment.yml**  
  Dependencies and environment setup for reproducibility.

- **index.md**  
  Main landing page content for the lecture website.

- **README.md**  
  Overview of the repository and instructions for use.

## Features

- **Automated Deployment**: Pushes to the `main` branch trigger a CI/CD pipeline that deploys changes to the website.


## Usage

Clone the repository:

  ```bash
  git clone https://git.io-warnemuende.de/iow-lectures/climateoftheearth.git
  conda env create -f environment.yml
  conda activate book
  ```
