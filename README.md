
<!-- PROJECT BADGES -->
[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/gitnasr/CloudinaryScrapper.svg)](https://github.com/gitnasr/CloudinaryScrapper/commits/main) 

<!-- PROJECT TITLE -->
# Cloudinary Resource Scraper and Downloader ☁️⬇️

<!-- PROJECT DESCRIPTION -->
This Python script scrapes resources from your Cloudinary account, downloads them, and stores the data in a local database.  It handles pagination, rate limits, and directory structures. It is designed with robustness in mind, particularly dealing with Cloudinary's API and network operations.

<!-- TABLE OF CONTENTS -->
## Table of Contents
*   [Project Overview](#project-overview)
*   [Features](#features)
*   [Prerequisites](#prerequisites)
*   [Installation](#installation)
*   [Usage](#usage)
*   [Algorithms](#algorithms)
    *   [Resource Fetching with Pagination](#resource-fetching-with-pagination)
    *   [Rate Limit Handling](#rate-limit-handling)
    *   [Resource Download](#resource-download)
*   [File Structure](#file-structure)
*   [Configuration](#configuration)
*   [Error Handling](#error-handling)
*   [Contributing](#contributing)
*   [License](#license)
*   [Acknowledgments](#acknowledgments)

<!-- PROJECT OVERVIEW -->
## Project Overview

This project provides a script for fetching and downloading resources from a Cloudinary account. It is designed to be fault-tolerant and handle common issues like rate limits and network errors. The script uses the Cloudinary API to retrieve resources and save them to a local directory structure that mirrors the structure in your Cloudinary account. It also stores resource metadata to a TinyDB database for data management.

<!-- FEATURES -->
## Features

*   ✅ **Cloudinary API Integration:** Uses the Cloudinary Python library to interact with the Cloudinary API.
*   🔄 **Resource Fetching with Pagination:** Retrieves all resources, handling pagination through the Cloudinary API.
*   ⏱️ **Rate Limit Handling:** Implements rate limit detection and scheduling retries using the `apscheduler` library.
*   💾 **Local Storage:** Downloads resources to a local directory structure mirroring that of your Cloudinary account.
*   📦 **Data Persistence:** Stores resource metadata and pagination details in a local TinyDB database for efficient data management.
*   🛡️ **Error Handling:** includes robust error handling for network issues, API errors, and file I/O operations.
*   ⚙️ **Configuration:** Uses environment variables to store sensitive information (API keys, cloud name).

<!-- PREREQUISITES -->
## Prerequisites

Before you begin, ensure you have met the following requirements:

*   Python 3.8 or higher
*   A Cloudinary account
*   Basic understanding of Cloudinary concepts (cloud name, API key, API secret)
*   Environment set up to manage environment variables such as `.env` files.
*   Required Python packages installed (see Installation).

<!-- INSTALLATION -->
## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>  # Replace <repository_url> with your repository URL
    cd <your-repo-name>  # Replace `<your-repo-name>` with the name of your repository on your local system
    ```
2.  **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:

        ```bash
        .venv\Scripts\activate
        ```
    *   On macOS and Linux:

        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    *Create `requirements.txt` file and add the requirements, see below*.

    ```text
    cloudinary
    requests
    python-dotenv
    apscheduler
    tinydb
    ```
5.  **Configure your environment variables:**

    Create a `.env` file in the project root and set the following environment variables:

    ```env
    CLOUD_NAME=<your_cloudinary_cloud_name>
    API_KEY=<your_cloudinary_api_key>
    API_SECRET=<your_cloudinary_api_secret>
    ```
    Replace `<your_cloudinary_cloud_name>`, `<your_cloudinary_api_key>`, and `<your_cloudinary_api_secret>` with your actual Cloudinary credentials.

<!-- USAGE -->
## Usage

1.  **Run the script:**

    ```bash
    python main.py
    ```

2.  **Monitor the output:** The script will:
    *   Fetch resources from Cloudinary, page by page.
    *   Download the resources to a `downloads/<your_cloud_name>` directory, mirroring the folder structure in your Cloudinary account.
    *   Store resource metadata in a local `db.json` file using TinyDB.
    *   Handle rate limits and resume fetching automatically.

3.  **Check the output:** The downloaded resources will be stored in the `downloads` directory in a directory structure that mirrors the structure on your Cloudinary account. The `db.json` file will contain  the metadata of fetched resources and pagination state.

<!-- ALGORITHMS -->
## Algorithms

This section provides summaries of the key algorithms used in this project.

### Resource Fetching with Pagination 🔄

*   **Summary:** The `get_resources` method fetches resources from the Cloudinary API, handling pagination to retrieve all resources. It uses a `while` loop to iterate through pages, using the `next_cursor` value returned by the API to fetch the next set of resources, and extends the `all_resources` list.
*   **Steps:**
    1.  Initialize `cursor` to `None` and `page` to 1.
    2.  Call `cloudinary.api.resources` with `max_results` and `cursor`.
    3.  Append resources to the `all_resources` list.
    4.  Update `cursor` with the value from the response for the next page.
    5.  Increment `page`.
    6.  Store resources and pagination data in TinyDB.
    7.  Repeat from step 2 until `cursor` is `None`.
    8.  Call the `download_resource` method.

### Rate Limit Handling ⏱️

*   **Summary:** The script incorporates rate limit detection using information from API errors, schedules the next run using `apscheduler`, and retries fetching resources after a delay to avoid being blocked by the Cloudinary API.
*   **Steps:**
    1.  **Error Detection:** Catches exceptions from `cloudinary.api.resources`.
    2.  **Rate Limit Check:** Checks if the exception message includes "Rate Limit Exceeded".
    3.  **Time Extraction:** Parses the error message to extract the retry time.
    4.  **Scheduling:**  Uses extracted time from the error message.  Adds a job to the `apscheduler` to retry `get_resources` at the specified time using the `date` trigger.
    5.  **Retry:**  The scheduled job calls `get_resources` with the `next_cursor` and `page ` from the last run state.

### Resource Download ⬇️

*   **Summary:** The `download_resource` method iterates through the fetched resources and downloads each one using `requests`. It creates the necessary directory structure, handles potential file I/O errors, and provides progress feedback.
*   **Steps:**
    1.  Create the download directory if it doesn't exist.
    2.  Iterate over each resource in `self.all_resources`.
    3.  Construct the download URL and the local file path. It also performs a safety check to ensure the folder paths are valid.
    4.  Use `requests.get` with `stream=True` for efficient downloading.
    5.  Write the file in chunks to handle potentially large files.
    6.  Handle `requests.RequestException` and `IOError` for network and file saving errors, providing error messages.

<!-- FILE STRUCTURE -->
## File Structure

```
.
├── .env            # Environment variables
├── .gitignore      # Git ignore file
├── README.md       # This README file
├── main.py         # The main Python script
├──  db.json       # Local database for storing resource and pagination data (created after first run).
└── .venv           # Virtual environment (created after first run)
└── downloads       # Directory where downloaded resources are saved (created after first run)
```

<!-- CONFIGURATION -->
## Configuration

The project relies on environment variables to store sensitive information like your Cloudinary credentials.

*   **`.env` file:**
    *   `CLOUD_NAME`: Your Cloudinary cloud name.
    *   `API_KEY`: Your Cloudinary API key.
    *   `API_SECRET`: Your Cloudinary API secret.

<!-- ERROR HANDLING -->
## Error Handling

The script contains several error-handling mechanisms:

*   **Environment Variable Errors:** Checks for missing environment variables during initialization.
*   **API Errors:**  Handles potential exceptions from the Cloudinary API, particularly rate limit errors.
*   **Network Errors:** Catches `requests.RequestException` during download.
*   **File I/O Errors:** Handles `IOError` during file saving.
*   **Invalid Folder Path:** includes a check to prevent invalid folder paths, mitigating security risks to the local file system.
*   **Unexpected Errors:** Includes a generic `except` block to catch and report any other unexpected errors.

<!-- CONTRIBUTING -->
## Contributing

Contributions are welcome!  Feel free to:

*   Open an issue to report a bug or suggest an enhancement.
*   Submit a pull request with your proposed changes.

<!-- LICENSE -->
## License

This project is licensed under the [MIT License](LICENSE).

