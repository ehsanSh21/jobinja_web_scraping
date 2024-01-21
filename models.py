from sqlalchemy import (create_engine, Column,DateTime, Integer, String, Text,
                        Date, DECIMAL, ForeignKey, Table)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine,ForeignKey ,Column, Integer, String, CHAR, Sequence
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

company_categories = Table(
    'company_categories',
    Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('category_id', Integer, ForeignKey('categories.id')),
)


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slug=Column(String(255), nullable=False,unique=True)
    description = Column(Text)
    location = Column(String(255))
    industry = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    categories = relationship('Category', secondary=company_categories, back_populates='companies')
    jobs = relationship('Job', back_populates='company')

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    description = Column(Text)
    link = Column(String(255), nullable=False, unique=True)
    province = Column(String(255))
    city = Column(String(255))
    category = Column(String(255), nullable=False)
    posted_date = Column(Date)
    experience_years_min = Column(String(255))
    experience_years_max = Column(String(255))
    salary_min = Column(DECIMAL(10, 2))
    salary_max = Column(DECIMAL(10, 2))
    salary_currency = Column(String(3))
    company = relationship('Company', back_populates='jobs')

class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

class JobSkill(Base):
    __tablename__ = 'job_skills'
    job_id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    skill_id = Column(Integer, ForeignKey('skills.id'), primary_key=True)
    job = relationship('Job', back_populates='skills')
    skill = relationship('Skill', back_populates='jobs')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    companies = relationship('Company', secondary=company_categories, back_populates='categories')




# Add back-population relationships
Company.jobs = relationship('Job', back_populates='company')
# Job.categories = relationship('JobCategory', back_populates='job')
Job.skills = relationship('JobSkill', back_populates='job')
# Category.jobs = relationship('JobCategory', back_populates='category')
Skill.jobs = relationship('JobSkill', back_populates='skill')


