from sqlalchemy import create_engine,ForeignKey ,Column, Integer, String, CHAR, Sequence
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DECIMAL, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
import sys
import re
import requests
from bs4 import BeautifulSoup
from models import Base, Company, Job, Skill, JobSkill, Category, company_categories
from Convertor import Convertor
from JobScraper import JobScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
from sqlalchemy import delete
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, text
import csv


engine = create_engine('sqlite:///C:/Users/hp/PycharmProjects/pythonProject/webscraping21.db', echo=True)
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


session.execute(delete(Job))
session.commit()

session.execute(delete(Category))
session.commit()

session.execute(delete(company_categories))
session.commit()

session.execute(delete(Skill))
session.commit()

session.execute(delete(Company))
session.commit()

session.execute(delete(JobSkill))
session.commit()


url='https://jobinja.ir/companies/pazhouhabshargh/jobs/CngC/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-php-%D9%85%D8%B3%D9%84%D8%B7-%D8%A8%D9%87-%D9%84%D8%A7%D8%B1%D8%A7%D9%88%D9%84-%D9%85%D8%B4%D9%87%D8%AF-%D8%AF%D8%B1-%D9%BE%D9%84%D8%AA%D9%81%D8%B1%D9%85-%D8%AA%D8%AE%D8%B5%D8%B5%DB%8C-%D9%BE%D8%B2%D8%B4%DA%A9%DB%8C-%D9%85%DB%8C%D9%86%D8%B3?_ref=16'
# url='https://jobinja.ir/companies/charter118/jobs/Cxl7/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-php-%D9%85%D8%B4%D9%87%D8%AF-%D8%AF%D8%B1-%DA%86%D8%A7%D8%B1%D8%AA%D8%B1-118?_ref=16'
# url='https://jobinja.ir/companies/creativebug/jobs/CiQg/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-%D8%A7%D8%B1%D8%B4%D8%AF-%D9%81%D9%84%D8%A7%D8%AA%D8%B1-senior-flutter-developer-%D9%85%D8%B4%D9%87%D8%AF-%D8%AF%D8%B1-%D8%A7%D8%B3%D8%AA%D9%88%D8%AF%DB%8C%D9%88-%DA%A9%D8%B1%DB%8C%D8%AA%DB%8C%D9%88-%D8%A8%D8%A7%DA%AF?_ref=16'
# url = 'https://jobinja.ir/companies/barnameh-nevisan-piahroieh-novin-toos/jobs/CiPu/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85-senior-angular-developer-%D9%85%D8%B4%D9%87%D8%AF-%D8%AF%D8%B1-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3%D8%A7%D9%86-%D9%BE%DB%8C%D8%B4%D8%B1%D9%88%DB%8C-%D9%86%D9%88%DB%8C%D9%86-%D8%AA%D9%88%D8%B3?_ref=16'
job_scraper = JobScraper(url)
job_id = job_scraper.get_job_scrapping()
job_scraper.get_categories(job_id)
# print('dfsd')
# sys.exit()
job_title=session.query(Job).filter_by(id=job_id).first().title
Conv = Convertor()
english_part= Conv.extract_english_phrase(job_title)

job_province=session.query(Job).filter_by(id=job_id).first().province
job_category=session.query(Job).filter_by(id=job_id).first().category

website = 'https://jobinja.ir'
service= Service(executable_path="chromedriver.exe")

driver = webdriver.Chrome(service=service)
driver.get(website)
driver.implicitly_wait(10)

input_element=driver.find_element(By.CLASS_NAME,"c-jobSearchTop__blockInput")
input_element.send_keys(english_part)

selection_divs = driver.find_elements(By.CSS_SELECTOR, ".select2-selection.select2-selection--single")

for selection_div in selection_divs:
    location_button = selection_div.find_element(By.XPATH, f'//*[@title="همه‌ی استان‌ها"]')
    category_button = selection_div.find_element(By.XPATH, f'//*[@title="همه‌ی دسته‌بندی‌ها"]')

location_button.click()
input_search=driver.find_element(By.CLASS_NAME,"select2-search__field")
input_search.send_keys(job_province+Keys.ENTER)

category_button.click()
input_search=driver.find_element(By.CLASS_NAME,"select2-search__field")
input_search.send_keys(job_category+Keys.ENTER)

search_button_div = driver.find_element(By.CSS_SELECTOR,".c-homeHeader2__inputBox.c-widthAuto")
search_button=search_button_div.find_element(By.CLASS_NAME,"c-jobSearchTop__submitButton")
search_button.click()

time.sleep(3)

new_url = driver.current_url
response = requests.get(new_url, verify=False)
new_content = response.text
soup = BeautifulSoup(new_content, 'lxml')

section_content = soup.find("section", class_="c-jobSearchView u-mB20")
job_lists=section_content.find("ul", class_="o-listView__list c-jobListView__list")

all_jobs=job_lists.find_all("li",class_="c-jobListView__item")

for job in all_jobs:
    job_div=job.find("a", class_="c-jobListView__titleLink")
    job_link=str(job_div['href'])
    scrapping_job=JobScraper(job_link)
    jobId=scrapping_job.get_job_scrapping()

    scrapping_job.get_categories(jobId)

time.sleep(4)
driver.quit()

# Job ID for filtering
sql_query = text("""
 SELECT sub1.id, sub1.title, sub1.link, sub1.matching_skills, sub2.matching_company_category,
           ((sub1.matching_skills * 2) + sub2.matching_company_category) AS total
    FROM
        (SELECT jobs.id, jobs.link, jobs.title,
                SUM(CASE WHEN s.name IN (SELECT s.name
                                         FROM jobs
                                         JOIN job_skills ON jobs.id = job_skills.job_id
                                         JOIN main.skills s ON s.id = job_skills.skill_id
                                         WHERE jobs.id = :job_id) THEN 1 ELSE 0 END) AS matching_skills
         FROM jobs
         JOIN job_skills ON jobs.id = job_skills.job_id
         JOIN main.skills s ON s.id = job_skills.skill_id
         WHERE jobs.id != :job_id
         GROUP BY jobs.id, jobs.title
         ORDER BY matching_skills DESC) AS sub1
    JOIN
        (SELECT jobs.id, jobs.title, company_categories.company_id,
                SUM(CASE WHEN categories.name IN (SELECT categories.name
                                                   FROM jobs
                                                   JOIN company_categories ON jobs.company_id = company_categories.company_id
                                                   JOIN categories ON company_categories.category_id = categories.id
                                                   WHERE jobs.id = :job_id) THEN 1 ELSE 0 END) AS matching_company_category
         FROM jobs
         JOIN company_categories ON jobs.company_id = company_categories.company_id
         JOIN categories ON company_categories.category_id = categories.id
         WHERE jobs.id != :job_id
         GROUP BY jobs.id, jobs.title
         ORDER BY matching_company_category DESC) AS sub2
    ON sub1.id = sub2.id
    ORDER BY sub1.matching_skills DESC, sub2.matching_company_category DESC;
""")

params = {'job_id': job_id}

# Execute the raw SQL query
result = session.execute(sql_query,params)
rows = result.fetchall()

column_headers = ["ID", "Title", "Link", "Matching Skills", "Matching Company Category", "Total"]

# Create or open the CSV file
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Create a CSV writer
    csv_writer = csv.writer(csvfile)

    # Write the column headers
    csv_writer.writerow(column_headers)

    # Write each row to the CSV file
    csv_writer.writerows(rows)

# Close the session
session.close()



