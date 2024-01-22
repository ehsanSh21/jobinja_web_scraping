## Overview

This web scraping project is designed to automate the process of collecting and analyzing job data from a specific job portal. Leveraging the power of tools such as **Selenium**, **BeautifulSoup**, **Requests**, and **SQLAlchemy ORM**, this project aims to streamline the extraction and storage of valuable job-related information.

### Key Features:

- **Targeted Job Scraping:**
  - Begin by providing a specific job link of interest.
  - Extract comprehensive details for the specified job, including title, salary, category, skills required, location, and insights about the associated company.

- **Automated Search Operation:**
  - Utilize **Selenium** for automating the search functionality on the job portal.
  - Dynamically input job title, location, and category based on the data obtained for the specific job.
  - Execute a search to retrieve a list of relevant job opportunities.

- **Detailed Job List Scrapping:**
  - For each job in the search results, systematically scrape and store job details similar to the initial specific job.
  - Maintain a database to efficiently organize and manage the accumulated job-related data.

- **SQL Query for Job Matching:**
  - Implement a targeted SQL query to identify jobs related to the specific job based on shared skills.
  - Consider the similarity of job categories for each company to enhance result accuracy.

- **CSV Export of Results:**
  - Compile and export the titles and links of related jobs into a CSV file for convenient reference.

### Technologies Used:

- **Selenium:**
  - A powerful tool for automating web browser interactions, enabling seamless navigation and data collection.

- **BeautifulSoup:**
  - A Python library for pulling data out of HTML and XML files, facilitating the extraction of structured information from web pages.

- **Requests:**
  - A simple HTTP library for making web requests, enhancing the efficiency of data retrieval.

- **SQLAlchemy ORM:**
  - An Object-Relational Mapping (ORM) library for Python, providing a convenient and high-level interface for interacting with databases.

This project aims to empower users to effortlessly explore and analyze job opportunities by combining the capabilities of web scraping, automation, and database management.
