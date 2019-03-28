import json
from app import db
from datetime import datetime

class Employer(db.Model):
    __tablename__='employer'
    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    company = db.Column(db.String(30), default='None')
    country = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    dev_biography = db.Column(db.String(1000))
    profile_picture = db.Column(db.LargeBinary)
    Date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    member_since = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    jobs_of_employer = db.relationship('Jobs_Of_Employer', lazy=True, backref='jobs')

    def __init__(self, name, username, email, password, company, country, dev_biography):
        self.name = name
        self.username = username
        self.email = email
        self.company = company
        self.country = country
        self.password = password
        self.dev_biography = dev_biography

    
    def addEmployer(_name, _username, _email, _password, _dev_biography, _company, _country):
        newEmployer = Employer(name=_name, username=_username, email=_email, password=_password, dev_biography=_dev_biography, company=_company, country=_country)
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
            "Country": self.country,
            "Username": self.username,
	    "Password":self.password,
	    "Biography":self.dev_biography,
            "Member_Since":self.Date_posted.strftime('%Y-%m-%d')
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
    Date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    job_applicants = db.relationship('Job_Applicants', lazy=True, backref='jobs')

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
            "Status": self.work_status,
            "Username": self.username,
	    "Password": self.password,
	    "Other_Skills":self.other_stacks,
	    "Biography":self.dev_biography,
	    "Email": self.email,
	    "Country": self.country,
            "Member_Since":self.Date_posted.strftime('%Y-%m-%d')
        }

        return json.dumps(employee_object)


class Jobs_Of_Employer(db.Model):
    __tablename__='jobs_of_employer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    main_stack = db.Column(db.String(25), nullable=False)
    other_stacks = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(20), nullable=False)
    Date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'))
    job_applicants = db.relationship('Job_Applicants', lazy=True, backref='applicants')

    def __init__(self, title, description, main_stack, other_stacks, job_type, employer_id):
        self.title = title
        self.description = description
        self.main_stack = main_stack
        self.other_stacks = other_stacks
        self.job_type = job_type
        self.employer_id = employer_id
    
    def addJob(_title, _description, _main_stack, _other_stack, _job_type, _employer_id):
        new_Job = Jobs_Of_Employer(title=_title, description=_description, main_stack=_main_stack, other_stacks=_other_stack, job_type=_job_type, employer_id=_employer_id)
        db.session.add(new_Job)
        db.session.commit()

    def removeJob(_title):
        job_delete = Jobs_Of_Employer.query.filter_by(title=_title).delete()
        db.session.commit()

    def searchJob(_stack):
        to_search = Jobs_Of_Employer.query.filter_by(main_stack=_stack).first()
        return to_search
    
    def searchwork_status(_work_status):
        to_search = Jobs_Of_Employer.query.filter_by(job_type=_work_status).first()
        return to_search
    
    def __repr__(self):
        jobs_object={
            "Job_Title": self.title,
            "Stack": self.main_stack,
            "Job_Type":self.job_type,
            "Description":self.description,
            "Date_Posted":self.Date_posted.strftime('%Y-%m-%d')
        }

        return json.dumps(jobs_object)

class Job_Applicants(db.Model):
    __tablename__='job_applicants'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name =  db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    main_stack = db.Column(db.String(25), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    applicants_id = db.Column(db.Integer, db.ForeignKey('jobs_of_employer.id'))

    def __init__(self, name, title, main_stack, employee_id, applicants_id):
        self.name = name
        self.title = title
        self.main_stack = main_stack
        self.employee_id = employee_id
        self.applicants_id = applicants_id

    def addJobEmp(_name, _title, _main_stack, _employee_id, _applicants_id):
        new_Job = Job_Applicants(name=_name, title=_title, main_stack=_main_stack, employee_id=_employee_id, applicants_id=_applicants_id)
        db.session.add(new_Job)
        db.session.commit()
    
    def __repr__(self):
        job_applicants={
	    "Id": str(self.id),
            "Job_Title": self.title,
            "Applicant": self.name,
            "Stack": self.main_stack
        }

        return json.dumps(job_applicants)

class Inbox(db.Model):
    __tablename__ = 'inbox'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    sender =  db.Column(db.String(30), nullable=False)
    Date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username, subject, description, sender):
        self.username = username
        self.subject = subject
        self.description = description
        self.sender = sender
    
    def sendMessage(_username, _subject, _description, _sender):
        sent_message = Inbox(username=_username, subject=_subject, description=_description, sender=_sender)
        db.session.add(sent_message)
        db.session.commit()
    
    def __repr__(self):
        message={
            "Subject": self.subject,
            "To": self.username, 
            "From": self.sender,
            "Description": self.description,
            "Date_Posted":self.Date_posted.strftime('%Y-%m-%d')
        }

        return json.dumps(message)



