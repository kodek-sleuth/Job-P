import json
from app import *
from Models.portal import *
from flask.views import MethodView
from flask import current_app, Blueprint

jobs = Blueprint('jobs', __name__)

@jobs.route('/jobs', methods=['GET'])
def get_jobs():
    jobs_on_platform  = Jobs_Of_Employer.query.all()
    jobs_on_platformStr = str(jobs_on_platform)
    jobsToJson=json.loads(jobs_on_platformStr)

    return make_response(jsonify(jobsToJson))

@jobs.route('/jobs/<string:stack>', methods=['GET'])
def get_jobs_by_stack(stack):
    try:
        jobs_on_platform  = Jobs_Of_Employer.query.filter_by(main_stack=stack).first()
        jobs_on_platformStr = str(jobs_on_platform)
        jobsToJson=json.loads(jobs_on_platformStr)
        return make_response(jsonify(jobsToJson)), 200
    
    except:
        response={
            "Message": "Please Enter Valid Stack"
        }

@jobs.route('/jobs/<string:role>', methods=['GET'])
def get_jobs_by_role(stack):
    try:
        jobs_on_platform  = Jobs_Of_Employer.query.filter_by(job_type=role).first()
        jobs_on_platformStr = str(jobs_on_platform)
        jobsToJson=json.loads(jobs_on_platformStr)
        return make_response(jsonify(jobsToJson)), 200
    
    except:
        response={
            "Message": "Please Enter Valid Stack"
        }

@jobs.route('/empoyeer/employees', methods=['POST'])
def get_applicants_by_username():
    try:
        request_data = request.get_json()
        username = request_data['Username']

        if username:
            employees_on_platform  = Employee.query.filter_by(username=username).first()
            employees_on_platformStr = str(employees_on_platform)
            employeesToJson=json.loads(employees_on_platformStr)
            return make_response(jsonify(employeesToJson)), 200
        
        else:
            response={
                "Message": "Result Not Found"
            }
            return make_response(jsonify(response)), 200
    
    except:
        response={
            "Message": "Please Enter Valid Username"
        }
        
        return make_response(jsonify(response)), 200


@jobs.route('/employer/<string:stack>', methods=['GET'])
def get_applicant_by_stack(stack):
    emp = Employee.query.filter_by(main_stack=stack).first()
    empToStr = str(emp)
    empToJson=json.loads(empToStr)

    return make_response(jsonify(empToJson)), 200



@jobs.route('/employee/<string:username>/applied', methods=['GET'])
def get_jobs_applied(username):
    try:
        emp = Employee.query.filter_by(username=username).first()
        empToStr = str(emp.job_applicants)
        toJson = json.loads(empToStr)

        return make_response(jsonify(toJson)), 200
    
    except:
        response={
            "Message": "Login or SignUp to use This service"
        }

        return make_response(jsonify(response)), 500


@jobs.route('/employee/<string:username>/posted', methods=['GET'])
def get_jobs_posted(username):
    try:
        emp = Employer.query.filter_by(username=username).first()
        empToStr = str(emp.jobs_of_employer)
        toJson = json.loads(empToStr)

        return make_response(jsonify(toJson)), 200
    
    except:
        response={
            "Message": "Login or SignUp to use This service"
        }

        return make_response(jsonify(response)), 500

@jobs.route('/employee/<string:username>/inbox', methods=['GET'])
def get_inbox(username):
    try:
        emp = Employee.query.filter_by(username=username).first()
        empToStr = str(emp.inbox)
        toJson = json.loads(empToStr)

        return make_response(jsonify(toJson)), 200
    
    except:
        response={
            "Message": "Login or SignUp to use This service"
        }

        return make_response(jsonify(response)), 500

@jobs.route('/employees', methods=['GET'])
def get_employees():
    emp = Employee.query.all()
    empToStr = str(emp)
    toJson = json.loads(empToStr)
    return make_response(jsonify(toJson)), 200

@jobs.route('/job/applicants/<int:job_id>', methods=['GET'])
def get_applicants_of_job(job_id):
    emp_job = Jobs_Of_Employer.query.filter_by(id=job_id).first()
    if emp_job:
        emp_job_applicants_str = str(emp_job.job_applicants)
        toJson = json.loads(emp_job_applicants_str)
        return make_response(jsonify(toJson)), 200

@jobs.route('/employee/<string:employee_username>/inbox', methods=['POST'])
def send_message_to_employer(employee_username):
    try:
        request_data = request.get_json(force=True)
        username = request_data['To <Username>']
        subject = request_data['Subject']
        description = request_data['Description']

        check_employee = Employee.query.filter_by(username=employee_username).first()
        check_employer = Employer.query.filter_by(username=username).first()

        if check_employee and check_employer:
            Inbox.sendMessage(check_employer.username, subject, description, check_employee.username, check_employee.id, check_employer.id)
            response={
                "Message": "Successfully Sent Message To "+check_employer.name
            }

            return make_response(jsonify(response)), 200

        else:
            response={
                "Message": "Enter Valid Credentials"
            }

            return make_response(jsonify(response)), 401

    except:
        response={
                "Message": "Please Enter Valid Credentials"
            }

        return make_response(jsonify(response)), 401

@jobs.route('/employer/<string:employer_username>/inbox', methods=['POST'])
def send_message_to_employee(employer_username):
    try:
        request_data = request.get_json(force=True)
        username = request_data['To <Username>']
        subject = request_data['Subject']
        description = request_data['Description']

        check_employee = Employee.query.filter_by(username=username).first()
        check_employer = Employer.query.filter_by(username=employer_username).first()

        if check_employee and check_employer:
            Inbox.sendMessage(check_employee.username, subject, description, check_employer.username, check_employee.id, check_employer.id)
            response={
                "Message": "Successfully Sent Message To"+check_employee.name
            }

            return make_response(jsonify(response)), 200
        
        else:
            response={
                "Message": "Enter Valid Credentials"
            }

            return make_response(jsonify(response)), 401

    except:
        response={
                "Message": "Please Enter Valid Credentials"
            }

        return make_response(jsonify(response)), 401


@jobs.route('/employee/inbox/<string:username>/received', methods=['GET'])
def get_employee_received(username):
    emptli=[]
    emp = Employee.query.filter_by(username=username).first()
    to_str = str(emp.inbox)
    new_data = json.loads(to_str)
    for user in new_data:
        if user['To']==username:
            emptli.append(user)
    
    return make_response(jsonify(emptli)), 200


@jobs.route('/employer/inbox/<string:username>/received', methods=['GET'])
def get_employer_received(username):
    emptli=[]
    emp = Employer.query.filter_by(username=username).first()
    to_str = str(emp.inbox)
    new_data = json.loads(to_str)
    for user in new_data:
        if user['To']==username:
            emptli.append(user)
    
    return make_response(jsonify(emptli)), 200








