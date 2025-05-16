from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import declarative_base

from connection import engine

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, unique=True, nullable=False)
    department_name = Column(String(100), nullable=False)
    imported_from = Column(String(255))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())


class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, unique=True)
    job_name = Column(String(100), nullable=False)
    imported_from = Column(String(255))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())



class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, unique=True)
    name = Column(String(150), nullable=False)
    hire_datetime = Column(DateTime)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))
    imported_from = Column(String(255))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())

    # Declare relationships
    department = relationship('Department', back_populates='employees')
    job = relationship('Job', back_populates='employees')


if __name__ == "__main__":
    Base.metadata.create_all(engine)