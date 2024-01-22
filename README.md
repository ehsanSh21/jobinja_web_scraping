# Project Overview

This web scraping project is designed to automate the process of collecting and analyzing job data from a specific job portal. Leveraging the power of tools such as **Selenium**, **BeautifulSoup**, **Requests**, and **SQLAlchemy ORM**, this project aims to streamline the extraction and storage of valuable job-related information.

## Table of Contents

1. [Key Features](#key-features)
2. [Technologies Used](#technologies-used)
3. [Entity Relationship Diagram](#entity-relationship-diagram)
4. [Identifying Related Jobs](#identifying-related-jobs)


## Key Features

### 1. Targeted Job Scraping

- Provide a specific job link.
- Extract details such as title, salary, category, skills, location, and company insights.

### 2. Automated Search Operation

- Use **Selenium** to automate job searches.
- Dynamically input job details for an automated search operation.

### 3. Detailed Job List Scrapping

- Scrape and store details for each job in search results.
- Maintain a database for organized data management.

### 4. SQL Query for Job Matching

- Implement SQL queries to identify related jobs based on shared skills.
- Consider the similarity of job categories for each company.

### 5. CSV Export of Results

- Compile and export related job titles and links into a CSV file.

## Technologies Used

- **Selenium:** Automates web browser interactions for seamless navigation.
- **BeautifulSoup:** Extracts structured information from HTML and XML files.
- **Requests:** Makes web requests for efficient data retrieval.
- **SQLAlchemy ORM:** Provides a high-level interface for interacting with databases.

## Entity Relationship Diagram:

<img src="https://github.com/ehsanSh21/jobinja_web_scraping/blob/master/webscraping21.png" alt="Database Diagram" width="700" height="800">


## Identifying Related Jobs

I've employed SQL queries to pinpoint related jobs based on shared skills and the similarity of job categories for each company. The query operates in two layers:

### Matching Skills

- Calculates a `matching_skills` score by counting shared skills between a specific job (e.g., `1101263`) and others.
- Correlates skills from the `jobs`, `job_skills`, and `main.skills` tables.

### Matching Company Categories

- Determines a `matching_company_category` score by counting shared categories among companies associated with jobs.
- Correlates categories from the `jobs`, `company_categories`, and `categories` tables.

### Composite Score

- Combines scores to calculate an overall `total` score, giving twice the weight to skills.

This query help identify jobs with similar skills and companies offering similar job categories, providing a comprehensive approach to finding related jobs.

#### SQL Query: 
```sql
select sub1.id,sub1.title,
       sub1.link,
       sub1.matching_skills,
       sub2.matching_company_category,
       ((sub1.matching_skills*2)+(sub2.matching_company_category)) as total
from
(
select jobs.id,
       jobs.link,
       jobs.title,
    sum(CASE when s.name in (select s.name
from jobs
join job_skills on jobs.id = job_skills.job_id
join main.skills s on s.id = job_skills.skill_id
where jobs.id=1101263) then 1 else 0
end) as matching_skills
from jobs
join job_skills on jobs.id = job_skills.job_id
join main.skills s on s.id = job_skills.skill_id
where jobs.id!=1101263
group by jobs.id, jobs.title
order by matching_skills desc) as sub1
join
(select jobs.id,
       jobs.title,
       company_categories.company_id,
        sum(CASE when categories.name in (select categories.name
from jobs
join company_categories on jobs.company_id=company_categories.company_id
join categories on company_categories.category_id = categories.id
where jobs.id=1101263) then 1 else 0
end) as matching_company_category

from jobs
join company_categories on jobs.company_id=company_categories.company_id
join categories on company_categories.category_id = categories.id
where jobs.id!=1101263
group by jobs.id, jobs.title
order by matching_company_category desc
) as sub2
on sub1.id=sub2.id
ORDER BY sub1.matching_skills DESC, sub2.matching_company_category DESC
;

```




This project combines web scraping, automation, and database management to empower users in exploring and analyzing job opportunities effortlessly.
