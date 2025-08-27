from sqlalchemy import Column, Integer, String, Date, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class JobApplication(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    job_title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    application_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    deadline = Column(Date, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<JobApplication(id={self.id}, title='{self.job_title}', company='{self.company}')>"

    def display(self):
        deadline_str = self.deadline.strftime(
            "%Y-%m-%d") if self.deadline else "No deadline"
        notes_str = self.notes if self.notes else "No notes"

        return (f"ID: {self.id}\n"
                f"Job Title: {self.job_title}\n"
                f"Company: {self.company}\n"
                f"Application Date: {self.application_date}\n"
                f"Status: {self.status}\n"
                f"Deadline: {deadline_str}\n"
                f"Notes: {notes_str}\n"
                + "-" * 40)
