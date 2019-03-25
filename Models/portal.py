import json
from app import db

class Employer(db.Model):
    __tablename__='employer'
    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    company = db.Column(db.String(30))
    country = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    jobsemployer = db.relationship('JobsEmployer', lazy=True, backref='jobs')

    def __init__(self, name, username, email, password, company, country):
        self.name = name
        self.username = username
        self.email = email
        self.company = company
        self.country = country
        self.password = password

    
    def addEmployer(_name, _username, _email, _password, _company, _country):
        newEmployer = Employer(name=_name, username=_username, email=_email, company=_company, country=_country, password=_password)
        db.session.add(newEmployer)
        db.session.commit()
    
    def getEmployers():
        employers = Employer.query.all()
        return employers
    
    def getEmployer(_username):
        the_employer = Employer.query.filter_by(username=_username).first()
        return the_employer

    def __repr__(self):
        employer_object={
            "Name": self.name,
            "Company": self.company, 
            "Country": self.country
        }

        return json.dumps(employer_object)

class Employee(db.Model):
    __tablename__='employee'
    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    work_status = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    main_stack = db.Column(db.String(25), nullable=False)
    other_stacks = db.Column(db.String(100))
    dev_biography = db.Column(db.String(1000))
    profile_cv = db.Column(db.LargeBinary)
    profile_picture = db.Column(db.LargeBinary)
    jobsemployees = db.relationship('JobsEmployees', lazy=True, backref='jobs')


    def __init__(self, name, username, email, password, work_status, country, main_stack, other_stacks, dev_biography):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.work_status = work_status
        self.country = country
        self.main_stack = main_stack
        self.other_stacks = other_stacks
        self.dev_biography = dev_biography
      
    
    def addEmployee(_name, _username, _email, _password, _work_status, _country, _main_stack, _other_stacks, _dev_biography):
        newEmployer = Employee(name=_name, username=_username, email=_email, password=_password, work_status=_work_status, country=_country, main_stack=_main_stack, other_stacks=_other_stacks, dev_biography=_dev_biography)
        db.session.add(newEmployer)
        db.session.commit()
    
    def getEmployees():
        employers = Employee.query.all()
        return employers
    
    def getEmployee(_username):
        the_employer = Employee.query.filter_by(username=_username).first()
        return the_employer
    
    def getByExpertise(_stacks):
        the_employees = Employee.query.filter_by(main_stack=_stacks).first()
        return the_employees

    
    def __repr__(self):
        employee_object={
            "Name": self.name,
            "Expertise": self.main_stack, 
            "work_status": self.work_status
        }

        return json.dumps(employee_object)


class JobsEmployer(db.Model):
    __tablename__='jobsemployer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    main_stack = db.Column(db.String(25), nullable=False)
    other_stacks = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(20), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'))

    def __init__(self, title, description, main_stack, other_stacks, job_type, employer_id):
        self.title = title
        self.description = description
        self.main_stack = main_stack
        self.other_stacks = other_stacks
        self.job_type = job_type
        self.employer_id = employer_id
    
    def addJob(_title, _description, _main_stack, _other_stack, _job_type, _employer_id):
        new_Job = JobsEmployer(title=_title, description=_description, main_stack=_main_stack, other_stacks=_other_stack, job_type=_job_type, employer_id=_employer_id)
        db.session.add(new_Job)
        db.session.commit()

    def removeJob(_title):
        job_delete = JobsEmployer.query.filter_by(title=_title).delete()
        db.session.commit()

    def searchJob(_stack):
        to_search = JobsEmployer.query.filter_by(main_stack=_stack).first()
        return to_search
    
    def searchwork_status(_work_status):
        to_search = JobsEmployer.query.filter_by(job_type=_work_status).first()
        return to_search
    
    def __repr__(self):
        jobs_object={
            "Job": self.title,
            "Stack": self.main_stack
        }

        return json.dumps(jobs_object)

class JobsEmployees(db.Model):
    __tablename__='jobs_employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    interview = db.Column(db.String(100))
    main_stack = db.Column(db.String(25), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __init__(self, title, main_stack, employee_id):
        self.title = title
        self.main_stack = main_stack
        self.employee_id = employee_id


    def addJobEmp(_title, _main_stack, _employee_id):
        new_Job = JobsEmployees(title=_title, main_stack=_main_stack, employee_id=_employee_id)
        db.session.add(new_Job)
        db.session.commit()

    def searchJob(_stack):
        to_search = JobsEmployer.query.filter_by(main_stack=_stack).first()
        return to_search 
    
    def __repr__(self):
        jobs_object={
            "Job": self.title,
            "Stack": self.main_stack
        }

        return json.dumps(jobs_object)
    