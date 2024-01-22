import requests
from bs4 import BeautifulSoup
from Convertor import Convertor
import re
from urllib.parse import urlparse
from sqlalchemy import create_engine,ForeignKey ,Column, Integer, String, CHAR, Sequence
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DECIMAL, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
import sys
from models import Base, Company, Job, Skill, JobSkill, Category, company_categories
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from sqlalchemy.orm import joinedload
from sqlalchemy import exists


class JobScraper:
    def __init__(self, url):
        self.url = url

    def get_company_name(self):
        # connect to database:
        # Define the SQLite database engine
        engine = create_engine('sqlite:///C:/Users/hp/PycharmProjects/pythonProject/webscraping21.db', echo=True)
        # Base.metadata.create_all(engine)

        # Create a session to interact with the database
        Session = sessionmaker(bind=engine)
        session = Session()



        response = requests.get(self.url, verify=False)
        jobinja_text = response.text
        soup = BeautifulSoup(jobinja_text, 'lxml')

        job_title = soup.find('h1').text
        job_content = soup.find('section', class_='c-jobView')
        # company_name = job_content.find
        job_info = soup.find('div', class_='c-companyHeader__info')
        company_name = job_info.find('h2', class_='c-companyHeader__name').get_text()

        company_industry=job_info.div.select_one('span:not([rel]) a').text

        company_header=soup.find('div',class_='c-companyHeader__coverContainerInner').find('a',class_='c-companyHeader__logoLink')['href']
        parsed_url = urlparse(company_header)
        company_slug = parsed_url.path.split('/')[2]

        idURL = soup.find('a', class_='c-sharingJobOnMobile__uniqueURL').get_text()
        numbers = re.findall(r'\d+', idURL)

        # Join the numbers (in case there are multiple numeric parts, this will concatenate them)
        id = int(''.join(numbers))

        # Find all divs with the specific class
        divs_with_class = job_content.find_all('h4', class_='c-infoBox__itemTitle')

        # Placeholder for the next sibling
        next_sibling_content = None

        for div in divs_with_class:
            if div.get_text(strip=True) == "موقعیت مکانی":
                # Get the next sibling of this div
                next_sibling = div.find_next_sibling()
                if next_sibling:
                    location = next_sibling.span.get_text(strip=True)
                break

        Conv = Convertor()

        province = Conv.get_province(location)
        city = Conv.get_city(location)

        # Find all divs with the specific class
        divs_with_category = job_content.find_all('h4', class_='c-infoBox__itemTitle')

        # Placeholder for the next sibling
        next_sibling_content = None

        for div in divs_with_class:
            if div.get_text(strip=True) == "دسته‌بندی شغلی":
                # Get the next sibling of this div
                next_sibling = div.find_next_sibling()
                if next_sibling:
                    category = next_sibling.span.get_text(strip=True)
                break


        divs_with_exp = job_content.find_all('h4', class_='c-infoBox__itemTitle')

        # Placeholder for the next sibling
        next_sibling_content = None

        for div in divs_with_exp:
            if div.get_text(strip=True) == "حداقل سابقه کار":
                # Get the next sibling of this div
                next_sibling = div.find_next_sibling()
                if next_sibling:
                    experience = next_sibling.span.get_text(strip=True)
                break


        # Find all divs with the specific class
        divs_with_info = job_content.find_all('h4', class_='c-infoBox__itemTitle')

        # Placeholder for the next sibling
        next_sibling_content = None

        for div in divs_with_info:
            if div.get_text(strip=True) == "مهارت‌های مورد نیاز":
                # Get the next sibling of this div
                next_sibling = div.find_next_sibling()
                if next_sibling:
                    # skills = next_sibling.span.get_text(strip=True)
                    skills = next_sibling
                break

        skills = Conv.extract_span_text(skills.find_all('span'))

        for skill in skills:
            lower_case_skill = skill.lower().strip()  # Convert skill name to lowercase
            existing_skill = session.query(Skill).filter_by(name=lower_case_skill).first()
            if not existing_skill:
                # Skill doesn't exist, create a new record
                new_skill = Skill(name=lower_case_skill)
                session.add(new_skill)

        session.commit()

        #inser to companies
        existing_company = session.query(Company).filter_by(slug=company_slug).first()
        if not existing_company:
            new_company=Company(name=company_name,slug=company_slug,industry=company_industry)
            session.add(new_company)
            session.commit()


        company_id = session.query(Company).filter_by(slug=company_slug).first().id

        existing_job = session.query(Job).filter_by(id=id).first()
        if not existing_job:
            #insert into jobs
            new_job=Job(id=id,title=job_title,company_id=company_id,link=idURL,
                    experience_years_min=experience,category=category,province=province,city=city)
            session.add(new_job)
            session.commit()


        for skill in skills:
            lower_case_skill = skill.lower().strip()
            skill_id = session.query(Skill).filter_by(name=lower_case_skill).first().id
            existing_job_skill=session.query(JobSkill).filter_by(skill_id=skill_id,job_id=id).first()
            if not existing_job_skill:
                new_job_skill=JobSkill(skill_id=skill_id,job_id=id)
                session.add(new_job_skill)
        session.commit()
        return id
        # return self.url





    def get_categories(self,job_id):
        engine = create_engine('sqlite:///C:/Users/hp/PycharmProjects/pythonProject/webscraping21.db', echo=True)
        # Base.metadata.create_all(engine)

        # Create a session to interact with the database
        Session = sessionmaker(bind=engine)
        session = Session()

        company = (
                 session.query(Company)
                .join(Job)
                .options(joinedload(Company.jobs))
                .filter(Job.id == job_id)
                .first()
                )
        company_id = company.id

        website = self.url
        service = Service(executable_path="chromedriver.exe")

        driver = webdriver.Chrome(service=service)
        driver.get(website)
        driver.implicitly_wait(10)

        # company_jobs_div = driver.find_element(By.CSS_SELECTOR,
        #                                            ".c-companyHeader__navigatorContainer.container.u-clearFix")
        #
        # company_headers = company_jobs_div.find_elements(By.CSS_SELECTOR, ".c-companyHeader__navigatorLink")
        # for header in company_headers:
        #     a_element = header.find_element(By.TAG_NAME,"a")
        #     print(a_element.text)
        #     sys.exit()

        company_jobs_div = driver.find_element(By.CSS_SELECTOR,
                                               ".c-companyHeader__navigatorContainer.container.u-clearFix ul")
        # print(company_jobs_div.get_attribute("outerHTML"))
        # sys.exit()
        company_headers = company_jobs_div.find_elements(By.TAG_NAME,'li')
        for header in company_headers:
            header_element=header.find_element(By.TAG_NAME,'a')
            text_content = str(header_element.text.strip())
            if "فرصت‌های شغلی" in text_content:
                header_element.click()
                time.sleep(2)

        current_url = str(driver.current_url)

        response = requests.get(current_url, verify=False)
        company_jobs_page = response.text
        soup = BeautifulSoup(company_jobs_page, 'lxml')
        job_lists=soup.find_all("li",class_="o-listView__item__application")

        count = 0
        for job in job_lists:
            job_url=str(job.find('a',class_="c-jobListView__titleLink")['href'])
            response = requests.get(job_url, verify=False)
            jobs_page = response.text
            job_soup=BeautifulSoup(jobs_page, 'lxml')
            job_content = job_soup.find('section', class_='c-jobView')
            divs_with_class = job_content.find_all('h4', class_='c-infoBox__itemTitle')
            for div in divs_with_class:
                if div.get_text(strip=True) == "دسته‌بندی شغلی":
                    # Get the next sibling of this div
                    next_sibling = div.find_next_sibling()
                    if next_sibling:
                        category = next_sibling.span.get_text(strip=True)
                        # print(company_id)
                        # sys.exit()
                        existing_category = session.query(Category).filter_by(name=category).first()
                        if not existing_category:
                            # Skill doesn't exist, create a new record
                            new_category = Category(name=category)
                            session.add(new_category)
                            # session.commit()
                            company.categories.append(new_category)
                            # session.commit()
                        else:
                            record_exists = session.query(exists().where(
                                (company_categories.c.company_id == company.id) &
                                (company_categories.c.category_id == existing_category.id)
                            )).scalar()
                            if not record_exists:
                                company.categories.append(existing_category)

            count += 1
            if count == 10:
                break

        session.commit()

        driver.quit()






