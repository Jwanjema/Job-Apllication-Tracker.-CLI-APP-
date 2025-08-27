from sqlalchemy import create_engine, func, case
from sqlalchemy.orm import sessionmaker
from models import Base, JobApplication


def init_db():
    """Initialize the database with required tables"""
    engine = create_engine('sqlite:///job_applications.db')
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    """Create a database session"""
    Session = sessionmaker(bind=engine)
    return Session()


def add_application(session, job_title, company, application_date, status, deadline=None, notes=None):
    """Add a new job application to the database"""
    application = JobApplication(
        job_title=job_title,
        company=company,
        application_date=application_date,
        status=status,
        deadline=deadline,
        notes=notes
    )
    session.add(application)
    session.commit()
    return application.id


def get_all_applications(session):
    """Retrieve all job applications from the database"""
    return session.query(JobApplication).order_by(JobApplication.application_date.desc()).all()


def update_application_status(session, app_id, new_status):
    """Update the status of an application"""
    application = session.query(JobApplication).filter(
        JobApplication.id == app_id).first()
    if application:
        application.status = new_status
        session.commit()
        return True
    return False


def delete_application(session, app_id):
    """Delete an application from the database"""
    application = session.query(JobApplication).filter(
        JobApplication.id == app_id).first()
    if application:
        session.delete(application)
        session.commit()
        return True
    return False


def search_applications(session, search_term):
    """Search applications by company or job title"""
    return session.query(JobApplication).filter(
        (JobApplication.job_title.ilike(f'%{search_term}%')) |
        (JobApplication.company.ilike(f'%{search_term}%'))
    ).order_by(JobApplication.application_date.desc()).all()


def get_companies_stats(session):
    """Get statistics grouped by company"""
    # Get all applications grouped by company
    stats = session.query(
        JobApplication.company,
        func.count(JobApplication.id).label('total_apps'),
        func.sum(case((JobApplication.status == 'Applied', 1), else_=0)).label(
            'applied'),
        func.sum(case((JobApplication.status == 'Interviewing', 1), else_=0)).label(
            'interviewing'),
        func.sum(case((JobApplication.status == 'Offer', 1), else_=0)
                 ).label('offers'),
        func.sum(case((JobApplication.status == 'Rejected', 1), else_=0)).label(
            'rejected'),
        func.sum(case((JobApplication.status == 'Accepted', 1), else_=0)).label(
            'accepted'),
        func.sum(case((JobApplication.status == 'Withdrawn', 1), else_=0)).label(
            'withdrawn')
    ).group_by(JobApplication.company).order_by(func.count(JobApplication.id).desc()).all()

    return stats
