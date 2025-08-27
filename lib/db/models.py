# lib/db/models.py
from datetime import date
from sqlalchemy import (
    Column, Integer, String, Date, Enum, ForeignKey, Table, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from .database import Base, engine, get_session
import enum

# --- Association tables for many-to-many ---
applicant_skills = Table(
    "applicant_skills", Base.metadata,
    Column("applicant_id", ForeignKey("applicants.id"), primary_key=True),
    Column("skill_id", ForeignKey("skills.id"), primary_key=True),
    UniqueConstraint("applicant_id", "skill_id", name="uq_applicant_skill")
)

job_skills = Table(
    "job_skills", Base.metadata,
    Column("job_id", ForeignKey("jobs.id"), primary_key=True),
    Column("skill_id", ForeignKey("skills.id"), primary_key=True),
    UniqueConstraint("job_id", "skill_id", name="uq_job_skill")
)


class StatusEnum(str, enum.Enum):
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"

# --- Base mixin with common ORM helpers ---


class ORMHelpers:
    @classmethod
    def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, _id: int):
        return session.get(cls, _id)

    def delete(self, session):
        session.delete(self)
        session.commit()

# --- Models ---


class Company(Base, ORMHelpers):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    industry: Mapped[str] = mapped_column(String(120), nullable=True)
    location: Mapped[str] = mapped_column(String(120), nullable=True)

    # one-to-many
    jobs = relationship("Job", back_populates="company",
                        cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Company {self.id} {self.name}>"

    @validates("name")
    def validate_name(self, _, value):
        if not value or not value.strip():
            raise ValueError("Company name cannot be empty")
        return value.strip()


class Skill(Base, ORMHelpers):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    # many-to-many backrefs
    applicants = relationship(
        "Applicant", secondary=applicant_skills, back_populates="skills")
    jobs = relationship("Job", secondary=job_skills, back_populates="skills")

    @validates("name")
    def validate_name(self, _, value):
        v = (value or "").strip().lower()
        if not v:
            raise ValueError("Skill name cannot be empty")
        return v

    def __repr__(self):
        return f"<Skill {self.name}>"


class Applicant(Base, ORMHelpers):
    __tablename__ = "applicants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(160), nullable=False, unique=True)

    # many-to-many
    skills = relationship(
        "Skill", secondary=applicant_skills, back_populates="applicants")

    # one-to-many applications
    applications = relationship(
        "JobApplication", back_populates="applicant", cascade="all, delete-orphan")

    @property
    def skill_count(self) -> int:
        return len(self.skills)

    @validates("name")
    def validate_name(self, _, value):
        v = (value or "").strip()
        if not v:
            raise ValueError("Applicant name cannot be empty")
        return v

    @validates("email")
    def validate_email(self, _, value):
        v = (value or "").strip().lower()
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format")
        return v

    def __repr__(self):
        return f"<Applicant {self.id} {self.name}>"


class Job(Base, ORMHelpers):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"), nullable=False)
    company = relationship("Company", back_populates="jobs")

    # many-to-many required skills
    skills = relationship("Skill", secondary=job_skills, back_populates="jobs")

    # applications (one-to-many)
    applications = relationship(
        "JobApplication", back_populates="job", cascade="all, delete-orphan")

    @validates("title")
    def validate_title(self, _, value):
        v = (value or "").strip()
        if not v:
            raise ValueError("Job title cannot be empty")
        return v

    def __repr__(self):
        return f"<Job {self.id} {self.title} @ {self.company.name}>"


class JobApplication(Base, ORMHelpers):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_applied: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum), nullable=False, default=StatusEnum.applied)

    applicant_id: Mapped[int] = mapped_column(
        ForeignKey("applicants.id"), nullable=False)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)

    applicant = relationship("Applicant", back_populates="applications")
    job = relationship("Job", back_populates="applications")

    __table_args__ = (
        UniqueConstraint("applicant_id", "job_id",
                         name="uq_applicant_job_once"),
        CheckConstraint(
            "status in ('applied','interview','offer','rejected')", name="ck_status_valid"),
    )

    def __repr__(self):
        return f"<Application {self.id} {self.applicant.name} -> {self.job.title} [{self.status}]>"

# --- Create tables helper ---


def init_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
